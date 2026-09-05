const analyzeButton = document.getElementById("analyzeBtn");
const approveButton = document.getElementById("approveBtn");
const escalateButton = document.getElementById("escalateBtn");

console.log("JavaScript loaded");
console.log("Analyze button:", analyzeButton);
console.log("Approve button:", approveButton);
console.log("Escalate button:", escalateButton);


// =====================================================
// ANALYZE MESSAGE
// =====================================================

if (analyzeButton) {

    analyzeButton.addEventListener("click", async function () {

        console.log("ANALYZE BUTTON CLICKED");

        const customerId =
            document.getElementById("customer").value;

        const message =
            document.getElementById("message").value;


        if (message.trim() === "") {

            alert("Please enter a customer message.");

            return;
        }


        // Show customer message
        document.getElementById("customerMessage").textContent =
            message;


        // Show processing status
        document.getElementById("intent").textContent =
            "Analyzing...";

        document.getElementById("decision").textContent =
            "PROCESSING";

        document.getElementById("response").textContent =
            "Gemini is generating a response...";

        document.getElementById("evidence").textContent =
            "Searching knowledge base...";


        try {

            const result = await fetch("/api/analyze", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    customer_id: customerId,
                    message: message
                })

            });


            const data = await result.json();


            if (!result.ok) {

                throw new Error(
                    data.error || "Analysis failed"
                );

            }


            // =================================================
            // CUSTOMER ACCOUNT
            // =================================================

            document.getElementById("accountName").textContent =
                data.customer.name;

            document.getElementById("accountPlan").textContent =
                data.customer.plan;

            document.getElementById("accountService").textContent =
                data.customer.service;

            document.getElementById("accountBilling").textContent =
                data.customer.billing_status;

            document.getElementById("accountStatus").textContent =
                data.customer.account_status;


            // =================================================
            // INTENT
            // =================================================

            if (data.article) {

                document.getElementById("intent").textContent =
                    data.article.category + " Problem";

            } else {

                document.getElementById("intent").textContent =
                    "Unknown Problem";

            }


            // =================================================
            // DECISION
            // =================================================

            document.getElementById("decision").textContent =
                data.decision;


            // =================================================
            // GEMINI RESPONSE
            // =================================================

            document.getElementById("response").textContent =
                data.response || "No response generated.";


            // =================================================
            // KNOWLEDGE BASE EVIDENCE
            // =================================================

            if (data.article) {

                document.getElementById("articleId").textContent =
                    data.article.article_id;

                document.getElementById("articleTitle").textContent =
                    data.article.title;

                document.getElementById("evidence").textContent =
                    data.article.article_id +
                    " — " +
                    data.article.title;

            } else {

                document.getElementById("articleId").textContent =
                    "No Article";

                document.getElementById("articleTitle").textContent =
                    "No matching knowledge base article";

                document.getElementById("evidence").textContent =
                    "No matching knowledge base article found.";

            }


            console.log("Analysis successful");


        } catch (error) {

            console.error("Analysis error:", error);


            document.getElementById("intent").textContent =
                "Error";

            document.getElementById("decision").textContent =
                "ERROR";

            document.getElementById("response").textContent =
                "Error: " + error.message;

            document.getElementById("evidence").textContent =
                "Unable to retrieve knowledge base information.";

        }

    });

}


// =====================================================
// APPROVE & SEND
// =====================================================

if (approveButton) {

    approveButton.addEventListener("click", async function () {

        console.log("APPROVE BUTTON CLICKED");


        const customerId =
            document.getElementById("customer").value;

        const message =
            document.getElementById("message").value;

        const response =
            document.getElementById("response").textContent;


        if (message.trim() === "") {

            alert("Please enter a customer message first.");

            return;
        }


        if (
            response.trim() === "" ||
            response.includes("No response generated") ||
            response.includes("Gemini is generating")
        ) {

            alert("Please analyze the message first.");

            return;
        }


        try {

            const result = await fetch("/api/approve", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    customer_id: customerId,

                    message: message,

                    response: response

                })

            });


            const data = await result.json();


            if (!result.ok) {

                throw new Error(
                    data.error || "Approval failed"
                );

            }


            document.getElementById("decision").textContent =
                "SENT";


            alert(
                "RESPONSE APPROVED & SENT ✅\n\n" +
                "Customer: " +
                data.customer_name +
                "\nCustomer ID: " +
                data.customer_id +
                "\n\nResponse sent successfully."
            );


        } catch (error) {

            console.error("Approval error:", error);

            alert(
                "Approval failed:\n\n" +
                error.message
            );

        }

    });

}


// =====================================================
// ESCALATE
// =====================================================

if (escalateButton) {

    escalateButton.addEventListener("click", async function () {

        console.log("ESCALATE BUTTON CLICKED");


        const customerId =
            document.getElementById("customer").value;

        const message =
            document.getElementById("message").value;

        const decision =
            document.getElementById("decision").textContent;


        if (message.trim() === "") {

            alert("Please enter a customer message first.");

            return;
        }


        try {

            const result = await fetch("/api/escalate", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    customer_id: customerId,

                    message: message,

                    reason:
                        "Issue requires human support. Decision: " +
                        decision

                })

            });


            const data = await result.json();


            if (!result.ok) {

                throw new Error(
                    data.error || "Escalation failed"
                );

            }


            const handoff =
                data.handoff_summary;


            document.getElementById("decision").textContent =
                "ESCALATED";


            alert(

                "ESCALATED TO HUMAN SUPPORT 🚨\n\n" +

                "Customer: " +
                handoff.customer_name +

                "\nCustomer ID: " +
                handoff.customer_id +

                "\nPlan: " +
                handoff.plan +

                "\nService: " +
                handoff.service +

                "\nBilling: " +
                handoff.billing_status +

                "\nAccount: " +
                handoff.account_status +

                "\n\nCustomer Message:\n" +
                handoff.customer_message +

                "\n\nReason:\n" +
                handoff.reason

            );


        } catch (error) {

            console.error("Escalation error:", error);

            alert(
                "Escalation failed:\n\n" +
                error.message
            );

        }

    });

}


// =====================================================
// FINISHED
// =====================================================

console.log(
    "Customer Support Assistant JavaScript loaded successfully."
);