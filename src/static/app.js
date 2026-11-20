
/*
=========================================
AWN AI — Application Logic
=========================================
*/

document.addEventListener("DOMContentLoaded", () => {

    // DOM Elements
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const messagesContainer = document.getElementById("messages");
    const sendButton = document.getElementById("send-button");
    const newChatButton = document.getElementById("new-chat-button");
    const characterCount = document.getElementById("character-count");

    // Preserve the original welcome screen
    const welcomeTemplate = document
        .getElementById("empty-chat")
        ?.cloneNode(true);

    let isWaiting = false;


    // =====================================
    // Helpers
    // =====================================

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }


    function createElement(tag, className, text = "") {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        if (text) {
            element.textContent = text;
        }

        return element;
    }


    function updateCharacterCount() {
        const currentLength = messageInput.value.length;
        characterCount.textContent = `${currentLength} / 2000`;
    }


    function hideWelcome() {
        const emptyChat = document.getElementById("empty-chat");

        if (emptyChat) {
            emptyChat.remove();
        }
    }


    function showWelcome() {
        if (!welcomeTemplate) {
            return;
        }

        messagesContainer.replaceChildren(
            welcomeTemplate.cloneNode(true)
        );
    }


    // =====================================
    // User Messages
    // =====================================

    function addUserMessage(content) {

        hideWelcome();

        const message = createElement("div", "message user");

        const label = createElement(
            "span",
            "message-label",
            "You"
        );

        const bubble = createElement(
            "div",
            "message-bubble",
            content
        );

        message.appendChild(label);
        message.appendChild(bubble);

        messagesContainer.appendChild(message);

        scrollToBottom();
    }


    // =====================================
    // Assistant Messages
    // =====================================

    function addAssistantMessage(data) {

        const message = createElement("div", "message assistant");

        const label = createElement(
            "span",
            "message-label",
            "AWN Assistant"
        );

        const bubble = createElement("div", "message-bubble");

        const responseText =
            data.response ||
            "I couldn't generate a response. Please try again.";

        bubble.textContent = responseText;

        message.appendChild(label);
        message.appendChild(bubble);


        // Scope Status
        if (data.scope) {

            const statusLabels = {
                IN_SCOPE: "Within service scope",
                OUT_OF_SCOPE: "Outside service scope",
                UNCLEAR_SCOPE: "Needs clarification"
            };

            const status = createElement(
                "span",
                "message-status",
                statusLabels[data.scope] || data.scope
            );

            message.appendChild(status);
        }


        // Knowledge Sources
        if (Array.isArray(data.sources) && data.sources.length > 0) {

            const sourcesBox = createElement("details", "sources-box");

            const summary = createElement(
                "summary",
                "",
                `View sources (${data.sources.length})`
            );

            sourcesBox.appendChild(summary);

            data.sources.forEach((source, index) => {

                const sourceItem = createElement(
                    "div",
                    "source-item"
                );

                const sourceTitle =
                    source.title ||
                    source.section ||
                    source.name ||
                    `Knowledge source ${index + 1}`;

                const sourceContent =
                    source.content ||
                    source.text ||
                    source.chunk ||
                    "";

                const title = createElement(
                    "strong",
                    "",
                    sourceTitle
                );

                sourceItem.appendChild(title);

                if (sourceContent) {

                    const content = createElement(
                        "p",
                        "",
                        sourceContent
                    );

                    sourceItem.appendChild(content);
                }

                sourcesBox.appendChild(sourceItem);
            });

            bubble.appendChild(sourcesBox);
        }


        messagesContainer.appendChild(message);

        scrollToBottom();
    }


    // =====================================
    // Typing Indicator
    // =====================================

    function showTypingIndicator() {

        removeTypingIndicator();

        const message = createElement(
            "div",
            "message assistant"
        );

        message.id = "typing-message";

        const label = createElement(
            "span",
            "message-label",
            "AWN Assistant"
        );

        const bubble = createElement(
            "div",
            "message-bubble typing-indicator"
        );

        for (let i = 0; i < 3; i++) {
            bubble.appendChild(
                document.createElement("span")
            );
        }

        message.appendChild(label);
        message.appendChild(bubble);

        messagesContainer.appendChild(message);

        scrollToBottom();
    }


    function removeTypingIndicator() {

        const typingMessage = document.getElementById(
            "typing-message"
        );

        if (typingMessage) {
            typingMessage.remove();
        }
    }


    // =====================================
    // API Request
    // =====================================

    async function sendMessage(content) {

        if (!content || isWaiting) {
            return;
        }

        isWaiting = true;

        sendButton.disabled = true;
        messageInput.disabled = true;

        addUserMessage(content);

        messageInput.value = "";

        updateCharacterCount();

        messageInput.style.height = "auto";

        showTypingIndicator();

        try {

            // Give the browser time to display the typing indicator
            await new Promise(resolve => setTimeout(resolve, 300));


            const response = await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: content
                })

            });


            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail || "The server returned an error."
                );
            }

            addAssistantMessage(data);


        } catch (error) {

            console.error("AWN AI request failed:", error);

            addAssistantMessage({

                response:
                    "I'm sorry, something went wrong while processing your message."

            });

        } finally {

            removeTypingIndicator();

            isWaiting = false;

            sendButton.disabled = false;
            messageInput.disabled = false;

            messageInput.focus();
        }
    }


    // =====================================
    // Form Submission
    // =====================================

    chatForm.addEventListener("submit", (event) => {

        event.preventDefault();

        const content = messageInput.value.trim();

        if (!content || isWaiting) {
            return;
        }

        sendMessage(content);
    });


    // =====================================
    // Character Counter
    // =====================================

    messageInput.addEventListener("input", () => {

        updateCharacterCount();

        messageInput.style.height = "auto";

        messageInput.style.height =
            Math.min(messageInput.scrollHeight, 110) + "px";
    });


    // =====================================
    // Keyboard Shortcuts
    // =====================================

    messageInput.addEventListener("keydown", (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey &&
            !event.isComposing
        ) {

            event.preventDefault();

            chatForm.requestSubmit();
        }
    });


    // =====================================
    // Quick Actions — Event Delegation
    // =====================================

    messagesContainer.addEventListener("click", (event) => {

        const button = event.target.closest(".suggestion-item");

        if (!button || isWaiting) {
            return;
        }

        const prompt = button.dataset.prompt;

        if (!prompt) {
            return;
        }

        messageInput.value = prompt;

        updateCharacterCount();

        chatForm.requestSubmit();
    });


    // =====================================
    // New Conversation
    // =====================================

    newChatButton.addEventListener("click", () => {

        if (isWaiting) {
            return;
        }

        showWelcome();

        messageInput.value = "";

        updateCharacterCount();

        messageInput.style.height = "auto";

        messageInput.focus();

        scrollToBottom();
    });


    // =====================================
    // Initialization
    // =====================================

    updateCharacterCount();

    console.log(
        "AWN AI interface initialized successfully."
    );

});
