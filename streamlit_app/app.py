import streamlit as st
import requests

# Inject custom CSS for chat styling
st.markdown("""
    <style>
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        font-size: 16px;
        line-height: 1.5;
    }
    .user-bubble {
        background-color: #e8f0fe;
        color: #1a73e8;
        text-align: left;
        max-width: 70%;
        margin-left: auto;
        margin-right: 0;
    }
    .response-bubble {
        background-color: #f1f3f4;
        color: #202124;
        text-align: left;
        max-width: 70%;
        margin-right: auto;
        margin-left: 0;
    }
    .button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for query-response history
if "history" not in st.session_state:
    st.session_state.history = []

# Main application
st.title("🤖 LLM-based RAG Search")

# Sidebar for additional info
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- 💡 Enter your query to retrieve an answer from the RAG system.
- 📡 Ensure your backend is running for proper results.
""")

# Display query-response history in the sidebar
st.sidebar.subheader("Query History")
for idx, entry in enumerate(st.session_state.history):
    with st.sidebar.expander(f"Query {idx + 1}: {entry['query']}", expanded=False):
        st.write(entry["answer"])

# Input for user query
query = st.text_input("Enter your query:", placeholder="Type your question here...")

# Trigger search when the user clicks the button
if st.button("Search", key="search", help="Click to search"):
    if query:  # Ensure there's a query input before proceeding
        try:
            # Make a POST request to the Flask API with the user's query
            flask_url = "http://localhost:5001/query"  # Update this with your Flask server URL if different
            response = requests.post(flask_url, json={"query": query})

            # Check the response status
            if response.status_code == 200:
                # If the request is successful, extract and display the generated answer
                answer = response.json().get('answer', "No answer received.")
                
                # Display user query and response as chat bubbles
                st.markdown(f'<div class="chat-bubble user-bubble">{query}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-bubble response-bubble">{answer}</div>', unsafe_allow_html=True)

                # Add query and response to session state history
                st.session_state.history.append({"query": query, "answer": answer})
            else:
                # Handle error if the response status code is not 200
                st.error(f"Error: {response.status_code}, Unable to retrieve the answer.")
        except Exception as e:
            # Handle any exceptions that may occur during the request
            st.error(f"An error occurred while accessing the backend: {e}")
    else:
        st.warning("Please enter a query before searching.")
