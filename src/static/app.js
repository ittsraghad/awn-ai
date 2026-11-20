/*
=========================================
AWN AI — Application logic
Talks to POST /api/chat and GET /health
=========================================
*/

document.addEventListener("DOMContentLoaded", () => {

    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const messagesContainer = document.getElementById("messages");
    const conversation = document.getElementById("conversation");
    const sendButton = document.getElementById("send-button");
    const newChatButton = document.getElementById("new-chat-button");
    const characterCount = document.getElementById("character-count");
    const statusBox = document.querySelector(".header-status");
    const statusText = document.getElementById("status-text");

    const MAX_LENGTH = 2000;

    const SCOPE_LABELS = {
        IN_SCOPE: "Answered from knowledge base",
        OUT_OF_SCOPE: "Outside what AWN supports",
        UNCLEAR_SCOPE: "Needs more detail"
    };

    let isWaiting = false;


    // ---------- Helpers ----------

    function el(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text) node.textContent = text;
        return node;
    }

    function prettify(value) {
        // "track_order" -> "Track order"
        const text = String(value).replace(/_/g, " ").trim().toLowerCase();
        return text.charAt(0).toUpperCase() + text.slice(1);
    }

    function scrollToBottom() {
        // The page scrolls (not the message box), so the newest message stays visible above the composer
        window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "smooth" });
    }

    function updateCharacterCount() {
        characterCount.textContent = `${messageInput.value.length} / ${MAX_LENGTH}`;
    }

    function resizeInput() {
        messageInput.style.height = "auto";
        messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + "px";
    }

    function setBusy(busy) {
        isWaiting = busy;
        sendButton.disabled = busy;
        messageInput.disabled = busy;
        newChatButton.disabled = busy;
        document.querySelectorAll(".chip, .topic").forEach((b) => { b.disabled = busy; });
    }


    // ---------- Conversation mode ----------

    function startChatMode() {
        document.body.classList.add("is-chatting");
        conversation.hidden = false;
    }

    function endChatMode() {
        document.body.classList.remove("is-chatting");
        conversation.hidden = true;
        messagesContainer.replaceChildren();
    }


    // ---------- Messages ----------

    function addUserMessage(content) {
        const message = el("div", "message user");
        message.append(el("span", "message-label", "You"), el("div", "message-bubble", content));
        messagesContainer.appendChild(message);
        scrollToBottom();
    }

    function addAssistantMessage(data) {
        const message = el("div", "message assistant");
        const bubble = el("div", "message-bubble", data.response || "I couldn’t generate a response. Please try again.");

        message.append(el("span", "message-label", "AWN"), bubble);

        // Scope + intent tags
        const tags = el("div", "message-tags");
        if (data.scope) {
            const warn = data.scope !== "IN_SCOPE";
            tags.appendChild(el("span", warn ? "tag warn" : "tag", SCOPE_LABELS[data.scope] || data.scope));
        }
        if (data.intent) tags.appendChild(el("span", "tag", prettify(data.intent)));
        if (tags.childNodes.length) message.appendChild(tags);

        // Knowledge sources
        if (Array.isArray(data.sources) && data.sources.length > 0) {
            const box = el("details", "sources-box");
            box.appendChild(el("summary", "", `View sources (${data.sources.length})`));

            data.sources.forEach((source, index) => {
                const item = el("div", "source-item");
                const title = source.title || source.section || source.name || `Knowledge source ${index + 1}`;
                const body = source.content || source.text || source.chunk || "";

                item.appendChild(el("strong", "", title));
                if (body) item.appendChild(el("p", "", body));
                box.appendChild(item);
            });

            message.appendChild(box);
        }

        messagesContainer.appendChild(message);
        scrollToBottom();
    }

    function showTypingIndicator() {
        removeTypingIndicator();
        const message = el("div", "message assistant");
        message.id = "typing-message";

        const bubble = el("div", "message-bubble typing-indicator");
        bubble.setAttribute("aria-label", "AWN is typing");
        for (let i = 0; i < 3; i++) bubble.appendChild(document.createElement("span"));

        message.append(el("span", "message-label", "AWN"), bubble);
        messagesContainer.appendChild(message);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        document.getElementById("typing-message")?.remove();
    }


    // ---------- API ----------

    async function sendMessage(content) {
        if (!content || isWaiting) return;

        setBusy(true);
        startChatMode();
        addUserMessage(content);

        messageInput.value = "";
        updateCharacterCount();
        resizeInput();
        showTypingIndicator();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: content })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(typeof data.detail === "string" ? data.detail : "The server returned an error.");
            }

            removeTypingIndicator();
            addAssistantMessage(data);

        } catch (error) {
            console.error("AWN AI request failed:", error);
            removeTypingIndicator();
            addAssistantMessage({ response: "Sorry, something went wrong while processing your message. Please try again." });

        } finally {
            setBusy(false);
            messageInput.focus();
        }
    }

    async function checkHealth() {
        try {
            const response = await fetch("/health");
            if (!response.ok) throw new Error("unhealthy");
            statusBox.dataset.state = "ok";
            statusText.textContent = "Assistant online";
        } catch {
            statusBox.dataset.state = "down";
            statusText.textContent = "Assistant offline";
        }
    }


    // ---------- Events ----------

    chatForm.addEventListener("submit", (event) => {
        event.preventDefault();
        sendMessage(messageInput.value.trim());
    });

    messageInput.addEventListener("input", () => {
        updateCharacterCount();
        resizeInput();
    });

    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
            event.preventDefault();
            chatForm.requestSubmit();
        }
    });

    // Quick chips and topic cards send their prompt directly
    document.addEventListener("click", (event) => {
        const button = event.target.closest("[data-prompt]");
        if (!button || isWaiting) return;
        sendMessage(button.dataset.prompt);
    });

    // Header navigation: leave the conversation first, then go to the section
    const navLinks = document.querySelectorAll(".site-nav a");

    navLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            if (isWaiting) {
                event.preventDefault();
                return;
            }

            event.preventDefault();

            if (document.body.classList.contains("is-chatting")) {
                endChatMode();
            }

            const target = document.querySelector(link.getAttribute("href"));
            // Wait one frame so the landing sections are visible before scrolling
            requestAnimationFrame(() => {
                target?.scrollIntoView({ behavior: "smooth", block: "start" });
            });

            navLinks.forEach((item) => item.classList.toggle("is-current", item === link));
        });
    });

    newChatButton.addEventListener("click", () => {
        if (isWaiting) return;
        endChatMode();
        messageInput.value = "";
        updateCharacterCount();
        resizeInput();
        window.scrollTo({ top: 0 });
        messageInput.focus();
    });

    document.querySelector(".brand")?.addEventListener("click", (event) => {
        event.preventDefault();
        if (isWaiting) return;
        endChatMode();
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    updateCharacterCount();
    checkHealth();
});
