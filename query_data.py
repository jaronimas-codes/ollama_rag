import argparse
import time  # Import the time module
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

# ################################
# ################################
#           Template #1

# PROMPT_TEMPLATE = """
# Answer the question based only on the following context:

# {context}

# ---

# Answer the question based on the above context: {question}
# """

# #################################
# ################################
#           Template #2

PROMPT_TEMPLATE = """
Based on the retrieved document, provide a detailed but concise answer to the following question:

{context}

---

{question}
"""

################################


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Record the start time
    start_time = time.time()

    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    query_text = f"Provide a concise answer (1-2 sentences) to the following question.\n{query_text}"
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2:1b")

    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"

    # Record the end time
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(formatted_response)
    print(f"Time taken: {elapsed_time:.2f} seconds")

    return response_text, sources


if __name__ == "__main__":
    main()
