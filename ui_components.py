import streamlit as st
from chunker import ChunkingConfig


class ConfigController:
    def __init__(self):
        if "similarity_threshold" not in st.session_state:
            st.session_state.similarity_threshold = 0.88
        if "min_len" not in st.session_state:
            st.session_state.min_len = 250
        if "max_len" not in st.session_state:
            st.session_state.max_len = 500

    def sync_widget_state(self, parameter_key: str):
        slider_key = f"{parameter_key}_slider"
        input_key = f"{parameter_key}_input"

        if slider_key in st.session_state:
            st.session_state[parameter_key] = st.session_state[slider_key]
        elif input_key in st.session_state:
            st.session_state[parameter_key] = st.session_state[input_key]

    def create_parameter_widget(
        self,
        label: str,
        parameter_key: str,
        min_value,
        max_value,
        step,
        format_str: str = "%d",
    ):
        st.sidebar.write(f"**{label}**")
        col1, col2 = st.sidebar.columns([5, 1])

        current_value = st.session_state[parameter_key]

        with col1:
            st.slider(
                label,
                min_value=min_value,
                max_value=max_value,
                value=current_value,
                step=step,
                key=f"{parameter_key}_slider",
                label_visibility="collapsed",
                on_change=self.sync_widget_state,
                args=(parameter_key,),
            )
        with col2:
            st.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                value=current_value,
                step=step,
                format=format_str,
                key=f"{parameter_key}_input",
                label_visibility="collapsed",
                on_change=self.sync_widget_state,
                args=(parameter_key,),
            )

    def display_sidebar_widgets(self):
        st.sidebar.header("2. Tune Algorithm")
        self.create_parameter_widget(
            "Similarity Threshold",
            "similarity_threshold",
            0.70,
            0.99,
            0.01,
            "%.2f",
        )
        self.create_parameter_widget(
            "Minimum Chunk Length (chars)", "min_len", 50, 500, 10
        )

        minimum_allowed_max_length = st.session_state.min_len
        if st.session_state.max_len < st.session_state.min_len:
            st.session_state.max_len = st.session_state.min_len
        self.create_parameter_widget(
            "Maximum Chunk Length (chars)",
            "max_len",
            minimum_allowed_max_length,
            1000,
            10,
        )

    def get_chunking_config(self) -> ChunkingConfig:
        return ChunkingConfig(
            similarity_threshold=st.session_state.similarity_threshold,
            min_chunk_length=st.session_state.min_len,
            max_chunk_length=st.session_state.max_len,
        )
