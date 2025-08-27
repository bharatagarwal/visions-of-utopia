# Project Plan

## Core Vision

Create "Visions of Utopia" an interactive web application that allows users to explore and synthesize concepts from a curated library of 10 classic utopian texts.

The tool will use a RAG (Retrieval-Augmented Generation) pipeline to provide
nuanced, comparative, and properly cited answers based on the source material.

## Source Texts

You have a final list of 10 public domain books. The most pragmatic source format is the UTF-8 plain text (`.txt`) files from Project Gutenberg, as they are cleaner and more consistently structured for automated processing than the HTML versions.

## Chunking Strategy

A hierarchical, multi-tool pipeline is best:

1. Parse `.txt` files: Use Regex to clean boilerplate and split the text into chapters.
2. Use SpaCy Locally: Within each chapter, use SpaCy for robust sentence segmentation and its built-in vectors to perform a fast, free, local semantic chunking process, grouping related sentences into coherent paragraphs.
3. Final Cloud Embeddings: Generate the final, high-quality storage embeddings for these completed chunks using OpenAI's API.

### Technology Stack

- Data Ingestion: Python, SpaCy, Regex, OpenAI Embedding API.
- Database: A local PostgreSQL instance with the `pgvector` extension.
- Application Backend: Python with a search module using the `psycopg2` library.
- Application Frontend: Streamlit is the recommended choice for its balance of rapid development and a professional, customizable UI.
- Synthesis LLM: GPT-4.1-Turbo (or a similar frontier model) via OpenAI's API is non-negotiable for achieving the high-quality synthesis and citation required by the vision.

### Hardware Strategy (M1 Air 8GB)

A hybrid model is necessary for your M1 Air 8GB:

- Local Machine: Handles all data ingestion, the Postgres database, running the Streamlit app, and the cron job for image generation.
- Cloud APIs: Used for the one-time embedding of chunks and the real-time generation of the final synthesis.

### Image Gallery

A nightly cron job on your local machine using MLX and the SDXL-Turbo model will generate "visions of utopia" and save them to a gallery folder, providing a unique and engaging visual element for your app.

---

# Product Requirements Document: Visions of Utopia

## Vision & Goal

To create a web-based tool that makes the rich, complex ideas within foundational utopian literature accessible and explorable. The synthesizer will not just answer questions but will act as an intellectual partner, helping users compare, contrast, and synthesize different philosophical visions for an ideal society.

## User Personas

- The Student/Researcher: Needs to quickly find and compare how different authors (e.g., Bellamy vs. Morris) approached specific themes like labor, governance, or technology. Values accurate citations and direct access to source text.
- The Curious Explorer: A non-specialist interested in "big ideas." Wants to ask broad, conceptual questions and receive an engaging, coherent, and thought-provoking summary.
- The Creative/Writer: Looking for inspiration and novel concepts. Wants to explore diverse, sometimes conflicting ideas to spark their own creative process.

##  Core Features

| Feature Name | Description | User Story |
| :--- | :--- | :--- |
| Core Synthesis Engine | The user can enter a text query about a utopian concept. The system will retrieve relevant passages from the 10-book corpus and use a powerful LLM to generate a synthesized, multi-paragraph answer. | "As a curious explorer, I want to ask 'How is family structured in utopia?' and receive a coherent essay that draws from multiple books." |
| Source Citation | Every sentence in the synthesized answer that draws from a retrieved source must be clearly cited (e.g., `[Source 1]`, `[Source 2]`). | "As a student, I need to know exactly which book an idea came from so I can verify the source." |
| Context Transparency | The UI must display the exact, unaltered source chunks that were retrieved and fed to the LLM as context for the generation. | "As a researcher, I want to see the raw context to evaluate *why* the AI generated the answer it did." |
| Semantic Search Control | The user can choose between at least two retrieval methods: "Simple Vector Search" for direct relevance and "Diverse Search (MMR)" for broader, more comparative results. | "As a creative, I want to use 'Diverse Search' on 'technology' to see conflicting ideas, not just the same one repeated." |
| Source Filtering | The user can select a subset of the 10 books to include in the search, allowing for targeted queries. | "As a student, I want to filter my search to only *News from Nowhere* and *A Crystal Age* to compare pastoral utopias." |
| "Visions" Gallery | The application will display a gallery of AI-generated images, each representing a "vision of utopia" inspired by the source texts. | "As a user, I want to be visually inspired by artistic interpretations of the utopian concepts." |


