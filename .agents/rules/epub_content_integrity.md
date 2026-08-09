# Systematic EPUB Content & Completeness Verification Rules

Every time ebooks or catalog entries are loaded, downloaded, generated, or built in this project, execute the following mandatory verification steps:

1. **Unabridged Text & Completeness Guarantee:**
   - **No Summaries/Resumes:** Verify systematically that the EPUB contains full, unabridged literary text. Never accept summaries, synopses, reviews, or book resumes.
   - **File Size Threshold:** Every EPUB file must be a full-length book (minimum >= 20 KB to 40 KB, 0 2KB stub files).

2. **OPF Metadata Alignment:**
   - `<dc:title>` and `<dc:creator>` inside the EPUB OPF manifest must match the expected catalog title and author 100%.

3. **Zero Synthetic Placeholders & Hash Collisions:**
   - 0 synthetic filler sentences or template review placeholders.
   - 0 binary MD5 hash collisions across files.

4. **Mandatory Test Runner Step:**
   - Always run `python3 -m unittest discover -s tests -v` after updating or building ebooks to verify that all 16 integrity checks pass cleanly.
