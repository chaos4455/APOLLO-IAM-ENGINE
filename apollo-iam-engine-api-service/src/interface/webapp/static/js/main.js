// fecha modal ao clicar no backdrop
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('open');
  }
});
// fecha modal com Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.open')
      .forEach(m => m.classList.remove('open'));
  }
});
// auto-dismiss alerts após 4s
document.querySelectorAll('.alert').forEach(a => {
  setTimeout(() => { a.style.opacity = '0'; a.style.transition = 'opacity .4s';
    setTimeout(() => a.remove(), 400); }, 4000);
});
