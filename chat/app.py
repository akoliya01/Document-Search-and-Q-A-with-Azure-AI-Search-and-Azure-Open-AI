import os
import openai
import requests
from flask import Flask, request, jsonify, render_template
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
app = Flask(__name__)

# Azure Configuration
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
    AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Authentication
search_client = SearchClient(endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/",
                             index_name=AZURE_SEARCH_INDEX,
                             credential=AZURE_SEARCH_KEY)
openai.api_key = AZURE_OPENAI_KEY

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Step 1: Retrieve relevant content from Azure AI Search
    search_results = search_client.search(search_text=user_query, top=3)
    retrieved_texts = [doc['content'] for doc in search_results]
    
    if not retrieved_texts:
        return jsonify({"response": "No relevant information found."})
    
    # Step 2: Construct prompt for OpenAI
    prompt = f"""
    You are an AI assistant. Answer the following question based on the provided company content:
    
    Context:
    {retrieved_texts}
    
    Question: {user_query}
    
    Answer:
    """
    
    # Step 3: Get response from OpenAI
    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    return jsonify({"response": response['choices'][0]['message']['content']})

if __name__ == "__main__":
    app.run(debug=True)

# HTML UI (index.html)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Azure AI Chat</title>
    <script>
        async function askQuestion() {
            let query = document.getElementById("query").value;
            if (!query) {
                alert("Please enter a question");
                return;
            }
            
            let response = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            });
            
            let result = await response.json();
            document.getElementById("response").innerText = result.response;
        }
    </script>
</head>
<body>
    <h1>Azure AI Chat</h1>
    <input type="text" id="query" placeholder="Ask a question...">
    <button onclick="askQuestion()">Ask</button>
    <p id="response"></p>
</body>
</html>
"""

with open("templates/index.html", "w") as f:
    f.write(html_content)
