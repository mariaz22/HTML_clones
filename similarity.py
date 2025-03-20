import numpy as np
import json
import os
import asyncio
from css_images_compare import compute_css_similarity
from structure_compare import structural_similarity
import hdbscan
import sys
from collections import defaultdict

#combine the two similarity indices with the CSS index having a higher weight
async def combine_similarities(css_similarity, struct_similarity, weights={"css": 0.8, "structure": 0.2}):
    return (css_similarity * weights["css"]) + (struct_similarity * weights["structure"])

async def compare_files(file_pair):
    file1, file2 = file_pair
    css_sim = await compute_css_similarity(file1, file2)
    loop = asyncio.get_running_loop()
    struct_sim = await loop.run_in_executor(None, structural_similarity, file1, file2)
    combined_sim = await combine_similarities(css_sim, struct_sim)
    return combined_sim

async def main():
    with open("preprocessed_data.json", "r", encoding="utf-8") as f:
        preprocessed_data = json.load(f)

    num_files = len(preprocessed_data)

    file_pairs = [
        (preprocessed_data[i], preprocessed_data[j])
        for i in range(num_files)
        for j in range(i + 1, num_files)
    ]

    #print(f"Numar de comparații : {len(file_pairs)}")

    #the comparisons will be run in parallel for a shorter execution time
    tasks = [compare_files(pair) for pair in file_pairs]
    results = await asyncio.gather(*tasks)

    #a similarity matrix is created indicating the similarity between two HTML pages i and j
    similarity_matrix = np.zeros((num_files, num_files))
    for idx, (i, j) in enumerate(((i, j) for i in range(num_files) for j in range(i + 1, num_files))):
        similarity_matrix[i][j] = results[idx]
        similarity_matrix[j][i] = results[idx]

    #converts a similarity matrix into a distance matrix, where higher similarity corresponds to lower distance
    distance_matrix = 1 - similarity_matrix

    #use HDBSCAN algorithm to the distance matrix and predicts cluster assignments for each HTML page
    hdbscan_clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
    clusters = hdbscan_clusterer.fit_predict(distance_matrix)

    #they are traversed for display, and clusters are created for each subdirectory in the directory
    cluster_dict = defaultdict(lambda: defaultdict(list))
    for i, cluster in enumerate(clusters):
        subdirectory = preprocessed_data[i]['subdirectory']
        filename = os.path.basename(preprocessed_data[i]['file'])
        cluster_dict[subdirectory][cluster].append(filename)

    for subdirectory, clusters in cluster_dict.items():
        print(f"\nSubdirector: {subdirectory}")
        for cluster, files in clusters.items():
            if len(files) > 0:
                print(f" [{', '.join(files)}]")



if __name__ == '__main__':
    asyncio.run(main())
