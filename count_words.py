#!/usr/bin/env python3

import os
import re
import glob

def count_words_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter (between ---)
    content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL|re.MULTILINE)

    # Remove import statements
    content = re.sub(r'^import.*$', '', content, flags=re.MULTILINE)

    # Remove HTML-like tags and components
    content = re.sub(r'^<.*>$', '', content, flags=re.MULTILINE)

    # Remove Mermaid diagrams
    content = re.sub(r'```mermaid.*?```', '', content, flags=re.DOTALL)

    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove admonitions
    content = re.sub(r'^:::.*?^:::', '', content, flags=re.DOTALL|re.MULTILINE)

    # Count remaining words
    words = re.findall(r'\b\w+\b', content)
    return len(words)

def main():
    print("Chapter Word Count Summary")
    print("==========================")

    mdx_files = glob.glob("/mnt/c/Users/dell/Desktop/AI-Spec-Driven-Book/book_frontend/docs/**/*.mdx", recursive=True)

    total_words = 0
    chapter_counts = []

    for file_path in sorted(mdx_files):
        word_count = count_words_in_file(file_path)
        filename = os.path.basename(file_path)
        chapter_counts.append((filename, word_count))
        print(f"{filename}: {word_count} words")
        total_words += word_count

    print(f"\nTotal words across all chapters: {total_words}")

    # Identify files with fewer than 500 words (potentially too short based on spec)
    short_chapters = [item for item in chapter_counts if item[1] < 500 and 'intro' not in item[0].lower()]
    if short_chapters:
        print(f"\nChapters with fewer than 500 words (may need expansion):")
        for filename, count in short_chapters:
            print(f"  - {filename}: {count} words")

if __name__ == "__main__":
    main()