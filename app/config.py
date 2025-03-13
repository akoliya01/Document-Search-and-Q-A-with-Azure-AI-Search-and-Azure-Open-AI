class Config:
AZURE_SEARCH_SERVICE = "<Name of Azure AI Search>"  # e.g., mysearchservice
AZURE_SEARCH_INDEX = "<Name of indexes you created in AI search>"  # e.g., companydocs
AZURE_OPENAI_ENDPOINT = "<Endpoint URL for Azure Open AI>"
AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"  # Your deployed model name
AZURE_SEARCH_KEY = "<Key of Azure search>"  # Azure Search API Key
AZURE_OPENAI_KEY = "<Key of Azure Open AI>"  # Azure OpenAI API Key



# import os

# class Config:
#     SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
#     SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
#     SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")
#     OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")