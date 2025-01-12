# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:43:24 2025

@author: leand
"""

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_reddit(subreddit, max_posts=500):
    base_url = "https://old.reddit.com/r/Helldivers/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    titles_and_comments = []
    posts_scraped = 0

    while base_url and posts_scraped < max_posts:
        response = requests.get(base_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data from {base_url} (Status code: {response.status_code})")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraindo o título e o link dos comentários:
        posts = soup.find_all('div', class_='thing')
        for post in posts:
            if posts_scraped >= max_posts:
                break

            title = post.find('a', class_='title')
            comments_link = post.find('a', class_='comments')

            if title and comments_link:
                post_data = {
                    'title': title.text,
                    'comments_url': comments_link['href'],
                }
                
                post_response = requests.get(comments_link['href'], headers=headers)
                post_soup = BeautifulSoup(post_response.text, 'html.parser')
                comments = post_soup.find_all('div', class_='md')

                post_data['comments'] = [comment.text.strip() for comment in comments if comment.text]
                titles_and_comments.append(post_data)

                posts_scraped += 1

        # Para ir navegando pelas páginas:
        next_button = soup.find('span', class_='next-button')
        base_url = next_button.a['href'] if next_button else None

        time.sleep(2) # uma espera de 2s para o servidor não bloquear

    return titles_and_comments


# Salvando para .csv:
def save_to_csv(data, filename="reddit_data.csv"):
    rows = []
    for post in data:
        title = post['title']
        comments_url = post['comments_url']
        for comment in post['comments']:
            rows.append({
                'title': title,
                'comments_url': comments_url,
                'comment': comment
            })
    
    # Criando o DF para um .csv:
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data saved to {filename}")



# Example usage
subreddit = "python"
scraped_data = scrape_reddit(subreddit, max_posts=30) # seleciona a quant de posts




# Print results
#for post in scraped_data:
#    print(f"Title: {post['title']}")
#    print("Comments:")
#    for comment in post['comments']:
#        print(f"- {comment}")
#    print("-" * 80)




#for post in mostra:
#    print(f"Title: {post['title']}")
#    print("Comments:")
#    # Ignora o primeiro comentário usando fatiamento
#    for comment in post['comments'][1:]:
#        print(f"- {comment}")
#    print("-" * 80)



#save_to_csv(scraped_data, "reddit_python_dados2.csv")