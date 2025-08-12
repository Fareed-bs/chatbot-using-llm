import google.generativeai as genai
import os
import streamlit as st

st.title("Chatbot with the Gemini model")

# Get your API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Configure the API key for Gemini
genai.configure(api_key=api_key)

# Create a model instance
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# Define a function to generate a response


def generate_response(user_prompt):
    response = model.generate_content(user_prompt)
    return response.text


# Create a text input box with a default placeholder
user_prompt = st.text_input("User: ")

if st.button("Submit"):
    output = generate_response(user_prompt)
    st.write("Assistant:", output)
