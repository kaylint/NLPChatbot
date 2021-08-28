/** --------------
   RUN WHEN LOADED
 ----------------- */

document.addEventListener("DOMContentLoaded", function() {
    updateSendButtonDisabledState();
    toggleSendButtonDisabledStateOnMessageInputInput();
    makeExternalCallWhenFormSubmits();
});

/** --------------
   EVENT LISTENERS
 ----------------- */

function toggleSendButtonDisabledStateOnMessageInputInput() {
    const messageInput = getMessageInputElement();
    messageInput.addEventListener("input", updateSendButtonDisabledState, false);
}

function makeExternalCallWhenFormSubmits() {
    const phoneForm = getPhoneFormElement();
    const messageInput = getMessageInputElement();

    phoneForm.addEventListener("submit", function(event) {
        event.preventDefault();
        event.stopPropagation();

        console.log("submitted");

        const messageInputValue = messageInput.value;
        addToChat(messageInputValue, "ours");
        clearMessageInput();

        fetch("/send-message", {
                method: "POST",
                headers: { "Content-Type": "application/json; charset=utf-8" },
                body: JSON.stringify({ message: messageInputValue }),
            })
            .then(function(response) {
                return response.text().then(function(responsetext) {
                    console.log(responsetext);
                    addToChat(responsetext, "theirs");
                })
            })
            .catch(function(response) {
                console.error(response);
                addToChat(response, "error");
            });
    });
}

/** --------------
   ELEMENT GETTERS
 ----------------- */

function getChatHistoryElement() {
    return document.querySelector(".chat-history");
}

function getPhoneFormElement() {
    return document.querySelector(".phone-outline");
}

function getMessageInputElement() {
    return document.querySelector("#message-input");
}

function getSendButtonElement() {
    return document.querySelector(".send-button");
}

/** --------------
   HELPER FUNCTIONS
 ----------------- */

function updateSendButtonDisabledState() {
    const messageInput = getMessageInputElement();
    const message = (messageInput.value || "").trim();

    if (message.length <= 0) {
        disableSendButton();
        return;
    }

    enableSendButton();
}

function disableSendButton() {
    const sendButtonelement = getSendButtonElement();
    sendButtonelement.setAttribute("disabled", true);
}

function enableSendButton() {
    const sendButtonelement = getSendButtonElement();
    sendButtonelement.removeAttribute("disabled");
}

function addToChat(message, oursTheirs) {
    const chatHistory = getChatHistoryElement();

    const newChatBubble = document.createElement("p");
    newChatBubble.classList.add("chat-bubble");
    newChatBubble.classList.add(oursTheirs);
    newChatBubble.textContent = message;

    const newNode = chatHistory.appendChild(newChatBubble);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    return newNode;
}

function clearMessageInput() {
    const messageInput = getMessageInputElement();
    messageInput.value = "";
    updateSendButtonDisabledState();
}