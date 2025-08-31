import streamlit as st
from ui_components import ConfigController

st.set_page_config(
    page_title="Chunking Inspector",
    layout="centered",
)


st.markdown(
    """
<style>
    .stSidebar {
        padding: 2rem;
        width: 33% !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


st.sidebar.title(
    "Chunking Inspector",
)

st.sidebar.header(
    "1. Select Source Text",
)

book_title = st.sidebar.selectbox(
    "Choose a book:",
    options=["Book A", "Book B", "Book C"],
)

chapter = st.sidebar.selectbox(
    "Choose a chapter:",
    options=["Chapter 1", "Chapter 2", "Chapter 3"],
)

config_controller = ConfigController()
config_controller.display_sidebar_widgets()

chunk_config = config_controller.get_chunking_config()

st.title("Chunking Results")
st.markdown(
    f"**Book:** `{book_title}` | **Chapter:** `{chapter}`",
)

st.write("Current Configuration:")
st.write(chunk_config)

st.info("This is where the chunking results will be displayed.")
