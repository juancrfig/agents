In Grok Build, MEMORY.md files (both global and workspace ones) and session logs are stored on the SQLite Index as overlapping chunks.  

### Cases Where These Chunks Are Injected into the Context Window

1. During the first run, the *FTS5/BM25* algorithm takes in the `MEMORY.md` files (global and workspace), the session logs, and the user's message. 
Looks on the index for chunks producing a high score of matching. These are injected automatically into the contex window.
2. After compaction, the resulting context is fed back into the algorithm and matching chunks are injected.
3. The LLM can choose to call `memory_search` (with a query string). It gets back matching chunks scored ≥ 0.7. Then it can call `memory_get` for the full file if needed.
