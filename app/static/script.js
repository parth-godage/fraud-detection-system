const form = document.getElementById("fraudForm");

const button = document.getElementById("analyzeBtn");

const result = document.getElementById("result");
const resultIcon = document.getElementById("resultIcon");
const resultTitle = document.getElementById("resultTitle");
const resultMessage = document.getElementById("resultMessage");

const probabilityText =
    document.getElementById("probabilityText");

const probabilityBar =
    document.getElementById("probabilityBar");


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    // Start loading animation
    button.classList.add("loading");

    // Hide previous result
    result.classList.add("hidden");
    result.classList.remove("safe", "danger");

    // Get values
    const transaction = {

        step: Number(
            document.getElementById("step").value
        ),

        type:
            document.getElementById("type").value,

        amount: Number(
            document.getElementById("amount").value
        ),

        oldbalanceOrg: Number(
            document.getElementById("oldbalanceOrg").value
        ),

        oldbalanceDest: Number(
            document.getElementById("oldbalanceDest").value
        )
    };


    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(transaction)
        });


        if (!response.ok) {
            throw new Error("Prediction request failed");
        }


        const data = await response.json();


        // Fraud probability
        const probability =
            Number(data.fraud_probability) * 100;


        // Show result
        result.classList.remove("hidden");


        if (data.prediction === 1) {

            // ================= FRAUD =================

            result.classList.add("danger");

            resultIcon.textContent = "⚠️";

            resultTitle.textContent =
                "Potential Fraud Detected";

            resultMessage.textContent =
                "This transaction shows patterns associated with fraudulent activity.";

        } else {

            // ================= LEGITIMATE =================

            result.classList.add("safe");

            resultIcon.textContent = "✓";

            resultTitle.textContent =
                "Transaction Appears Legitimate";

            resultMessage.textContent =
                "No significant fraud pattern was detected in this transaction.";
        }


        // Probability
        probabilityText.textContent =
            probability.toFixed(1) + "%";


        // Animate progress bar
        probabilityBar.style.width = "0%";

        setTimeout(() => {

            probabilityBar.style.width =
                Math.min(probability, 100) + "%";

        }, 50);


        // Scroll to result
        setTimeout(() => {

            result.scrollIntoView({
                behavior: "smooth",
                block: "nearest"
            });

        }, 150);


    } catch (error) {

        console.error(error);

        result.classList.remove("hidden");

        result.classList.add("danger");

        resultIcon.textContent = "✕";

        resultTitle.textContent =
            "Something went wrong";

        resultMessage.textContent =
            "Unable to connect to the fraud detection service. Please try again.";

        probabilityText.textContent = "—";

        probabilityBar.style.width = "0%";

    } finally {

        button.classList.remove("loading");

    }

});