import argparse, csv, json, time, re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo  # se der erro no Windows: pip install tzdata
import requests

DISCORD_API = "https://discord.com/api/v10"
DISCORD_EPOCH_MS = 1420070400000  # 2015-01-01T00:00:00Z

def dt_to_snowflake(dt_utc: datetime) -> int:
    ms = int(dt_utc.timestamp() * 1000)
    return (ms - DISCORD_EPOCH_MS) << 22

def parse_date_local(date_str: str, tz_name: str) -> tuple[datetime, datetime]:
    """
    Aceita 'YYYY-MM-DD' ou 'DD/MM/YYYY' e retorna (start_utc, end_utc) do dia no fuso informado.
    """
    if "/" in date_str:
        d, m, y = date_str.split("/")
        local_start = datetime(int(y), int(m), int(d), 0, 0, 0, tzinfo=ZoneInfo(tz_name))
    else:
        local_start = datetime.fromisoformat(date_str).replace(tzinfo=ZoneInfo(tz_name))
    start_utc = local_start.astimezone(timezone.utc)
    end_utc = (local_start + timedelta(days=1)).astimezone(timezone.utc)
    return start_utc, end_utc

def validate_channel_in_guild(token: str, channel_id: str, guild_id: str | None):
    if not guild_id:
        return
    headers = {"Authorization": f"Bot {token}"}
    r = requests.get(f"{DISCORD_API}/channels/{channel_id}", headers=headers, timeout=30)
    r.raise_for_status()
    info = r.json()
    if str(info.get("guild_id")) != str(guild_id):
        raise RuntimeError(f"Canal {channel_id} não pertence à guild {guild_id} (guild real: {info.get('guild_id')}).")

def fetch_channel_day(
    token: str, channel_id: str, start_utc: datetime, end_utc: datetime,
    contains: list[str] | None = None, require_all: bool = False,
    regex: str | None = None, authors: list[str] | None = None,
    rate_sleep=0.3
):
    start_sf = dt_to_snowflake(start_utc)
    end_sf = dt_to_snowflake(end_utc)

    headers = {"Authorization": f"Bot {token}"}
    url = f"{DISCORD_API}/channels/{channel_id}/messages"

    results = []
    before = end_sf
    rx = re.compile(regex, flags=re.IGNORECASE|re.MULTILINE) if regex else None

    def passes_filters(m):
        # autor
        if authors:
            aid = m["author"]["id"]
            aname = (m["author"].get("username") or "").lower()
            if not any(a == aid or a.lower() == aname for a in authors):
                return False
        # conteúdo
        txt = m.get("content", "") or ""
        if contains:
            checks = [(c.lower() in txt.lower()) for c in contains]
            if require_all and not all(checks):
                return False
            if not require_all and not any(checks):
                return False
        if rx and not rx.search(txt):
            return False
        return True

    while True:
        params = {"limit": 100, "before": str(before)}
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code == 429:
            retry = resp.json().get("retry_after", 1.0)
            time.sleep(float(retry) + 0.25)
            continue
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break

        for m in batch:
            ts = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
            if ts < start_utc:
                break
            if start_utc <= ts < end_utc and passes_filters(m):
                results.append({
                    "channel_id": channel_id,
                    "id": m["id"],
                    "timestamp": ts.isoformat(),
                    "author_id": m["author"]["id"],
                    "author_name": m["author"].get("username"),
                    "content": m.get("content", ""),
                    "attachments": [a.get("url") for a in m.get("attachments", [])],
                    "mentions": [u.get("id") for u in m.get("mentions", [])],
                })
        before = int(batch[-1]["id"])
        oldest_ts = datetime.fromisoformat(batch[-1]["timestamp"].replace("Z", "+00:00"))
        if oldest_ts < start_utc:
            break
        time.sleep(rate_sleep)

    return results

def save_csv(path: str, rows: list[dict]):
    keys = ["channel_id","id","timestamp","author_id","author_name","content","attachments","mentions"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        if not rows:
            f.write("")
            return
        import csv
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            r = r.copy()
            r["attachments"] = ",".join(r.get("attachments", []))
            r["mentions"] = ",".join(r.get("mentions", []))
            w.writerow(r)

def save_json(path: str, rows: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def main():
    ap = argparse.ArgumentParser(description="Exporta mensagens de um dia específico (com filtros).")
    ap.add_argument("--token", required=True, help="Bot token.")
    ap.add_argument("--channels", nargs="+", required=True, help="IDs de canais (um ou mais).")
    ap.add_argument("--date", required=True, help="Data 'YYYY-MM-DD' ou 'DD/MM/YYYY' (fuso local).")
    ap.add_argument("--tz", default="America/Fortaleza", help="Fuso, ex.: America/Fortaleza.")
    ap.add_argument("--out", required=True, help="Arquivo de saída (.csv ou .json).")
    ap.add_argument("--guild", help="Opcional: valida se o canal pertence a esta guild (server ID).")
    ap.add_argument("--contains", nargs="*", help="Filtrar mensagens que contenham essas palavras (qualquer uma por padrão).")
    ap.add_argument("--all", action="store_true", help="Se passado, exige TODAS as palavras de --contains.")
    ap.add_argument("--regex", help="Regex para filtrar conteúdo (IGN Case).")
    ap.add_argument("--authors", nargs="*", help="Filtrar por autores (IDs ou usernames).")
    args = ap.parse_args()

    start_utc, end_utc = parse_date_local(args.date, args.tz)

    all_rows = []
    for ch in args.channels:
        if args.guild:
            validate_channel_in_guild(args.token, ch, args.guild)
        print(f"[+] Buscando {args.date} (fuso {args.tz}) no canal {ch}…")
        rows = fetch_channel_day(
            args.token, ch, start_utc, end_utc,
            contains=args.contains, require_all=args.all,
            regex=args.regex, authors=args.authors
        )
        print(f"    {len(rows)} mensagens encontradas.")
        all_rows.extend(rows)

    if args.out.lower().endswith(".csv"):
        save_csv(args.out, all_rows)
    else:
        save_json(args.out, all_rows)
    print(f"[✓] Salvo em {args.out}")

if __name__ == "__main__":
    main()
