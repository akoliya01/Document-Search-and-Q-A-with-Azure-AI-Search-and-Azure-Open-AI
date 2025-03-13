import os
from dotenv import load_dotenv
load_dotenv()

AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
print("AZURE_SEARCH_KEY:", AZURE_SEARCH_KEY)
print("Type:", type(AZURE_SEARCH_KEY))