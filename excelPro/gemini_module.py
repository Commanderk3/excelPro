import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the Generative AI client with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Default generation configuration
default_generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Function to create a generative model
def create_model(model_name="gemini-1.5-flash", generation_config=default_generation_config, system_instruction="You are an office employee and your job is to convert texts into a python dictionary format. The second row data should correspond to the first row, therefor use inverted commas to denote corresponding dataset if you find multiple datas. Use doble quotation mark. Dont give the formated string in md"):
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_instruction,
    )

# Function to start a chat session and send a message
def send_message(model, message="", history=[]):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(message)
    return response.text
