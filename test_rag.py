from query_data import query_rag
from langchain_ollama import OllamaLLM

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

def query_and_validate(question: str, expected_response: str):
    # Query the RAG system
    response_text = query_rag(question)
    
    # Format evaluation prompt
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    # Initialize the Ollama model for evaluation
    model = OllamaLLM(model="llama3.2:1b", 
                      temperature=0.2,
                      max_tokens=200,        # Limit the response
                      top_p=0.9 )
    # Optional: Nucleus sampling to focus on likely tokens)
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    # Return true or false based on the evaluation
    if "true" in evaluation_results_str_cleaned:
        return {"result": True, "actual_response": response_text}
    elif "false" in evaluation_results_str_cleaned:
        return {"result": False, "actual_response": response_text}
    else:
        raise ValueError(f"Invalid evaluation result: {evaluation_results_str_cleaned}")

# Test cases for The Journey of Cocoa to Europe
def cocoa_questions():
    return [
        {
            "question": "Where did the cocoa plant originate from? (Answer with the region only)",
            "expected_response": "Central and Equatorial America"
        },
        {
            "question": "What was cocoa used for by the Mayans and Aztecs?",
            "expected_response": "As a drink for religious or martial ceremonies and as currency"
        },
        {
            "question": "When did Europeans first encounter cocoa?",
            "expected_response": "During Christopher Columbus's fourth journey to America in 1502"
        },
        {
            "question": "What changes were made to cocoa when it was brought to Europe?",
            "expected_response": "Sugar was added, and it was consumed hot"
        },
        {
            "question": "What role did cocoa play in European courts?",
            "expected_response": "It was a luxury drink consumed by the nobility"
        },
        {
            "question": "Which people are credited with the invention of the cocoa drink?",
            "expected_response": "The Olmecs"
        }
    ]

# Test cases for Space: The New Frontier
def space_questions():
    return [
        # {
        #     "question": "What is the purpose of the Space: The New Frontier Educator's Guide?",
        #     "expected_response": "To provide hands-on activities for elementary and middle school students"
        # },
        # {
        #     "question": "What are two key concepts covered in the activities of Space: The New Frontier?",
        #     "expected_response": "How gravity works and what makes something stay in orbit"
        # },
        # {
        #     "question": "What is one challenge included in the space activities?",
        #     "expected_response": "Build a rocket from a straw and a plane from a piece of paper"
        # },
        # {
        #     "question": "What major hazard do astronauts face when leaving Earth’s atmosphere?",
        #     "expected_response": "Radiation"
        # },
        {
            "question": "What happened on February 22, 2024, related to space exploration?",
            "expected_response": "The first lunar landing by a U.S.-built spacecraft since Apollo 17"
        }
    ]
