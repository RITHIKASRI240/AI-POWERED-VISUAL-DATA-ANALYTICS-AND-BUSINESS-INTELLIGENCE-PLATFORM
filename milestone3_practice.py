import sys
import os

# add paths so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "documents"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "knowledge_base"))

from document_loader import load_document
from text_cleaner    import clean_text, get_word_count
from chunker         import split_into_chunks, split_by_paragraph
from metadata        import get_file_info, add_text_stats, print_info
from database        import add_chunks_to_db, search, reset_db


# -------------------------------------------------------
# STEP 1: Load the PDF
# -------------------------------------------------------
print("\n=== STEP 1: Loading Document ===")

pdf_path = "data/safety_manual.pdf"
raw_text = load_document(pdf_path)

if not raw_text:
    # use demo text if PDF not found
    print("Using demo text since PDF was not found.")
    raw_text = (
        "PPE Policy\n\n"
        "All employees must wear a hardhat on the construction site at all times. "
        "High-visibility vests are required near heavy machinery. "
        "Protective goggles must be worn when using grinding tools.\n\n"
        "Fire Safety\n\n"
        "Fire exits must stay clear at all times. "
        "Fire drills are held every three months. "
        "Fire extinguishers are placed at every floor entrance.\n\n"
        "First Aid\n\n"
        "First aid kits are at every workstation. "
        "Report any injury to the safety officer within 24 hours."
    )

print("Characters loaded:", len(raw_text))


# -------------------------------------------------------
# STEP 2: Clean the text
# -------------------------------------------------------
print("\n=== STEP 2: Cleaning Text ===")

cleaned = clean_text(raw_text)
print("Word count:", get_word_count(cleaned))
print("Preview:", cleaned[:200])


# -------------------------------------------------------
# STEP 3: Get file metadata
# -------------------------------------------------------
print("\n=== STEP 3: File Metadata ===")

info = get_file_info(pdf_path)
info = add_text_stats(info, cleaned)
print_info(info)


# -------------------------------------------------------
# STEP 4: Split into chunks
# -------------------------------------------------------
print("\n=== STEP 4: Chunking Text ===")

chunks = split_by_paragraph(cleaned)
print(f"Total chunks: {len(chunks)}")
for i, c in enumerate(chunks[:3]):
    print(f"\nChunk {i}: {c[:120]}")


# -------------------------------------------------------
# STEP 5: Store in vector database
# -------------------------------------------------------
print("\n=== STEP 5: Storing in Knowledge Base ===")

try:
    reset_db()
    add_chunks_to_db(chunks, source_name="safety_manual")
    print("Stored successfully!")
except Exception as e:
    print("Could not store in DB:", e)
    print("Make sure chromadb and sentence-transformers are installed.")


# -------------------------------------------------------
# STEP 6: Search the knowledge base
# -------------------------------------------------------
print("\n=== STEP 6: Searching Knowledge Base ===")

queries = [
    "What PPE is required on site?",
    "What are the fire safety rules?",
    "How to report an injury?",
]

for q in queries:
    print(f"\nQuery: {q}")
    try:
        results = search(q, top_k=2)
        for i, r in enumerate(results):
            print(f"  Result {i+1} (score={r['distance']}): {r['text'][:150]}")
    except Exception as e:
        print("  Search failed:", e)


print("\n=== All steps completed! ===")
