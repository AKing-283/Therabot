document.addEventListener("DOMContentLoaded", () => {

    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("message");

    // -----------------------------
    // ADD MESSAGE TO CHAT
    // -----------------------------
    function addMessage(sender, text, messageId = null) {
        const wrapper = document.createElement("div");
        wrapper.classList.add("msg");

        let html = `
            <p><b>${sender === "user" ? "You" : "Therabot"}:</b> ${text}</p>
        `;

        // Feedback only for bot messages
        if (sender === "bot" && messageId) {
            html += `
                <div class="feedback">
                    <button onclick="sendFeedback(${messageId}, 'positive')">👍</button>
                    <button onclick="sendFeedback(${messageId}, 'negative')">👎</button>
                </div>
            `;
        }

        wrapper.innerHTML = html;
        chatBox.appendChild(wrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // -----------------------------
    // SEND MESSAGE
    // -----------------------------
    window.sendMessage = async function () {

        let msg = input.value.trim();
        if (!msg) return;

        addMessage("user", msg);
        input.value = "";

        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg })
            });

            const data = await res.json();

            addMessage("bot", data.bot_reply, data.message_id);

        } catch (err) {
            addMessage("bot", "Error connecting to server ❌");
        }
    };


    // -----------------------------
    // FEEDBACK SYSTEM (COMPLETE LOOP)
    // -----------------------------
    window.sendFeedback = async function (messageId, value) {

        // 👍 correct prediction
        if (value === "positive") {

            await fetch("/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message_id: messageId,
                    correct_emotion: "correct"
                })
            });

            alert("Thanks for feedback 👍");
            return;
        }

        // 👎 incorrect prediction → ask correct emotion
        if (value === "negative") {

            const correctEmotion = prompt(
                "Enter correct emotion (happy, sad, anger, fear, neutral):"
            );

            if (!correctEmotion) return;

            await fetch("/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message_id: messageId,
                    correct_emotion: correctEmotion
                })
            });

            alert("Correct emotion saved 👍");
        }
    };


    // -----------------------------
    // LOAD METRICS DASHBOARD
    // -----------------------------
    async function loadMetrics() {
        try {
            const res = await fetch("/metrics");
            const data = await res.json();

            document.getElementById("acc").innerText = data.accuracy || "-";
            document.getElementById("f1").innerText = data.f1_score || "-";
            document.getElementById("time").innerText = data.last_trained || "-";
            document.getElementById("feedback").innerText = data.feedback_used || "-";

        } catch (e) {
            console.error("Metrics load error", e);
        }
    }

    loadMetrics();
    setInterval(loadMetrics, 5000);


    // -----------------------------
    // RETRAIN MODEL
    // -----------------------------
    window.retrainModel = async function () {

        const loader = document.getElementById("loader");
        loader.style.display = "block";

        const oldMetrics = await fetch("/metrics").then(r => r.json());
        const oldAcc = oldMetrics.accuracy || 0;

        try {
            const res = await fetch("/retrain", { method: "POST" });
            const data = await res.json();

            loader.style.display = "none";

            alert(
                `✅ Retrained Successfully!\n\nOld Accuracy: ${oldAcc}\nNew Accuracy: ${data.accuracy}`
            );

            loadMetrics();

        } catch (err) {
            loader.style.display = "none";
            alert("❌ Retrain failed");
        }
    };

});