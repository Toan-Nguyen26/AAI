const chatSection = document.getElementById("chat-section");
const reviewsSection = document.getElementById("reviews-section");
const creditsSection = document.getElementById("credits-section");
const welcomePage = document.getElementById("welcome-page");
const homeButton = document.getElementById("home-button");
const toggleSidebar = document.getElementById("toggle-sidebar");

const chatOption = document.getElementById("chat-option");
const reviewsOption = document.getElementById("reviews-option");
const creditsOption = document.getElementById("credits-option");
const navButtons = document.querySelectorAll(".nav-btn");

const sidebar = document.getElementById("sidebar");
const sidebarContent = document.getElementById("sidebar-content");
const parentingHelpContainer = document.getElementById(
  "parenting-help-container"
);
const toggleSidebarButton = document.getElementById("toggle-sidebar");
const collapseIcon = document.getElementById("collapse-icon");

// Hide all sections
function hideAllSections() {
  chatSection.classList.add("hidden");
  reviewsSection.classList.add("hidden");
  creditsSection.classList.add("hidden");
  welcomePage.classList.add("hidden");
}

// Show specific section
function showSection(section) {
  hideAllSections();
  section.classList.remove("hidden");
  section.classList.add("visible");
}

// Reset active button state
function resetActiveButtons() {
  navButtons.forEach((btn) => btn.classList.remove("active"));
}

// Sidebar button event listeners
chatOption.addEventListener("click", () => {
  resetActiveButtons();
  chatOption.classList.add("active");
  showSection(chatSection);
});

reviewsOption.addEventListener("click", () => {
  resetActiveButtons();
  reviewsOption.classList.add("active");
  showSection(reviewsSection);
});

creditsOption.addEventListener("click", () => {
  resetActiveButtons();
  creditsOption.classList.add("active");
  showSection(creditsSection);
});

// Home button event listener
homeButton.addEventListener("click", () => {
  resetActiveButtons();
  showSection(welcomePage);
});

toggleSidebarButton.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");

  // Toggle the icon between <- and ->
  if (sidebar.classList.contains("collapsed")) {
    collapseIcon.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
          </svg>
      `;
  } else {
    collapseIcon.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18" />
          </svg>
      `;
  }
});
// Default: Show welcome page
hideAllSections();
showSection(welcomePage);
