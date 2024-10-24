import streamlit as st
import time
from query_data import query_rag  # Reuse the query_rag function from query_data.py
from test_rag import cocoa_questions, space_questions, query_and_validate  # Reuse test cases from test_rag.py

# Streamlit App UI
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Query Data", "Test RAG"])

    if page == "Query Data":
        display_query_page()
    elif page == "Test RAG":
        display_test_page()

# Page for querying data
def display_query_page():
    st.title("RAG Query Interface")
    query_text = st.text_input("Enter your query", placeholder="Type your question here...")
    
    if st.button("Submit Query"):
        if query_text:
            with st.spinner('Querying the RAG system...'):
                response = query_rag(query_text)
            st.subheader("Response")
            st.write(response)
        else:
            st.warning("Please enter a query text to submit!")

# Page for running the tests
def display_test_page():
    st.title("Test RAG")
    
    test_suite = st.selectbox("Select Test Suite", ["Cocoa Journey", "Space Frontier"])
    
    if st.button("Run Test Cases"):
        if test_suite == "Cocoa Journey":
            st.write("Running Cocoa Journey Test Cases...")
            run_tests(cocoa_questions())
        elif test_suite == "Space Frontier":
            st.write("Running Space Frontier Test Cases...")
            run_tests(space_questions())

# Helper function to run tests and display results
def run_tests(questions):
    for q in questions:
        st.write(f"**Question:** {q['question']}")
        st.write(f"**Expected Answer:** {q['expected_response']}")
        
        # Show a spinner while the test is running
        with st.spinner(f"Running test for question: {q['question']}"):
            # Start timer to measure the query time
            start_time = time.time()
            
            # Run the query and validation
            result = query_and_validate(q['question'], q['expected_response'])
            
            # End timer
            end_time = time.time()
            time_taken = end_time - start_time
            
        # Display the response and additional info
        st.write(f"**Response:** {result['actual_response']}")
        st.write(f"Sources: {result.get('sources', 'No sources available')}")
        st.write(f"Time taken: {time_taken:.2f} seconds")
        
        # Show pass/fail result
        if result['result']:
            st.success("Test Passed")
        else:
            st.error("Test Failed")

if __name__ == "__main__":
    main()
