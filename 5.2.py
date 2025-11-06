import sys
import re
from collections import Counter

def read_files(paths):
    text = ""
    for path in paths:
        with open(path, 'r', encoding='utf-8') as f:
            text += f.read() + " "
    return text

def clean_words(text):
    return re.findall(r'\b\w+\b', text.lower())

def split_sentences(text):
    return re.split(r'[.!?]', text)

def main():
    files = sys.argv[1:]
    text = read_files(files)

    words = clean_words(text)
    sentences = [s.strip() for s in split_sentences(text) if s.strip()]

    word_freq = Counter(words)
    unique_words = set(words)
    sentence_lengths = {s: len(s.split()) for s in sentences}

    longest = max(sentence_lengths, key=sentence_lengths.get)
    shortest = min(sentence_lengths, key=sentence_lengths.get)

    print("\nTop 10 frequent words:")
    for word, count in word_freq.most_common(10):
        print(f"{word}: {count}")

    print(f"\nTotal unique words: {len(unique_words)}")
    print(f"\nLongest sentence ({sentence_lengths[longest]} words):\n{longest}")
    print(f"\nShortest sentence ({sentence_lengths[shortest]} words):\n{shortest}")

if __name__ == "__main__":
    main()
