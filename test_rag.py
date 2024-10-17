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
    model = OllamaLLM(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    # Print prompt for debugging
    print(prompt)

    # Return true or false based on the evaluation
    if "true" in evaluation_results_str_cleaned:
        # Print response in green if correct
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in red if incorrect
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )

# Test case 1: Monopoly rules
def test_monopoly_rules():
    # Original question
    assert query_and_validate(
        question="How much total money does a player start with in Monopoly? (Answer with the number only)",
        expected_response="$1500",
    )

    assert query_and_validate(
        question="What is the age recommendation for Monopoly?",
        expected_response="8+",
    )
    assert query_and_validate(
        question="How many players can play Monopoly?",
        expected_response="2 to 8 players",
    )
    assert query_and_validate(
        question="What happens when you land on or pass over GO in Monopoly?",
        expected_response="You collect $200",
    )
    assert query_and_validate(
        question="What does the Speed Die allow you to do in Monopoly?",
        expected_response="It speeds up the game",
    )
    assert query_and_validate(
        question="What happens if you roll doubles three times in a row in Monopoly?",
        expected_response="You go to Jail",
    )


# Test case 2: Ticket to Ride rules
def test_ticket_to_ride_rules():
    # Original question
    assert query_and_validate(
        question="How many points does the longest continuous train get in Ticket to Ride? (Answer with the number only)",
        expected_response="10 points",
    )
    
    assert query_and_validate(
        question="How many players can play Ticket to Ride?",
        expected_response="2 to 5 players",
    )
    assert query_and_validate(
        question="What age is Ticket to Ride recommended for?",
        expected_response="8 and above",
    )
    assert query_and_validate(
        question="How many Destination Ticket cards are in Ticket to Ride?",
        expected_response="30 cards",
    )
    assert query_and_validate(
        question="What happens when you have fewer than 3 plastic trains at the end of your turn in Ticket to Ride?",
        expected_response="The game ends",
    )
    assert query_and_validate(
        question="What color are the locomotives in Ticket to Ride?",
        expected_response="Multi-colored",
    )


if __name__ == "__main__":
    test_monopoly_rules()
    test_ticket_to_ride_rules()
