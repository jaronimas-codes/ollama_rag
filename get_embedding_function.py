####################################################################################################################
########################################## OllamaEmbeddings ########################################################
####################################################################################################################

from langchain_ollama import OllamaEmbeddings
def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

#####################################################################################################################
########################################## BedrockEmbeddings ########################################################
#####################################################################################################################

# from langchain_aws import BedrockEmbeddings

# def get_embedding_function():
#     embeddings = BedrockEmbeddings(
#         credentials_profile_name="default", region_name="us-east-1"
#     )
#     return embeddings

#####################################################################################################################
########################################## OpenAIEmbeddings #########################################################
#####################################################################################################################

# import openai
# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
# import os

# # Load environment variables from .env file
# # set .env file with OPENAI_API_KEY=numbers
# load_dotenv(override=True)

# # Access the OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_embedding_function():
#     # Ensure you have set your OpenAI API key as an environment variable
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     if not openai_api_key:
#         raise ValueError("OPENAI_API_KEY environment variable not set.")

#     # Initialize OpenAI embeddings
#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     return embeddings
