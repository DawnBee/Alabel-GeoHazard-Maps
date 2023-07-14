// Modal Settings
const openModalBtn = document.getElementById('open-modal-btn');
const closeModalBtn = document.getElementById('close-modal-btn');
const modalOverlay = document.getElementById('modal-overlay');

openModalBtn.addEventListener('click', function () {
  showModal();
});

closeModalBtn.addEventListener('click', function () {
  hideModal();
});

function showModal() {
  modalOverlay.style.opacity = '1';
  modalOverlay.style.pointerEvents = 'auto';
  document.addEventListener('keydown', handleKeyPress);
};

function hideModal() {
  modalOverlay.style.opacity = '0';
  modalOverlay.style.pointerEvents = 'none';
  document.removeEventListener('keydown', handleKeyPress);
};

function handleKeyPress(event) {
  if (event.key === 'Escape') {
    hideModal();
  }
};