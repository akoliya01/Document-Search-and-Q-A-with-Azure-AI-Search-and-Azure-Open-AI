import os
from flask import Flask, Blueprint, render_template, request
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from config import Config


app = Flask(__name__)

bp = Blueprint('main', __name__)


# Initialize Azure AI Search client
search_client = SearchClient(
    endpoint=Config.AZURE_SEARCH_ENDPOINT,
    index_name=Config.AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(Config.AZURE_SEARCH_KEY)
)

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
    api_key=Config.AZURE_OPENAI_KEY,
    api_version="2023-05-15"
)

def search_and_respond(query):
    try:
        # Search documents in Azure AI Search
        results = search_client.search(search_text=query, top=3)
        context = "\n".join([doc["content"] for doc in results if "content" in doc])

        if not context:
            return "No relevant information found."

        # Generate response with Azure OpenAI
        prompt = f"Based on the following information:\n{context}\nAnswer the question: {query}"
        response = openai_client.chat.completions.create(
            model="gpt-35-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@bp.route("/", methods=["GET", "POST"])
def index():
    answer = None
    query = None
    if request.method == "POST":
        query = request.form["query"]
        answer = search_and_respond(query)
    return render_template("index.html", answer=answer, query=query)

# Register Blueprint
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
