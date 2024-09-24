import streamlit as st
import openai
import os


# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Change the environment variable name here
openai.api_key = "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"

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Sidebar
st.sidebar.title("Chat History")

if st.sidebar.button("New Chat"):
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Display chat history in sidebar
for i, msg in enumerate(st.session_state['messages'][1:], 1):  # Skip the system message
    if msg['role'] == 'user':
        st.sidebar.text_area(f"You {i}", value=msg['content'], height=50, disabled=True)
    elif msg['role'] == 'assistant':
        st.sidebar.text_area(f"Assistant {i}", value=msg['content'], height=50, disabled=True)

# Main chat interface
st.title("Chatbot")

# Generate a response using OpenAI API
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['messages']
        )
        assistant_response = response.choices[0].message['content']
        st.session_state['messages'].append({"role": "assistant", "content": assistant_response})
        return assistant_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Display chat messages
for message in st.session_state['messages'][1:]:  # Skip the system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is your question?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            st.markdown(response)

# Styling
st.markdown("""
<style>
.stTextInput>div>div>input {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)
