CREATE TABLE utopian_texts (
    id SERIAL PRIMARY KEY,
    book_title VARCHAR(255) NOT NULL,
    chapter_title VARCHAR(255),
    mxb_embeddings VECTOR(1024),
    chunk_sequence INT NOT NULL,
    bge_embeddings VECTOR(1024)
    chunk_text TEXT NOT NULL,
    nomic_embeddings VECTOR(768),
);
