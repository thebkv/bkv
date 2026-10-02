#!/usr/bin/env python3
import argparse
import json
import re
import sys

# Standard KJV Book Number to Name Mapping
BOOK_MAP = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles", 15: "Ezra",
    16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms", 20: "Proverbs",
    21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah", 24: "Jeremiah", 25: "Lamentations",
    26: "Ezekiel", 27: "Daniel", 28: "Hosea", 29: "Joel", 30: "Amos",
    31: "Obadiah", 32: "Jonah", 33: "Micah", 34: "Nahum", 35: "Habakkuk",
    36: "Zephaniah", 37: "Haggai", 38: "Zechariah", 39: "Malachi", 40: "Matthew",
    41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Romans",
    46: "1 Corinthians", 47: "2 Corinthians", 48: "Galatians", 49: "Ephesians", 50: "Philippians",
    51: "Colossians", 52: "1 Thessalonians", 53: "2 Thessalonians", 54: "1 Timothy", 55: "2 Timothy",
    56: "Titus", 57: "Philemon", 58: "Hebrews", 59: "James", 60: "1 Peter",
    61: "2 Peter", 62: "1 John", 63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation"
}

def load_bible_data(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "verses" in data:
                return data["verses"]
            return data
    except Exception as e:
        print(f"Error loading JSON file '{json_path}': {e}", file=sys.stderr)
        sys.exit(1)

def get_clean_text(text):
    return re.sub(r"\{[^}]+\}", "", text)

def format_ref(entry, ref_key):
    book_raw = entry.get("book", "") if isinstance(entry, dict) else ""
    chap = entry.get("chapter", 0) if isinstance(entry, dict) else 0
    verse = entry.get("verse", 0) if isinstance(entry, dict) else 0

    if isinstance(book_raw, int) and book_raw in BOOK_MAP:
        book_name = BOOK_MAP[book_raw]
    elif str(book_raw).isdigit() and int(book_raw) in BOOK_MAP:
        book_name = BOOK_MAP[int(book_raw)]
    elif book_raw:
        book_name = str(book_raw)
    else:
        match = re.match(r"^(\d+)\s+(\d+):(\d+)$", str(ref_key))
        if match:
            b_num = int(match.group(1))
            b_name = BOOK_MAP.get(b_num, str(b_num))
            return f"{b_name} {match.group(2)}:{match.group(3)}"
        return str(ref_key)

    return f"{book_name} {chap}:{verse}".strip()

def search_bible(verses, target_word, mode, show_all, case_sensitive=False):
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(rf"\b{re.escape(target_word)}\b", flags)
    total_count = 0
    found_instances = []

    iterator = verses.items() if isinstance(verses, dict) else enumerate(verses)

    for ref_key, entry in iterator:
        if isinstance(entry, dict):
            raw_text = entry.get("raw") or entry.get("tagged") or entry.get("text") or ""
            clean_text = get_clean_text(raw_text)
            ref_str = format_ref(entry, ref_key)
        else:
            raw_text = str(entry)
            clean_text = get_clean_text(raw_text)
            ref_str = format_ref({}, ref_key)

        matches = list(pattern.finditer(clean_text))
        
        if matches:
            match_count = len(matches)
            total_count += match_count
            
            display_text = raw_text if show_all else clean_text
            display_text = " ".join(display_text.split())

            found_instances.append({
                "ref": ref_str,
                "text": display_text,
                "count_in_verse": match_count
            })

            if "count" not in mode:
                break

    return total_count, found_instances

def main():
    parser = argparse.ArgumentParser(
        description="Find first instance or total count of a word in a Bible JSON file."
    )
    parser.add_argument("json_file", help="Path to the Bible JSON file")
    parser.add_argument("word", help="Word to search for")
    parser.add_argument("-v", "--verse", action="store_true", help="Show clean verse text")
    parser.add_argument("-a", "--all", action="store_true", help="Show all tags (Strong's, TVM, raw data)")
    parser.add_argument("-c", "--count", action="store_true", help="Count total usages across the Bible")
    parser.add_argument("-s", "--case-sensitive", action="store_true", help="Enforce exact case matching")
    
    args = parser.parse_args()
    show_all = args.all
    mode = "count" if args.count else "find"

    verses = load_bible_data(args.json_file)
    total_count, instances = search_bible(verses, args.word, mode, show_all, case_sensitive=args.case_sensitive)

    if args.count:
        print(f"Total occurrences of '{args.word}': {total_count}")
        if instances:
            print(f"First occurrence: {instances[0]['ref']}")
            print(f"Text: {instances[0]['text']}")
    else:
        if instances:
            first = instances[0]
            print(f"{first['ref']}")
            print(f"Text: {first['text']}")
        else:
            print(f"Word '{args.word}' not found.")

if __name__ == "__main__":
    main()
