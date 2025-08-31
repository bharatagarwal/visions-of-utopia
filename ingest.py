from books.a_crystal_age import chapter1, chapter2
import spacy

nlp = spacy.load("en_core_web_md")
doc = nlp(chapter2)

chunks = list()
current_chunk_sentences = list()
similarity_threshold = 0.88
min_chunk_length = 250
max_chunk_length = 500

sentences = list(doc.sents)

for i, sentence in enumerate(sentences):
    if not current_chunk_sentences:
        current_chunk_sentences.append(sentence)
        continue

    current_chunk = " ".join(
        [sent.text for sent in current_chunk_sentences]
    )
    current_chunk_doc = nlp(current_chunk)
    similarity = sentence.similarity(current_chunk_doc)
    print(f"{similarity}: {sentence}")

    potential_chunk = current_chunk + " " + sentence.text

    if (
        similarity >= similarity_threshold
        and len(potential_chunk) <= max_chunk_length
    ):
        current_chunk_sentences.append(sentence)
    else:
        if len(current_chunk) >= min_chunk_length:
            chunks.append(current_chunk)
        else:
            current_chunk_sentences.append(sentence)
            if len(potential_chunk) >= min_chunk_length:
                chunks.append(potential_chunk)
                current_chunk_sentences = []
            continue
        current_chunk_sentences = [sentence]

if current_chunk_sentences:
    final_chunk = " ".join(
        [sent.text for sent in current_chunk_sentences]
    )
    if len(final_chunk) >= min_chunk_length:
        chunks.append(final_chunk)
