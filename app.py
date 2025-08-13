import google.generativeai as genai
import os
import streamlit as st
import pymongo


myclient = pymongo.MongoClient(
    "mongodb://localhost:27017/")  # Set up MongoDB connection

mydb = myclient["chatbot_db"]  # Create a db

# Create a collection to store conversations
mycol = mydb["store_conversations"]


# Set up the Streamlit app
st.title("Chatbot with the Gemini model")
st.subheader("How can I assist you today?")

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
    with st.spinner(text="Generating..."):
        output = generate_response(user_prompt)
        st.write("Assistant:", output)

    # Create a conversation document
    conversation = {
        "user": user_prompt,
        "assistant": output
    }

    # Insert the conversation into the MongoDB collection
    mycol.insert_one(conversation)

# Chat history
st.sidebar.title("Chat History")

# Fetch all conversations from the database
history = list(mycol.find({}, {"_id": 1, "user": 1}))

# Create a list of options for the selectbox.
# We'll use the user's prompt as the label for readability.
history_options = {f"{conv['user'][:50]}...": conv["_id"] for conv in history}

selected_option_label = st.sidebar.selectbox(
    "Select a conversation to view",
    options=history_options.keys()
)

# If an option is selected, find and display the full conversation
if selected_option_label:
    selected_id = history_options[selected_option_label]
    conversation_to_display = mycol.find_one({"_id": selected_id})
    st.sidebar.write("User:", conversation_to_display["user"])
    st.sidebar.write("Assistant:", conversation_to_display["assistant"])
