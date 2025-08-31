from dataclasses import dataclass
from typing import List

from books.a_crystal_age import chapter2
import spacy
from spacy.tokens import Doc, Span


@dataclass
class ChunkingConfig:
    similarity_threshold: float = 0.88
    min_chunk_length: int = 250
    max_chunk_length: int = 500


@dataclass
class Chunk:
    text: str
    sentences: List[Span]


class ChunkBuilder:
    def __init__(self, doc_context: Doc):
        self._doc = doc_context
        self.sentences: List[Span] = []

    def add_sentence(self, sentence: Span):
        self.sentences.append(sentence)

    def can_accommodate(self, sentence: Span, max_length: int) -> bool:
        if not self.sentences:
            return True
        potential_length = len(self.to_text()) + len(sentence.text) + 1
        return potential_length <= max_length

    def is_similar_to(self, sentence: Span, threshold: float) -> bool:
        if not self.sentences:
            return True
        return sentence.similarity(self.as_span()) >= threshold

    def as_span(self) -> Span:
        return self._doc[self.sentences[0].start : self.sentences[-1].end]

    def to_text(self) -> str:
        return " ".join([sent.text for sent in self.sentences])

    def clear(self):
        self.sentences = []


class SemanticChunker:
    def __init__(self, nlp_model: spacy.language.Language, config: ChunkingConfig):
        self.nlp = nlp_model
        self.config = config

    def process(self, text: str) -> List[Chunk]:
        doc = self.nlp(text)
        builder = ChunkBuilder(doc_context=doc)
        chunks: List[Chunk] = []

        for sentence in doc.sents:
            self.process_sentence(sentence, builder, chunks)

        self.finalize_chunks(builder, chunks)
        return chunks

    def process_sentence(
        self, sentence: Span, builder: ChunkBuilder, chunks: List[Chunk]
    ) -> None:
        is_similar = builder.is_similar_to(sentence, self.config.similarity_threshold)
        can_fit = builder.can_accommodate(sentence, self.config.max_chunk_length)

        if is_similar and can_fit:
            builder.add_sentence(sentence)
        else:
            self.complete_current_chunk(builder, chunks)
            builder.add_sentence(sentence)

    def complete_current_chunk(
        self, builder: ChunkBuilder, chunks: List[Chunk]
    ) -> None:
        chunk_text = builder.to_text()
        if len(chunk_text) >= self.config.min_chunk_length:
            chunks.append(
                Chunk(
                    text=chunk_text,
                    sentences=builder.sentences.copy(),
                )
            )
        builder.clear()

    def finalize_chunks(self, builder: ChunkBuilder, chunks: List[Chunk]) -> None:
        final_chunk_text = builder.to_text()
        if len(final_chunk_text) >= self.config.min_chunk_length:
            chunks.append(
                Chunk(
                    text=final_chunk_text,
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

    config = ChunkingConfig(
        similarity_threshold=0.88,
        min_chunk_length=250,
        max_chunk_length=500,
    )

    chunker = SemanticChunker(nlp_model=nlp, config=config)
    chunks = chunker.process(chapter2)

    doc = nlp(chapter2)
    sentences = list(doc.sents)

    # print(f"Processed chapter into {len(chunks)} chunks from {len(sentences)} sentences.")
    # for i, chunk in enumerate(chunks):
    #     print(
    #         f"--- CHUNK {i + 1} (Length: {len(chunk.text)}, Sentences: {len(chunk.sentences)}) ---"
    #     )
    #     print(chunk.text)
    #     print()
