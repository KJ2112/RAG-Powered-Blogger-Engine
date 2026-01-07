# RAG-Powered Search Engine

## Project Overview

This project builds an open-source, GPU-accelerated Retrieval-Augmented Generation (RAG) system over a corpus of scraped blogs. Instead of paid APIs, it uses:
- **Sentence-Transformers** on CUDA for fast semantic embeddings  
- **FAISS** for efficient vector retrieval  
- **Hugging Face Transformers** for on-device language generation  

All steps—from raw text ingestion to final answer generation—run in Jupyter notebooks on Kaggle’s dual Tesla T4 GPUs (16 GB each), ensuring both speed and reproducibility.

---

## Data Scraping

We collected ~9 000 blog posts by automating Google searches via the Serper API and a custom Python scraper:
1. **Query generation**  
   A curated list of domain-relevant search phrases was fed to Serper’s Google search endpoint.  
2. **URL filtering**  
   Results were filtered to exclude known non-blog domains (e.g. social media, video sites).  
3. **Content extraction**  
   Each URL was fetched with browser-style headers, parsed with BeautifulSoup, and concatenated into plain text.  
4. **Quality checks**  
   Language detection (NLTK + langdetect) ensured only English posts; very short pages (under 300 tokens) were discarded.  
5. **Deduplication**  
   URLs were MD5-hashed to avoid repeats; visited set persisted across runs.  
6. **Output**  
   Valid entries (title, URL, full text, rank, query) were appended into a single JSON array file—**scraped_blogs_final.json**.

---

## Data & Metadata

- The raw corpus (**scraped_blogs_final.json - https://drive.google.com/file/d/1z4DMBtV6aPV9y3A_c-6OqanN8A0xL2yA/view?usp=sharing**) and the 
  downstream chunk metadata (**metadata.pkl - https://drive.google.com/file/d/13phpSJbizWVxbmrwOUQMsarqIXDlMsTr/view?usp=sharing**) have been uploaded to Google Drive for easy access.  
- In Kaggle or Colab, mount the Drive and point your notebooks at those files under the mounted path.  

---

## Notebook Pipeline

### 1. `rag_prep.ipynb` – Preprocessing & Indexing  
- Loads the raw JSON of blog posts.  
- Splits each article into ~500-word chunks, tracking source identifiers.  
- Computes 384-dimensional embeddings on GPU.  
- Builds a FAISS inner-product index and saves both the index and chunk metadata.

### 2. `rag_recomm.ipynb` – Retrieval & Generation  
- Loads the FAISS index and the chunk metadata.  
- Defines a semantic retrieval function that embeds incoming queries on GPU and retrieves top-k chunks.  
- Assembles retrieved text into a context prompt.

---

## Environment & Performance

- **Runtime:** Kaggle Notebooks with two Tesla T4 GPUs (16 GB VRAM each)  
- **Indexing speed:** ~8–12 seconds for ~10 000 chunks  
- **Per-query latency:**  
  - Embedding + retrieval: < 0.1 s  
  - LLM generation (200 tokens): ~ 2 – 4 s  

This configuration allows rapid prototyping and high-quality results without external API costs.

---

## Future Work

- **Hybrid Retrieval**: Combine sparse (BM25) + dense (FAISS) to cover diverse query types  
- **Advanced Reranking**: Use a cross-encoder for final reordering of retrieved chunks  
- **Scalability**: Migrate FAISS index to a distributed store for millions of documents  
- **Model Upgrades**: Plug in newer open models (e.g. LLaMA-based) for higher-quality generation  

---

## Acknowledgements

This project adapts ideas from the RAG paradigm in open-source literature and leverages the Hugging Face and FAISS ecosystems for accessible, on-device NLP pipelines.  
