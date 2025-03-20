import re
import numpy as np
import time
import asyncio
import json

#the function converts a hexadecimal color code into an RGB tuple
#extracts and converts each pair of hex digits into an integer representing RGB components
def hex_to_rgb(color):
    color = color.lstrip("#")
    if len(color) == 3:
        color = "".join([c * 2 for c in color])
    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

#extracts the RGB values from a color string in RGB or RGBA format
#it uses re.match to find numeric values inside an rgb() or rgba() string
#is useful for comparing colors
def extract_rgb(color):
    match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color)
    if match:
        return tuple(map(int, match.groups()))
    return None

def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

#calculates the similarity between two sets of colors by converting them into RGB format and comparing their distances
#it converts hex and RGB colors into RGB tuples using hex_to_rgb and extract_rgb
#for each color in the first set, it finds the closest color in the second set based on Euclidean distance
def color_similarity(set1, set2):
    if not set1 or not set2:
        return 0.0

    set1_rgb = {hex_to_rgb(c) if c.startswith("#") else extract_rgb(c) for c in set1}
    set2_rgb = {hex_to_rgb(c) if c.startswith("#") else extract_rgb(c) for c in set2}
    set1_rgb.discard(None)
    set2_rgb.discard(None)

    if not set1_rgb or not set2_rgb:
        return 0.0

    total_similarity = sum(
        1 - (min(color_distance(c1, c2) for c2 in set2_rgb) / np.sqrt(255**2 * 3))
        for c1 in set1_rgb
    )

    return total_similarity / len(set1_rgb)

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def css_class_similarity(file1, file2):
    styles1 = {",".join(sorted(cls)) for cls in file1["styles"] if cls}
    styles2 = {",".join(sorted(cls)) for cls in file2["styles"] if cls}
    return jaccard_similarity(styles1, styles2)

async def compute_css_similarity(file1, file2, weights={"colors": 0.4, "styles": 0.3, "images": 0.4}):
    color_sim = color_similarity(set(file1["colors"]), set(file2["colors"]))
    style_sim = css_class_similarity(file1, file2)

    colors_empty = len(file1["colors"]) == 0 and len(file2["colors"]) == 0
    styles_empty = len(file1["styles"]) == 0 and len(file2["styles"]) == 0

    if colors_empty and styles_empty:
        return 1.0

    if (colors_empty and not styles_empty) or (not colors_empty and styles_empty):
        return 0.0

    image_urls1 = set(file1["images"])
    image_urls2 = set(file2["images"])

    if len(image_urls1) == 0 and len(image_urls2) == 0:
        image_sim = 1.0
    elif image_urls1 == image_urls2:
        image_sim = 1.0
    else:
        image_sim = 0.0

    total_similarity = (
        color_sim * weights["colors"] +
        style_sim * weights["styles"] +
        image_sim * weights["images"]
    )

    return total_similarity
if __name__ == "__main__":
    start_time = time.perf_counter()

    with open("preprocessed_data.json", "r", encoding="utf-8") as f:
        preprocessed_data = json.load(f)

    file1 = preprocessed_data[0]
    file2 = preprocessed_data[1]

    similarity_score = asyncio.run(compute_css_similarity(file1, file2))

    end_time = time.perf_counter()
    #print(f"Timp executie: {end_time - start_time:.6f}")
