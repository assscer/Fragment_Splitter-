import argparse
from pathlib import Path
from msg_split import split_message

def main():
    parser = argparse.ArgumentParser(description="Split an HTML file into fragments.")
    parser.add_argument("file", type=Path, help="Path to the HTML file")
    parser.add_argument("--max-len", type=int, default=4096, help="Maximum length of each fragment")
    args = parser.parse_args()

    try:
        source = args.file.read_text(encoding="utf-8")
        for idx, fragment in enumerate(split_message(source, max_len=args.max_len), start=1):
            print(f"-- fragment #{idx}: {len(fragment)} chars --")
            print(fragment)
            print("\n" + "-" * 80 + "\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