## Non-Functional Requirements

- Performance: The web interface must be responsive. The final answer generation should ideally take under 15 seconds.
- Usability: The UI must be clean, intuitive, and require no technical knowledge to operate.
- Scalability: The backend must be designed to handle potential future expansion with more texts.
- Cost Management: The system must include caching to minimize redundant API calls.

## Future Features

- Interactive Citations: Clicking on a citation `[Source 1]` links the user directly to the relevant source chunk.
- User Accounts & History: Allow users to save their queries and the AI's responses.
- BYOK Model: Add an option for users to input their own API key for unlimited use.
---

# Implementation Plan

This is a high-level, phased plan to take you from zero to a deployed MVP.

## Data Ingestion & Local Setup

- Goal: Create the complete knowledge base.
- Tasks:
  - Download the 10 plain text files from Project Gutenberg.
  - Set up the local PostgreSQL database with the `pgvector` extension and the `utopian_texts` table schema.
  - Write the `ingest.py` script:
    - Implement the full Plain-Text-First Hierarchical Chunking Pipeline (Regex for chapters, SpaCy for semantic sentence grouping within chapters).
    - Integrate the OpenAI Embedding API call to generate and store the final embeddings for each chunk.
    - Run the ingestion script and populate your database. Verify the data is clean and correct.
- Deliverable: A fully populated PostgreSQL database ready for querying.

## Backend & UI Scaffolding

- Goal: Build a functional, end-to-end RAG pipeline and a basic UI.
- Tasks:
  - Create the `database.py` module. Implement the `simple_vector_search` and `get_all_book_titles` methods.
  - Create the `app_streamlit.py` file.
  - Build the basic Streamlit UI layout: sidebar for controls, main area for query and output.
  - Write the core `generate_utopian_vision` function. Implement the RAG logic using the "Simple Vector Search" method first. Hardcode the call to GPT-4.1.
- Deliverable: A working Streamlit app that can take a query, retrieve context, and generate a basic (uncited) answer.

## Advanced Features & Polish

- Goal: Implement the advanced features that fulfill the core product vision.
- Tasks:
  - Enhance `database.py`: Implement the Diverse Search (MMR) and Filtered Search methods.
  - Enhance `app_streamlit.py`:
    - Add the radio button and multi-select widgets to the UI to control the new search methods.
    - Update the `generate_utopian_vision` function to handle the logic for all three search modes.
    - Refine the master system prompt to enforce strict source citation.
    - Add the "Retrieved Sources" expander to the UI for context transparency.
  - Set up the Gallery:
    - Write the `cron_vision_generator.py` script using MLX and SDXL-Turbo.
    - Test it locally to generate a few images.
    - Configure the cron job on your Mac to run it automatically.
    - Add code to your Streamlit app to read from the `gallery` directory and display the images.
- Deliverable: The complete, feature-rich MVP application as defined in the PRD.

## Deployment & Cost Control

- Goal: Make the app public and ensure it's sustainable.
- Tasks:
  - Implement caching in your Streamlit app using `@st.cache_data` on your `generate_utopian_vision` function. This is your most important cost-control measure.
  - Deploy the app using a free service like Streamlit Community Cloud. Set your OpenAI API key as a secret in the deployment settings.
  - Share the link and start gathering feedback!
- Deliverable: A publicly accessible URL for your Visions of Utopia.
