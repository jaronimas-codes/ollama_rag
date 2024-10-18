import argparse
import os
import shutil
from langchain.document_loaders import PyPDFDirectoryLoader  # Ensure this is correct for your version
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma  # Updated import


CHROMA_PATH = "chroma"
# DATA_PATH = "data"
DATA_PATH = "data_compact"


def main():
    # Check if the database should be cleared (using the --reset flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    """Loads the PDF documents from the specified directory."""
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    """Splits the documents into chunks using the RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    """Adds or updates the documents in the Chroma database."""
    # Initialize Chroma with the persist directory
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs for the chunks
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Fetch existing document IDs from Chroma
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add new documents that don't exist in the DB.
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        print("Documents added to Chroma and automatically persisted.")
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    """Generates unique chunk IDs based on the source and page."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page metadata.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    """Clears the existing Chroma database by removing the directory."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
