import json
import os


def get_customer(customer_id):

    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "customers.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        customers = json.load(file)

    for customer in customers:

        if customer["customer_id"] == customer_id:
            return customer

    return None
