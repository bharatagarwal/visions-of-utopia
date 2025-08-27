CREATE TABLE corpus (
    id SERIAL PRIMARY KEY,
    book_title VARCHAR(255) NOT NULL,
    chapter_title VARCHAR(255),
    chunk_sequence INT NOT NULL,
    chunk_text TEXT NOT NULL,
    nomic_embeddings VECTOR(768),
    mxb_embeddings VECTOR(1024),
    bge_embeddings VECTOR(1024)
);
