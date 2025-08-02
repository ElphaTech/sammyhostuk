const hero = document.getElementById('logo-area');

const minHeight = 80; // matches logo height
const maxHeight = window.innerHeight;

window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const newHeight = Math.max(minHeight, maxHeight - scrollY);

    hero.style.height = newHeight + 'px';
    hero.style.position = 'relative';
});
