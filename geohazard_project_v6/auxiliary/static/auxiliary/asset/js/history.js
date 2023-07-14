// History Filter
const geoBtn = document.getElementById('banner-geo-btn');
const assesBtn = document.getElementById('banner-asses-btn');
const geoContainer = document.getElementById('geo-container');
const assesContainer = document.getElementById('assessments');


geoBtn.addEventListener('click', () => {
	geoContainer.classList.add('active');
	geoBtn.classList.add('active');
	assesContainer.classList.remove('active');
});

assesBtn.addEventListener('click', () => {
	geoContainer.classList.remove('active');
	geoBtn.classList.remove('active');
	assesContainer.classList.add('active');
});


// Scroll-to-top Arrow
const scrollToTopArrow = document.querySelector('.scroll-to-top');

// Show/hide arrow based on scroll position
window.addEventListener('scroll', () => {
  const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
  const scrollThreshold = document.documentElement.scrollHeight - window.innerHeight;

  if (scrollPosition > scrollThreshold * 0.7) {
    scrollToTopArrow.classList.add('show');
  } else {
    scrollToTopArrow.classList.remove('show');
  }
});

// Scroll to top when arrow is clicked
scrollToTopArrow.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});




