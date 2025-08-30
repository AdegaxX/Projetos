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