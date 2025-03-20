import re
from collections import Counter
import time
import string

# calculates the Jaccard similarity coefficient between two sets
#measures the similarity by dividing the size of the intersection of the sets by the size of their union

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0


def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.strip()

def text_similarity(text1, text2):
    text1 = normalize_text(text1)
    text2 = normalize_text(text2)

    words1 = Counter(text1.split())
    words2 = Counter(text2.split())

    intersection = sum((words1 & words2).values())
    union = sum((words1 | words2).values())

    return intersection / union if union != 0 else 0

def dom_structure_similarity(dom1, dom2):
    return jaccard_similarity(set(dom1), set(dom2))

def link_similarity(links1, links2):
    return jaccard_similarity(set(links1), set(links2))

def structural_similarity(file1, file2):
    text_sim = text_similarity(file1["visible_text"], file2["visible_text"])
    dom_sim = dom_structure_similarity(file1["dom_structure"], file2["dom_structure"])
    link_sim = link_similarity(file1["links"], file2["links"])

    total_similarity = (text_sim * 0.4) + (dom_sim * 0.4) + (link_sim * 0.2)
    return total_similarity


if __name__ == "__main__":
    import json

    with open("preprocessed_data.json", "r", encoding="utf-8") as f:
        preprocessed_data = json.load(f)

    file1 = preprocessed_data[0]
    file2 = preprocessed_data[1]

    #start_time = time.perf_counter()
    similarity_score = structural_similarity(file1, file2)

    #end_time = time.perf_counter()
    #print(f"Timp executie: {end_time - start_time:.6f}")