// MENU BURGER
const burger = document.getElementById('burger');
const links = document.getElementById('navLinks');

if (burger && links) {        // para evitar erro de null, só abre quando os há algo no burger ou no links
  burger.addEventListener('click', () => {
    const isOpen = links.classList.toggle('open');    //adiciona ou remove a classe open no contêiner dos links, retorna TRUE ou FALSE

    burger.classList.toggle('open', isOpen);    //garante que o burger receba a classe open
    
    burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');    // 'true' quando o menu está aberto, 'false' quando fechado.
  
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


// Botões do carrossel:
const carrossel = document.getElementById("carrossel");
const botaoesquerda = document.querySelector(".botao.esquerda");
const botaodireita = document.querySelector(".botao.direita");

botaoesquerda.addEventListener("click", () => {
  carrossel.scrollBy({ left: -220, behavior: "smooth" }); 
});

botaodireita.addEventListener("click", () => {
  carrossel.scrollBy({ left: 220, behavior: "smooth" }); 
});