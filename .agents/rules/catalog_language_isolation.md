# Catalog Language & Translation Isolation Rules

When adding, building, or modifying ebooks in the Athena Ebook Library project, enforce these strict language isolation rules:

1. **French Authors:**
   - Must ALWAYS be in authentic **French** (`language: "French"`, `<dc:language>fr</dc:language>`).
   - Applies to all French classics (e.g. Victor Hugo, Alexandre Dumas, Émile Zola, Honoré de Balzac, Marcel Proust, Molière, Voltaire).

2. **English Authors:**
   - Must ALWAYS be in authentic **English** (`language: "English"`, `<dc:language>en</dc:language>`).
   - Applies to all English classics (e.g. William Shakespeare, Charles Dickens, Jane Austen, Oscar Wilde, Arthur Conan Doyle, Mark Twain).

3. **World Authors (Non-French, Non-English):**
   - Must ALWAYS be in **French Translation** (`language: "French (Traduction)"`, `<dc:language>fr</dc:language>`).
   - Applies to all World Masterpieces (e.g. Nikolai Gogol, Fyodor Dostoevsky, Leo Tolstoy, Anton Chekhov, Dante Alighieri, Miguel de Cervantes, Homer, Virgil, Franz Kafka, Goethe).
