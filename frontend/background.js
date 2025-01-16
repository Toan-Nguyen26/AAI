const images = ["images/1.jpg", "images/2.jpg", "images/3.jpg", "images/4.jpg"];

const mainContent = document.getElementById("main-content");
let currentImageIndex = 0;

function changeBackground() {
  mainContent.style.backgroundImage = `url('${images[currentImageIndex]}')`;
  currentImageIndex = (currentImageIndex + 1) % images.length;
}

setInterval(changeBackground, 5000);
changeBackground();
