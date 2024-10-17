# Project Setup Guide

This guide will help you set up the project by downloading Ollama, pulling the Mistral model, setting up a virtual environment, installing the required packages, setting the correct interpreter, and running the database population and querying process.

## Step 1: Download Ollama for Your OS

To get started, you need to download and install Ollama for your operating system. Follow the instructions on the official Ollama website:

- [Ollama for macOS](https://ollama.com)
- [Ollama for Windows](https://ollama.com)
- [Ollama for Linux](https://ollama.com)

Ensure Ollama is properly installed and accessible via the terminal or command prompt.

## Step 2: Pull the Mistral Model

Once Ollama is installed, you need to pull the `Mistral` model. Run the following command in your terminal or command prompt:

```bash
ollama pull mistral
```

This will download and prepare the Mistral model for usage in your project.

## Step 3: Clone the Repository

Next, clone this repository from GitHub and navigate to the folder:

```bash
git clone <repo-url>
cd <repository-folder-name>
```

## Step 4: Set Up the Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 5: Install Requirements

After activating the virtual environment, install the required dependencies by running:

```bash
pip install -r requirements.txt
```
This will install all the necessary packages for the project.

## Step 6: Set the Correct Python Interpreter

In your development environment (e.g., VS Code or PyCharm), ensure that the interpreter is set to the Python interpreter inside your virtual environment (venv). This can usually be done through your IDE's settings under the "Python Interpreter" section.

## (Optional) Step 7: Add OpenAI API Key for Secure Data Use

If you use OpenAIEmbeddings, then you need OpenAI API key
For secure use of sensitive data like the OpenAI API key, you need to add the key to a .env file in the root of your project. 
Create a .env file and add the following:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

Make sure this .env file is included in your .gitignore to prevent it from being committed to version control.

## Step 8: Populate the Database

With the environment set up, the next step is to populate the database with data.

```bash
python populate_database.py
```

This script will populate the database with the required data.


## Step 9: Query the Data

Once the database is populated, you can query the data using the following command:

```bash
python query_data.py
```

This script will run queries on the populated data and return results.

