// MENU BURGER
const burger = document.getElementById('burger');
const links = document.getElementById('navLinks');

if (burger && links) {
  burger.addEventListener('click', () => {
    const isOpen = links.classList.toggle('open');
    burger.classList.toggle('open', isOpen);
    burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  // Fecha o menu ao clicar em um link
  links.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      links.classList.remove('open');
      burger.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    });
  });
}





// Para o carrossel:
  (function(){
    const root = document.querySelector('.crunch-hero');
    const slides = [...root.querySelectorAll('.slide')];
    const prevBtn = root.querySelector('.prev');
    const nextBtn = root.querySelector('.next');
    const dotsBox = root.querySelector('.dots');
    const AUTO = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--auto-ms')) || 7000;

    // cria dots
    slides.forEach((_, i) => {
      const b = document.createElement('button');
      b.className = 'dot' + (i === 0 ? ' is-active' : '');
      b.type = 'button';
      b.setAttribute('aria-label', `Ir para slide ${i+1}`);
      b.addEventListener('click', () => goTo(i, true));
      dotsBox.appendChild(b);
    });

    let index = 0, timer = null;

    function setActive(i){
      slides.forEach((s, k) => s.classList.toggle('is-active', k === i));
      [...dotsBox.children].forEach((d, k) => {
        d.classList.toggle('is-active', k === i);
        // reinicia animação do progresso
        d.style.animation = 'none';
        d.offsetHeight; // reflow
        d.style.animation = '';
      });
    }

    function goTo(i, user){
      index = (i + slides.length) % slides.length;
      setActive(index);
      if (user) restart(); // se usuário clicar, reinicia timer
    }

    function next(){ goTo(index + 1); }
    function prev(){ goTo(index - 1); }

    function restart(){
      clearInterval(timer);
      timer = setInterval(next, AUTO);
    }

    prevBtn.addEventListener('click', () => prev());
    nextBtn.addEventListener('click', () => next());

    // pausa auto-rolagem quando mouse está sobre o hero ou quando foco entra
    root.addEventListener('mouseenter', () => clearInterval(timer));
    root.addEventListener('mouseleave', restart);
    root.addEventListener('focusin', () => clearInterval(timer));
    root.addEventListener('focusout', restart);

    restart();
  })();