import os
import requests
from dotenv import load_dotenv

# Load the environment variables from your .env file
load_dotenv()

# Get your API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("🔴 ERROR: Could not find GEMINI_API_KEY in your .env file.")
else:
    print("--- Found API Key. Asking Google for available models... ---\n")
    
    # The URL to list available models
    url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
    
    try:
        # Make the request to the API
        response = requests.get(url)
        response.raise_for_status() # Raise an error for bad status codes
        
        data = response.json()
        
        print("✅ SUCCESS! Your API key has access to the following models:")
        print("==========================================================")
        
        for model in data.get('models', []):
            model_name = model.get('name')
            supported_methods = ", ".join(model.get('supportedGenerationMethods', []))
            
            # We are looking for a model that supports 'generateContent'
            if 'generateContent' in supported_methods:
                print(f"- {model_name}  (Supports: {supported_methods}) <-- USE THIS ONE")
            else:
                print(f"- {model_name}  (Supports: {supported_methods})")

        print("\n==========================================================")
        print("\nACTION: Copy one of the model names marked with 'USE THIS ONE' (like 'models/gemini-pro')")
        print("and paste it into the MODEL_NAME variable in your users/views.py file.")

    except requests.exceptions.HTTPError as e:
        print(f"🔴 HTTP ERROR: {e}")
        print("   This likely means your API key is invalid, or billing is not enabled on your Google Cloud project.")
    except Exception as e:
        print(f"🔴 An unexpected error occurred: {e}")