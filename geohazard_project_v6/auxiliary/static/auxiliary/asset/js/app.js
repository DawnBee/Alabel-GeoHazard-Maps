// Mobile NavBar Toggle
const mainScreen = document.getElementById("main");
const navMobileBtn = document.querySelector(".mobile-nav-btn");
const navMobileMenu = document.querySelector(".nav-menu-mobile");

navMobileBtn.addEventListener('click', () => {
  if (!navMobileMenu.classList.contains("shown")) {
    navMobileMenu.classList.add("shown");
    navMobileBtn.classList.add("expanded");
  } else {
    navMobileMenu.classList.remove("shown");
    navMobileBtn.classList.remove("expanded");
  }
});

mainScreen.addEventListener('click', () => {
  navMobileMenu.classList.remove("shown");
  navMobileBtn.classList.remove("expanded");
  navDesktopDropMenu.classList.remove("reveal");
});


// Mobile NavBar Dropdown Toggle
const navMobileDropArrow = document.querySelector(".mobile-drop-arrow");
const navMobileDropMenu = document.querySelector(".mobile-drop-menu");

navMobileDropArrow.addEventListener('click', () => {
  if (!navMobileDropMenu.classList.contains("reveal")) {
    navMobileDropMenu.classList.add("reveal");
  }  else {
    navMobileDropMenu.classList.remove("reveal");
  }
});


// Desktop NavBar Dropdown Toggle
const navDesktopDropArrow = document.querySelector(".drop-arrow");
const navDesktopDropMenu = document.querySelector(".drop-menu");

navDesktopDropArrow.addEventListener('click', () => {
  if (!navDesktopDropMenu.classList.contains("reveal")) {
    navDesktopDropMenu.classList.add("reveal");
  }  else {
    navDesktopDropMenu.classList.remove("reveal");
  }
});


// Selection Tabs 
const tabButtons = document.querySelectorAll(".tab-btn")
const allContents = document.querySelectorAll(".tab-content")

tabButtons.forEach((tab, index) => {
  tab.addEventListener('click',(e) => {
    tabButtons.forEach(tab => {tab.classList.remove("active")});
    tab.classList.add("active");
  allContents.forEach(content => {content.classList.remove("active")});
  allContents[index].classList.add("active");
  })
})


// Community Sorting
const sortBtn = document.querySelector(".sort-btn");
const sortOptions = document.querySelector(".sort-options")
const postBox = document.querySelector(".post-container")
const infoBox = document.querySelector(".community-info")

sortBtn.addEventListener('click', () => {
  if (!sortOptions.classList.contains('active')) {
    sortOptions.classList.add('active');
  } else {
    sortOptions.classList.remove('active');
  }
});

postBox.addEventListener('click', () => {
  sortOptions.classList.remove('active');
});

infoBox.addEventListener('click', () => {
  sortOptions.classList.remove('active');
});