from flask import Flask, render_template, request, jsonify

from src.customer_service import get_customer
from src.knowledge_base import search_articles
from src.decision_engine import make_decision
from src.gemini_service import generate_response

import json
import os
from datetime import datetime


app = Flask(__name__)


# =========================================================
# SAVE TICKET
# =========================================================

def save_ticket(ticket):

    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "tickets.json"
    )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            tickets = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        tickets = []


    tickets.append(ticket)


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tickets,
            file,
            indent=4
        )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# ANALYZE CUSTOMER MESSAGE
# =========================================================

@app.route("/api/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400


    customer_id = data.get("customer_id")

    message = data.get("message")


    if not customer_id or not message:

        return jsonify({
            "error": "Customer ID and message are required"
        }), 400


    # -----------------------------------------------------
    # GET CUSTOMER
    # -----------------------------------------------------

    customer = get_customer(customer_id)


    if customer is None:

        return jsonify({
            "error": "Customer not found"
        }), 404


    # -----------------------------------------------------
    # SEARCH KNOWLEDGE BASE
    # -----------------------------------------------------

    articles = search_articles(message)


    # -----------------------------------------------------
    # DECISION ENGINE
    # -----------------------------------------------------

    decision = make_decision(
        message,
        articles,
        customer
    )


    # Get first matching article

    article = (
        articles[0]
        if articles
        else None
    )


    # -----------------------------------------------------
    # GEMINI RESPONSE
    # -----------------------------------------------------

    ai_response = None


    if article is not None:

        try:

            ai_response = generate_response(
                message,
                customer,
                article
            )

        except Exception as error:

            print(
                "Gemini Error:",
                error
            )

            ai_response = (
                "Unable to generate AI response. "
                "Human support may be required."
            )


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return jsonify({

        "customer": customer,

        "decision": decision,

        "response": ai_response,

        "article": article

    })


# =========================================================
# APPROVE & SEND
# =========================================================

@app.route("/api/approve", methods=["POST"])
def approve():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "No data received"
        }), 400


    customer_id = data.get(
        "customer_id"
    )

    message = data.get(
        "message"
    )

    response = data.get(
        "response"
    )


    if not customer_id or not response:

        return jsonify({

            "error":
            "Customer ID and response are required"

        }), 400


    # -----------------------------------------------------
    # GET CUSTOMER
    # -----------------------------------------------------

    customer = get_customer(
        customer_id
    )


    if customer is None:

        return jsonify({
            "error": "Customer not found"
        }), 404


    # -----------------------------------------------------
    # CREATE TICKET
    # -----------------------------------------------------

    ticket = {

        "ticket_id":
            "TICKET-" +
            datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            ),

        "customer_id":
            customer_id,

        "customer_name":
            customer["name"],

        "message":
            message,

        "response":
            response,

        "decision":
            "RESOLVE",

        "status":
            "CLOSED",

        "created_at":
            datetime.now().isoformat()

    }


    # -----------------------------------------------------
    # SAVE TICKET
    # -----------------------------------------------------

    save_ticket(ticket)


    # -----------------------------------------------------
    # SEND SUCCESS RESPONSE
    # -----------------------------------------------------

    return jsonify({

        "success":
            True,

        "status":
            "SENT",

        "message":
            "Response approved and sent successfully.",

        "customer_id":
            customer_id,

        "customer_name":
            customer["name"],

        "original_message":
            message,

        "response":
            response,

        "ticket_id":
            ticket["ticket_id"]

    })


# =========================================================
# ESCALATE TO HUMAN SUPPORT
# =========================================================

@app.route("/api/escalate", methods=["POST"])
def escalate():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "No data received"
        }), 400


    customer_id = data.get(
        "customer_id"
    )

    message = data.get(
        "message"
    )

    reason = data.get(
        "reason"
    )


    if not customer_id or not message:

        return jsonify({

            "error":
            "Customer ID and message are required"

        }), 400


    # -----------------------------------------------------
    # GET CUSTOMER
    # -----------------------------------------------------

    customer = get_customer(
        customer_id
    )


    if customer is None:

        return jsonify({
            "error": "Customer not found"
        }), 404


    # -----------------------------------------------------
    # HANDOFF SUMMARY
    # -----------------------------------------------------

    handoff_summary = {

        "customer_id":
            customer_id,

        "customer_name":
            customer["name"],

        "plan":
            customer["plan"],

        "service":
            customer["service"],

        "billing_status":
            customer["billing_status"],

        "account_status":
            customer["account_status"],

        "customer_message":
            message,

        "reason":
            reason
            or
            "Human support required"

    }


    # -----------------------------------------------------
    # CREATE ESCALATION TICKET
    # -----------------------------------------------------

    ticket = {

        "ticket_id":
            "TICKET-" +
            datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            ),

        "customer_id":
            customer_id,

        "customer_name":
            customer["name"],

        "message":
            message,

        "decision":
            "ESCALATE",

        "status":
            "OPEN",

        "reason":
            reason
            or
            "Human support required",

        "created_at":
            datetime.now().isoformat()

    }


    # -----------------------------------------------------
    # SAVE TICKET
    # -----------------------------------------------------

    save_ticket(ticket)


    # -----------------------------------------------------
    # RETURN ESCALATION RESULT
    # -----------------------------------------------------

    return jsonify({

        "success":
            True,

        "status":
            "ESCALATED",

        "message":
            "Customer has been escalated to human support.",

        "handoff_summary":
            handoff_summary,

        "ticket_id":
            ticket["ticket_id"]

    })


# =========================================================
# TICKET HISTORY
# =========================================================

@app.route("/api/tickets", methods=["GET"])
def get_tickets():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "tickets.json"
    )


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            tickets = json.load(file)


    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):

        tickets = []


    return jsonify({

        "success":
            True,

        "tickets":
            tickets

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        port=8000

    )