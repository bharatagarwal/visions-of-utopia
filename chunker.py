from typing import Any, Dict, List

from books.a_crystal_age import chapter2
import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span


def create_chunking_config(
    threshold: float = 0.88,
    min_len: int = 250,
    max_len: int = 500,
):
    return {
        "threshold": threshold,
        "min_len": min_len,
        "max_len": max_len,
    }


def create_chunk(content, sentences: List[Span]):
    return {
        "content": content,
        "sentences": sentences,
    }


class ChunkBuilder:
    def __init__(self, context: Doc):
        self.doc = context
        self.sentences: List[Span] = []

    def add_sentence(self, sentence: Span):
        self.sentences.append(sentence)

    def can_accommodate(
        self,
        sentence: Span,
        max_length,
    ):
        if not self.sentences:
            return True

        newlen = len(self.to_text()) + len(sentence.text) + 1

        return newlen <= max_length

    def is_similar_to(
        self,
        sentence: Span,
        threshold,
    ):
        """
        If the chunk is empty, then any new sentence is automatically considered similar.
        """

        if not self.sentences:
            return True

        sim = sentence.similarity(self.as_span())
        return sim >= threshold

    def as_span(self) -> Span:
        start = self.sentences[0].start
        end = self.sentences[-1].end
        return self.doc[start:end]

    def to_text(self):
        return " ".join(
            [sent.text for sent in self.sentences],
        )

    def clear(self):
        self.sentences = []


class SemanticChunker:
    def __init__(
        self,
        nlp_model: Language,
        config,
    ):
        self.nlp = nlp_model
        self.config = config

    def process(self, text):
        doc = self.nlp(text)
        builder = ChunkBuilder(context=doc)

        chunks = []

        for sentence in doc.sents:
            self.process_sentence(
                sentence,
                builder,
                chunks,
            )

        self.finalize_chunks(builder, chunks)
        return chunks

    def process_sentence(
        self,
        sentence: Span,
        builder: ChunkBuilder,
        chunks,
    ):
        is_similar = builder.is_similar_to(
            sentence,
            self.config["threshold"],
        )

        can_fit = builder.can_accommodate(
            sentence,
            self.config["max_len"],
        )

        if is_similar and can_fit:
            builder.add_sentence(sentence)
        else:
            self.complete_current_chunk(
                builder,
                chunks,
            )

            builder.add_sentence(sentence)

    def complete_current_chunk(
        self,
        builder: ChunkBuilder,
        chunks,
    ):
        chunk_text = builder.to_text()

        if len(chunk_text) >= self.config["min_len"]:
            chunks.append(
                create_chunk(
                    content=chunk_text,
                    sentences=builder.sentences.copy(),
                )
            )

        builder.clear()

    def finalize_chunks(
        self,
        builder: ChunkBuilder,
        chunks,
    ):
        final_chunk_text = builder.to_text()

        final_chunk_len = len(final_chunk_text)

        if final_chunk_len >= self.config["min_len"]:
            chunks.append(
                create_chunk(
                    content=final_chunk_text,
                    sentences=builder.sentences.copy(),
                )
            )


if __name__ == "__main__":
    try:
        nlp = spacy.load("en_core_web_md")
    except OSError:
        raise RuntimeError(
            "spaCy model 'en_core_web_md' not found. Please run: python -m spacy download en_core_web_md"
        )

    config = create_chunking_config(
        threshold=0.88,
        min_len=250,
        max_len=500,
    )

    chunker = SemanticChunker(nlp_model=nlp, config=config)
    chunks = chunker.process(chapter2)

    doc = nlp(chapter2)
    sentences = list(doc.sents)
