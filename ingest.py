import re

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


start = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
end = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

combined_regex = rf"{start}(.*?)({end})"

for book in books:
    with open(f"txt/{book}.txt", "r") as f:
        raw_content = f.read()

        if content := re.search(combined_regex, raw_content, re.DOTALL):
            pass
