import re


def split_into_chunks(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap  # move forward with overlap

    return chunks


def split_by_paragraph(text):
    paragraphs = re.split(r'\n{2,}', text)
    chunks = [p.strip() for p in paragraphs if p.strip()]
    return chunks


# test
if __name__ == "__main__":
    sample_text = (
        "PPE is very important on construction sites. "
        "Workers must wear helmets at all times. "
        "Gloves must be worn when handling chemicals.\n\n"
        "Section 2: Fire Safety. All fire exits must be clear. "
        "Fire drills happen every 3 months.\n\n"
        "Section 3: First Aid. Kits are at every entrance."
    )

    chunks = split_into_chunks(sample_text, chunk_size=100, overlap=20)
    print(f"Total chunks: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"\nChunk {i}: {c}")
