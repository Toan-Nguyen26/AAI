const urlParams = new URLSearchParams(window.location.search);
const backendUrl = urlParams.get("api_url") || "http://localhost:8000/api/chat";
console.log("Backend URL:", backendUrl);
console.log("URL Parameters:", urlParams.toString());
console.log("Full URL:", window.location.href);
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

// Function to format the assistant's response
function formatResponse(response) {
  if (typeof response === "object") {
    return `<pre class="bg-gray-200 p-2 rounded-lg">${JSON.stringify(
      response,
      null,
      2
    )}</pre>`;
  }
  return response;
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
