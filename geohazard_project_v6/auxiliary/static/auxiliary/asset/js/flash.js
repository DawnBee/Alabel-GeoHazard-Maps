// Flash Message Settings
const flashMessage = document.querySelector('.flash-message');
const closeMessage = document.querySelector('.close-flash');

closeMessage.addEventListener('click', () => {
  flashMessage.classList.add('closed')
});