// Back to top button
const goTopBtn = document.getElementById("goTopBtn");

function toggleGoTopButton() {
  const scrollPosition = window.scrollY;
  const totalHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;

  if (scrollPosition / totalHeight >= 0.2) {
    goTopBtn.style.display = "flex";
  } else {
    goTopBtn.style.display = "none";
  }
}

window.addEventListener("scroll", toggleGoTopButton);

window.addEventListener("load", toggleGoTopButton);

goTopBtn.addEventListener("click", function (e) {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});


// Initialize AOS

document.addEventListener('DOMContentLoaded', function () {
    AOS.init({
      duration: 1500,
      offset: 200,
      easing: "ease-in-out",
    });
});

// Initialize AOS

gsap.registerPlugin(ScrollTrigger);
