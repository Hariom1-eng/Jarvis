const log = document.getElementById("conversation-log");
const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const statusPill = document.getElementById("status-pill");
const modeChip = document.getElementById("mode-chip");
const emotionChip = document.getElementById("emotion-chip");
const wakeWords = document.getElementById("wake-words");
const reminders = document.getElementById("reminders");
const todos = document.getElementById("todos");

function addEntry(role, text) {
  const card = document.createElement("div");
  card.className = `entry ${role}`;
  card.innerHTML = `<strong>${role === "user" ? "You" : "Jarvis"}</strong><div>${text}</div>`;
  log.appendChild(card);
  log.scrollTop = log.scrollHeight;
}

async function loadBoot() {
  const [bootRes, stateRes] = await Promise.all([
    fetch("/api/boot"),
    fetch("/api/state")
  ]);
  const boot = await bootRes.json();
  const state = await stateRes.json();
  addEntry("jarvis", boot.message);
  wakeWords.textContent = (state.wake_words || []).join(", ");
  reminders.textContent = (state.reminders || []).join(" | ") || "none";
  todos.textContent = (state.todos || []).join(" | ") || "none";
  modeChip.textContent = state.mode || "professional";
  statusPill.textContent = "Systems online";
}

async function sendMessage(message) {
  addEntry("user", message);
  statusPill.textContent = "Processing request";
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });
  const payload = await response.json();
  if (!response.ok) {
    addEntry("jarvis", payload.error || "Request failed.");
    statusPill.textContent = "Request failed";
    return;
  }
  addEntry("jarvis", payload.reply);
  modeChip.textContent = payload.mode || "professional";
  emotionChip.textContent = payload.emotion || "calm";
  statusPill.textContent = "Task completed";

  const stateRes = await fetch("/api/state");
  const state = await stateRes.json();
  reminders.textContent = (state.reminders || []).join(" | ") || "none";
  todos.textContent = (state.todos || []).join(" | ") || "none";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  await sendMessage(message);
});

document.querySelectorAll("[data-fill]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.fill;
    input.focus();
  });
});

loadBoot().catch(() => {
  statusPill.textContent = "Boot failed";
  addEntry("jarvis", "I recommend caution. The localhost control room could not complete startup.");
});
