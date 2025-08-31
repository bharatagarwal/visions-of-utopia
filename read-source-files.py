import os
import re

books = (
    "a_crystal_age",
    "a_modern_utopia",
    "herland",
    "little_fuzzy",
    "looking_backward",
    "new_atlantis",
    "news_from_nowhere",
    "the_last_evolution",
    "the_story_of_utopias",
    "utopia",
)


start = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
end = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

combined_regex = rf"{start}(.*?)({end})"

for book in books:
    with open(f"source/{book}.txt", "r") as f:
        raw_content = f.read()

        if content := re.search(combined_regex, raw_content, re.DOTALL):
            extracted_content = content.group(1).strip()
            with open(f"books/{book}.py", "w") as out_f:
                out_f.write('"""\n')
                out_f.write(extracted_content)
                out_f.write('\n"""')
