Of course. Based on the detailed project plan and the sample `txt` files, here is a specific and actionable outline for your ingestion plan. This expands on "Sprint 1" with precise steps and considerations for your `ingest.py` script.

# Ingestion Plan: From Raw Text to Queryable Knowledge Base

This plan outlines the process for transforming the 10 Project Gutenberg `.txt` files into a structured, vectorized database ready for the  application.

Objective: To parse, clean, chunk, and embed the content of 10 utopian texts, storing the results in a local PostgreSQL database with the `pgvector` extension.

Key Technologies: Python, Regex, SpaCy, OpenAI API, PostgreSQL (`pgvector`), `psycopg2` library.

---

## Setup and Configuration

1.  Environment Setup:
  - Ensure your local PostgreSQL server is running.
  - Connect to PostgreSQL and create a new database (e.g., `utopian_synth`).
  - Enable the `pgvector` extension by running the command: `CREATE EXTENSION vector;`
  - Set up a Python virtual environment and install the necessary libraries:

 ```bash
 pip install spacy psycopg2-binary openai python-dotenv
 python -m spacy download en_core_web_md
 ```

2.  Database Schema:
  - Create the primary table for storing the text chunks and their embeddings.

  SQL Schema for `utopian_texts` table:
  ```sql
  CREATE TABLE utopian_texts (
      id SERIAL PRIMARY KEY,
      book_title VARCHAR(255) NOT NULL,
      chapter_title VARCHAR(255),
      chunk_sequence INT NOT NULL,
      chunk_text TEXT NOT NULL,
      embedding VECTOR(1536) -- OpenAI's text-embedding-ada-002 model output dimension
  );
  ```

3.  Project Structure:
    - Create a project directory with the following structure:
        ```
      utopian_synthesizer/
      ├── txt/
      │   ├── a-crystal-age.txt
      │   └── ... (all 10 .txt files)
      ├── ingest.py
      └── .env
      ```
  - Store your sensitive keys in the `.env` file (e.g., `OPENAI_API_KEY`, `DB_PASSWORD`).

---

## The `ingest.py` Script Logic

This script will be the heart of the ingestion process, executing a multi-step pipeline for each file.

Boilerplate Removal and Content Extraction
- Goal: Isolate the core narrative text from Project Gutenberg headers and footers.
- Method:
    1. Read each `.txt` file.
    2. Use Regular Expressions (Regex) to identify the start and end of the book's content. Project Gutenberg files often have clear markers.
        - Start Marker: Look for phrases like `* START OF THE PROJECT GUTENBERG EBOOK ... *`.
        - End Marker: Look for phrases like `* END OF THE PROJECT GUTENBERG EBOOK ... *`.
    3. Extract only the text between these two markers for processing.

Chapter-Level Segmentation
- Goal: Split the core text into its constituent chapters.
- Method:
    1. Use Regex to split the text based on common chapter heading formats (e.g., `Chapter 1`, `CHAPTER I.`, `Chapter the First`). The sample files show some variation, so the pattern should be flexible.
    2. For each resulting block of text, extract the chapter title and the chapter content. Store these as a list of `(chapter_title, chapter_content)` tuples.

Hierarchical Semantic Chunking (The Core Logic)
- Goal: Divide each chapter into smaller, semantically coherent chunks.
- Method: This implements the "Plain-Text-First Hierarchical Chunking Pipeline."
    1. Load SpaCy Model: Load the `en_core_web_md` model once at the beginning of the script.
    2. Sentence Segmentation: For each chapter's content, use SpaCy's `doc.sents` to accurately split the text into individual sentences. This is more robust than simple newline or period splitting.
    3. Semantic Grouping:
        - Iterate through the sentences of a chapter.
        - Group 3-5 consecutive sentences to form a preliminary "chunk."
        - This creates overlapping semantic context and ensures no sentence stands alone, which is crucial for high-quality embeddings. A simple grouping strategy is often more effective and computationally cheaper than complex vector similarity checks at this stage.

Embedding Generation
- Goal: Convert each text chunk into a vector embedding using OpenAI's API.
- Method:
    1. For each generated text chunk:
    2. Make an API call to OpenAI's embeddings endpoint (e.g., using the `text-embedding-ada-002` model).
    3. The API will return a 1536-dimension vector.

Database Storage
- Goal: Store the processed data and its vector embedding into the PostgreSQL database.
- Method:
    1. Establish a connection to your PostgreSQL database using `psycopg2`.
    2. For each chunk, execute an `INSERT` statement to add a new row to the `utopian_texts` table.
    3. The row should contain:
        - The book title (derived from the filename).
        - The chapter title from Step 2.
        - A sequence number for the chunk within the chapter.
        - The clean text of the chunk itself.
        - The embedding vector received from the OpenAI API.

Verification
- Goal: Confirm the ingestion was successful.
- Method: After the script runs, connect to your database and run a simple query to check the data.
    ```sql
    SELECT book_title, COUNT(*)
    FROM utopian_texts
    GROUP BY book_title;
    ```
- This will show you the number of chunks successfully ingested for each book, providing a high-level confirmation that the process worked as expected.
