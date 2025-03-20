#The folder where the directories containing the HTML pages are saved is accessed, and a JSON file is created for each page containing
# the information extracted from the HTML and CSS code in the form of dictionaries for easier access to the information in the code for
# comparison.
from bs4 import BeautifulSoup
import os
import json
import re

# the functiono extracts all color values from CSS content and it is used for comparing shades
def extract_css_colors(css_content):
    color_pattern = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}|rgb\(\d+,\s*\d+,\s*\d+\)")
    return set(color_pattern.findall(css_content))

# reads an HTML and parses the document using BeautifulSoup, the extracted data is returned as a dictionary
# this function is useful for analyzing and comparing web pages based on their content and design
def preprocess_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

    dom_structure = [tag.name for tag in soup.find_all()]

    for script in soup(["script", "style", "noscript"]):
        script.extract()
    visible_text = " ".join(soup.stripped_strings)

    styles = [style.get("class") for style in soup.find_all(class_=True)]

    colors = set()
    for style_tag in soup.find_all("style"):
        colors.update(extract_css_colors(style_tag.get_text()))

    for tag in soup.find_all(style=True):
        colors.update(extract_css_colors(tag["style"]))

    links = [a["href"] for a in soup.find_all("a", href=True)]
    images = [img["src"] for img in soup.find_all("img", src=True)]

    subdirectory = os.path.basename(os.path.dirname(file_path))

    return {
        "file": file_path,
        "subdirectory": subdirectory,
        "dom_structure": dom_structure,
        "visible_text": visible_text,
        "styles": styles,
        "colors": list(colors),
        "links": links,
        "images": images
    }

def preprocess_directory(directory):
    dataset = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                file_path = os.path.join(root, filename)
                dataset.append(preprocess_html(file_path))

    with open("preprocessed_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return dataset


directory_path = "D:\\clones_2\\clones"
preprocessed_data = preprocess_directory(directory_path)
with open("preprocessed_data.json", "r", encoding="utf-8") as f:
    preprocessed_data = json.load(f)

#print("Datele au fost incarcate")
