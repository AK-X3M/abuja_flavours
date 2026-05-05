// ============================================================
// Abuja Flavours — Main JS
// ============================================================

// Toast notification system
function showToast(message, type = 'success') {
  const container = document.getElementById('dynamicToast') || createToastContainer();
  container.style.display = 'flex';
  
  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✓' : '✕'}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => {
      toast.remove();
      if (container.children.length === 0) container.style.display = 'none';
    }, 300);
  }, 3000);
}

function createToastContainer() {
  let container = document.getElementById('dynamicToast');
  if (!container) {
    container = document.createElement('div');
    container.id = 'dynamicToast';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  return container;
}

// Auto-dismiss static toasts
document.addEventListener('DOMContentLoaded', () => {
  const staticToasts = document.querySelectorAll('#toastContainer .toast');
  staticToasts.forEach((toast, i) => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000 + (i * 300));
  });
  
  // Smooth payment option selection visual feedback
  document.querySelectorAll('.payment-option').forEach(option => {
    option.addEventListener('click', () => {
      document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('payment-option--selected'));
      option.classList.add('payment-option--selected');
    });
  });
});

// Template filter polyfill — get_item from dict
// (handled server-side via custom template tag)
