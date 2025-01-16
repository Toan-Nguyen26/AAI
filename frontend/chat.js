const urlParams = new URLSearchParams(window.location.search);
const baseUrl = urlParams.get("api_url") || "http://localhost:8000";
const backendUrl = `${baseUrl}/api/chat`;

const chatLog = document.getElementById("chat-log");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const loadingSpinner = document.getElementById("loading-spinner");

// Function to display messages in the chat log
function addMessage(role, content) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `mb-4 ${
    role === "user" ? "text-blue-800" : "text-green-800"
  }`;
  messageDiv.innerHTML =
    role === "user"
      ? `<strong>You:</strong> ${content}`
      : `<strong>Assistant:</strong> ${formatResponse(content)}`;
  chatLog.appendChild(messageDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function formatResponse(response) {
  // If response is an object, extract its "response" key (expected format)
  if (typeof response === "object" && response.response) {
    const responseText = response.response;

    // Split the response into sections using double newlines for paragraphs
    const sections = responseText.split(/\n\n/);

    return sections
      .map((section) => {
        if (section.startsWith("**")) {
          // Bold Text - Headings or emphasized text
          return `<strong>${section.replace(
            /\*\*(.*?)\*\*/g,
            "$1"
          )}</strong><br>`;
        } else if (section.startsWith("-")) {
          // List items
          const items = section
            .split("\n")
            .filter((line) => line.startsWith("-"));
          const listHtml = items
            .map((item) => `<li>${item.replace(/^\-\s*/, "")}</li>`)
            .join("");
          return `<ul>${listHtml}</ul>`;
        } else {
          // Regular paragraphs
          return `<p>${section.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
          )}</p>`;
        }
      })
      .join("");
  }

  // Fallback to displaying raw JSON if no response key is found
  if (typeof response === "object") {
    return `<pre class="bg-gray-200 p-2 rounded-lg">${JSON.stringify(
      response,
      null,
      2
    )}</pre>`;
  }

  // Handle plain string responses as a fallback
  return `<p>${response}</p>`;
}

// Function to toggle button loading state
function setLoadingState(isLoading) {
  sendBtn.disabled = isLoading;
  loadingSpinner.classList.toggle("hidden", !isLoading);
}

sendBtn.addEventListener("click", async () => {
  const message = userInput.value.trim();
  if (!message) {
    alert("Please type a message.");
    return;
  }

  // Add user message to the chat log
  addMessage("user", message);
  userInput.value = "";

  // Disable button and show loading spinner
  setLoadingState(true);

  // Send message to the backend
  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: message }),
    });
    const data = await response.json();
    addMessage("assistant", data.response);
  } catch (error) {
    console.error(error);
    addMessage("assistant", "Error: Unable to connect to the backend.");
  }

  // Enable button and hide loading spinner
  setLoadingState(false);
});
