import json
import os


def search_articles(message):

    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "support_articles.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        articles = json.load(file)

    message = message.lower()

    results = []

    for article in articles:

        for keyword in article["keywords"]:

            if keyword.lower() in message:
                results.append(article)
                break

    return results