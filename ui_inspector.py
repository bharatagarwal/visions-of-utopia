import os
import pickle
import time

from books.a_crystal_age import chapter1, chapter2
from chunker import SemanticChunker
import spacy
import streamlit as st
from ui_components import ConfigController

st.set_page_config(
    page_title="Chunking Inspector",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stSidebar {
        padding: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_spacy_model():
    return spacy.load(
        "en_core_web_md",
    )


# Initialize session_state to hold our results across reruns.
if "processed_chunks" not in st.session_state:
    st.session_state.processed_chunks = []
if "total_sentences" not in st.session_state:
    st.session_state.total_sentences = 0
if "current_chapter_name" not in st.session_state:
    st.session_state.current_chapter_name = "Chapter 1"


nlp = load_spacy_model()
config_controller = ConfigController()

chapters = {
    "Chapter 1": chapter1,
    "Chapter 2": chapter2,
}

st.sidebar.title("Chunking Inspector")
st.sidebar.header("1. Select Source Text")

selected_chapter_name = st.sidebar.selectbox(
    "Choose a chapter:",
    options=list(
        chapters.keys(),
    ),
)

config_controller.display_sidebar_widgets()

process_button_pressed = st.sidebar.button(
    "Process Chapter",
    use_container_width=True,
    type="primary",
)

# --- Main Logic: Gated by the Button Press ---
if process_button_pressed:
    selected_chapter_text = chapters[selected_chapter_name]
    chunk_config = config_controller.get_chunking_config()

    chunker = SemanticChunker(
        nlp_model=nlp,
        config=chunk_config,
    )

    # When the button is pressed, we run the chunker and SAVE the results to session_state.
    with st.spinner("Chunking text..."):
        st.session_state.processed_chunks = chunker.process(
            selected_chapter_text
        )
        st.session_state.total_sentences = len(
            list(nlp(selected_chapter_text).sents)
        )
        st.session_state.current_chapter_name = selected_chapter_name

# --- Display Logic: Reads ONLY from Session State ---

col1, col2 = st.columns([3, 1])
with col1:
    st.title("Chunking Results")
    st.markdown(
        f"**Book:** `A Crystal Age` | **Chapter:** `{st.session_state.current_chapter_name}`"
    )

with col2:
    if st.session_state.processed_chunks:
        if st.button("Save", type="primary", use_container_width=True):
            # Create filename: booktitle-chapter-epochtime.pkl
            book_title = "a-crystal-age"
            chapter_name = (
                st.session_state.current_chapter_name.lower().replace(
                    " ", "-"
                )
            )
            epoch_time = int(time.time())
            filename = f"{book_title}-{chapter_name}-{epoch_time}.pkl"
            filepath = os.path.join("chunks", filename)

            # Convert spaCy objects to serializable format
            serializable_chunks = []
            for chunk in st.session_state.processed_chunks:
                serializable_chunk = {
                    "content": chunk["content"],
                    "sentences": [
                        sentence.text for sentence in chunk["sentences"]
                    ],
                }
                serializable_chunks.append(serializable_chunk)

            # Save the processed chunks
            with open(filepath, "wb") as f:
                pickle.dump(serializable_chunks, f)

            st.success(f"Chunks saved to {filename}")

metrics_col1, metrics_col2 = st.columns(2)

metrics_col1.metric(
    label="Total Sentences", value=st.session_state.total_sentences
)

metrics_col2.metric(
    label="Generated Chunks",
    value=len(st.session_state.processed_chunks),
)

st.divider()

st.header("Chunk and Sentence Breakdown")

if not st.session_state.processed_chunks:
    st.info(
        "Adjust parameters in the sidebar and click 'Process Chapter' to begin."
    )
else:
    # This loop now displays the PERSISTENT results from session_state.
    for i, chunk in enumerate(st.session_state.processed_chunks):
        chunk_text = chunk["content"]
        source_sentences = chunk["sentences"]

        expander_title = (
            f"Chunk #{i + 1}   |   "
            f"Length: {len(chunk_text)} chars   |   "
            f"Sentences: {len(source_sentences)}"
        )
        with st.expander(expander_title):
            st.subheader("Final Chunk Text")
            st.write(chunk_text)

            st.subheader("Source Sentences")
            for sentence in source_sentences:
                st.markdown(f"- *{sentence.text.strip()}*")
