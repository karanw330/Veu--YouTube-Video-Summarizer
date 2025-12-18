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
        hidden.scrollIntoView({ behavior: "smooth" });

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
                                <div class="message-avatar"><img src="static/img_2.png" style="position:relative;top:15px;" class="ai-avatar"></div>
                                <div class="message-content">
                                    ${data}
                                    <div class="message-timestamp">10:31 AM</div>
                                </div>
                            </div>`;
             hidden.insertAdjacentHTML("beforebegin",new_message);
             hidden.scrollIntoView({ behavior: "smooth" });
         })

        document.getElementById("user_message").value = "";
    }

    const socket = new WebSocket('ws://localhost:8765');

    socket.onopen= function(event){
        console.log("Online")
    }

    socket.onmessage=(event)=>{
        console.log(event.data);
}

    socket.onclose = function(event){
        console.log("Connection closed")
}

    window.addEventListener("keydown", function (event)
{
    if (event.key === 'Enter') {
        event.preventDefault();
        user_message();
    }
});