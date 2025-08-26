import re

start = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
end = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

combined_regex = rf"{start}(.*?)({end})"

books = (
    "a-crystal-age",
    "a-modern-utopia",
    "herland",
    "little-fuzzy",
    "looking-backward",
    "new-atlantis",
    "news-from-nowhere",
    "the-last-evolution",
    "the-story-of-utopias",
    "utopia",
)

for book in books:
    with open(f"txt/{book}.txt", "r") as f:
        raw_content = f.read()
        print(len(raw_content))

        if content := re.search(combined_regex, raw_content, re.DOTALL):
            print(f"\n----------{book}----------\n")
            print(content[1][:200].strip().replace("\n", " "))
            print(content[1][-200:].strip().replace("\n", " "))
