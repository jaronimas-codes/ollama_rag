from query_data import query_rag
from sentence_transformers import SentenceTransformer, util

# Load the Sentence Transformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function for semantic evaluation
def semantic_evaluate_response(expected: str, actual: str) -> bool:
    """Evaluate the response using semantic similarity."""
    # Generate embeddings for both expected and actual responses
    expected_embedding = model.encode(expected, convert_to_tensor=True)
    actual_embedding = model.encode(actual, convert_to_tensor=True)

    # Compute cosine similarity between the two embeddings
    similarity_score = util.pytorch_cos_sim(expected_embedding, actual_embedding)

    # Define a similarity threshold (adjust as necessary)
    return similarity_score.item() > 0.5  # You can adjust this threshold

# Modify the query_and_validate function to use semantic similarity
def query_and_validate(question: str, expected_response: str):
    """Queries the RAG system and evaluates the actual response using semantic similarity."""
    # Query the RAG system for the answer
    response_text, sources = query_rag(question)

    # Use semantic similarity for evaluation
    is_match = semantic_evaluate_response(expected_response, response_text)
    
    return {
        "result": is_match,
        "actual_response": response_text,
        "sources": sources  # Return the sources
    }


# Test cases for The Journey of Cocoa to Europe
def cocoa_questions():
    return [
        # {
        #     "question": "Where did the cocoa plant originate from? (Answer with the region only)",
        #     "expected_response": "Central and Equatorial America"
        # },
        {
            "question": "What was cocoa used for by the Mayans and Aztecs?",
            "expected_response": "As a drink for religious or martial ceremonies and as currency"
        },
        # {
        #     "question": "When did Europeans first encounter cocoa?",
        #     "expected_response": "During Christopher Columbus's fourth journey to America in 1502"
        # },
        # {
        #     "question": "What changes were made to cocoa when it was brought to Europe?",
        #     "expected_response": "Sugar was added, and it was consumed hot"
        # },
        # {
        #     "question": "What role did cocoa play in European courts?",
        #     "expected_response": "It was a luxury drink consumed by the nobility"
        # },
        # {
        #     "question": "Which people are credited with the invention of the cocoa drink?",
        #     "expected_response": "The Olmecs"
        # }
    ]


# Test cases for Space: The New Frontier
def space_questions():
    return [
        # {
        #     "question": "What is the purpose of the Space: The New Frontier Educator's Guide?",
        #     "expected_response": "To provide hands-on activities for elementary and middle school students"
        # },
        {
            "question": "What are two key concepts covered in the activities of Space: The New Frontier?",
            "expected_response": "How gravity works and what makes something stay in orbit"
        },
        # {
        #     "question": "What is one challenge included in the space activities?",
        #     "expected_response": "Build a rocket from a straw and a plane from a piece of paper"
        # },
        # {
        #     "question": "What major hazard do astronauts face when leaving Earth’s atmosphere?",
        #     "expected_response": "Radiation"
        # },
        # {
        #     "question": "What happened on February 22, 2024, related to space exploration?",
        #     "expected_response": "The first lunar landing by a U.S.-built spacecraft since Apollo 17"
        # }
    ]


# Helper function to run tests and display results
def run_tests(questions):
    for q in questions:
        print(f"**Question:** {q['question']}")
        print(f"**Expected Answer:** {q['expected_response']}")
        
        # Run the query and validation
        result = query_and_validate(q['question'], q['expected_response'])

        print(f"**Actual Answer:** {result['actual_response']}")
        # print(f"Sources: {result.get('sources', 'No sources available')}")
        print("\nTest Passed" if result['result'] else "Test Failed")
        print("\n")


if __name__ == "__main__":
    # Run test cases for Cocoa Journey
    # print("Running Cocoa Journey Test Cases...")
    run_tests(cocoa_questions())

    # Run test cases for Space: The New Frontier
    # print("Running Space Frontier Test Cases...")
    run_tests(space_questions())
