// ── Sidebar mobile toggle ──
function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!sidebar) return;
  const isOpen = sidebar.classList.contains('open');
  if (isOpen) {
    sidebar.classList.remove('open');
    overlay && overlay.classList.remove('open');
  } else {
    sidebar.classList.add('open');
    overlay && overlay.classList.add('open');
  }
}
function closeSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  sidebar && sidebar.classList.remove('open');
  overlay && overlay.classList.remove('open');
}
// Fecha sidebar ao navegar (mobile)
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', () => {
    if (window.innerWidth <= 768) closeSidebar();
  });
});

// ── Modal: fecha ao clicar no backdrop ──
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.classList.remove('open');
  }
});

// ── Modal: fecha com Escape ──
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-backdrop.open')
      .forEach(m => m.classList.remove('open'));
  }
});

// ── Modal: abre via data-modal="id" ──
document.addEventListener('click', e => {
  const btn = e.target.closest('[data-modal]');
  if (btn) {
    const target = document.getElementById(btn.dataset.modal);
    if (target) target.classList.add('open');
  }
});

// ── Auto-dismiss alerts após 4s ──
document.querySelectorAll('.alert').forEach(a => {
  setTimeout(() => {
    a.style.transition = 'opacity .4s';
    a.style.opacity = '0';
    setTimeout(() => a.remove(), 400);
  }, 4000);
});

// ── Loading state em forms ──
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button[type=submit]');
    if (btn && !btn.dataset.noload) {
      btn.disabled = true;
      btn.style.opacity = '.6';
    }
  });
});
