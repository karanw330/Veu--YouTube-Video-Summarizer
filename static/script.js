function user_message(){
        let message = document.getElementById("user_message").value;
        const hidden = document.getElementById("hidden");
        let new_message = `  <div class="message user-message">
                                <div class="message-avatar">U</div>
                                <div class="message-content">
                                    ${message}
                                    <div class="message-timestamp">10:31 AM</div>
                                </div>
                            </div>`;
        hidden.insertAdjacentHTML("beforebegin",new_message);

        fetch("/response", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body:
        `input=${encodeURIComponent(message)}&`
        })
        .then(response => response.json())
        .then(data => {
             const hidden = document.getElementById("hidden");
             let new_message = `<div class="message ai-message">
                                <div class="message-avatar"><img src="static/img_2.png" class="ai-avatar"></div>
                                <div class="message-content">
                                    ${data}
                                    <div class="message-timestamp">10:31 AM</div>
                                </div>
                            </div>`;
             hidden.insertAdjacentHTML("beforebegin",new_message);
             new_message.scrollIntoView(false);
         })

        document.getElementById("user_message").value = "";
    }