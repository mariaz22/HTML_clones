# Clustering algorithm for HTML documents

## Overview
This project aims to design an algorithm that groups together HTML documents that are similar from the perspective of a user viewing them in a web browser. The algorithm is implemented in Python using specific libraries.

## Project Structure
The project is organized into four main files, each serving a specific purpose in the overall functionality of the HTML document clustering algorithm:

1.HTML_data
  Is responsible for preprocessing HTML documents stored in specified directories. It extracts essential information from each HTML file, facilitating analysis and comparison of web pages. The main functionalities of this module include:
    -extract_css_colors(css_content) utilizes a regular expression to find and extract all color values from the provided CSS content, This extraction is crucial for comparing color shades between different web pages
    -preprocess_html(file_path) function reads an HTML file using the BeautifulSoup library to parse the document structure
    -preprocess_directory(directory) function iterates through a specified directory, processing each HTML file it finds
    -the dataset is saved as a JSON file (preprocessed_data.json)

2.structure_compare
  Is designed to analyze and compute the structural similarity between HTML documents
    -jaccard_similarity(set1, set2) calculates the Jaccard similarity coefficient between two sets, it measures similarity by dividing the size of the intersection of the sets by the size of           their union, providing a value between 0 and 1, a value of 1 indicates identical sets, while 0 indicates no overlap
    -structural_similarity(file1, file2) function integrates the results from text similarity, DOM structure similarity, and link similarity to compute a comprehensive similarity score. It uses weighted contributions from each similarity measure to determine the overall structural similarity between two HTML files:

    Text similarity contributes 40%
    DOM structure similarity contributes 40%
    Link similarity contributes 20%


 3.css_images_compare
 Is responsible for extracting and comparing CSS styles and images from HTML documents to determine their visual similarity.
   -hex_to_rgb(color) this function converts a hexadecimal color code into an RGB tuple, it handles hex codes, returning the corresponding RGB values as integers
   -extract_rgb(color) extracts RGB values from strings formatted as rgb(r, g, b), it uses a regular expression to find and return the RGB components as a tuple of integers
   -color_distance(color1, color2) calculates the Euclidean distance between two RGB colors, which is useful for determining how similar two colors are in terms of their visual representation
   -css_class_similarity(file1, file2): calculates the Jaccard similarity between the CSS class styles of two HTML documents
   -compute_css_similarity(file1, file2, weights): using asynchronous programming enhances performance by allowing multiple operations to run concurrently, improving responsiveness and              scalability when dealing with large datasets, 
    It combines the similarity scores for colors, styles, and images, applying specified weights to each component:
    Color similarity contributes 40% 
    Style similarity contributes 30% 
    Image similarity contributes 30%
    The function also handles edge cases, such as when both documents lack colors or styles, returning a similarity score of 1.0 if both are empty

4.similarity
 Is responsible for computing the overall similarity between HTML documents based on their CSS styles and structural elements.
 -combine_similarities(css_similarity, struct_similarity, weights)  it allows the user to specify weights for each component, with the CSS index having a higher weight (default is 0.8 for CSS     and 0.2 for structure). This prioritization emphasizes visual aspects when comparing documents.
 -the module applies the HDBSCAN clustering algorithm to the distance matrix, predicting cluster assignments for each HTML page based on their similarity
 -the results are organized and printed, displaying clusters of files grouped by their respective subdirectories

## Requirements
-Python 3.x is required to execute the project
-This project relies on several external libraries
In terminal: pip install beautifulsoup4 lxml numpy hdbscan
-ensure that the preprocessed_data.json file is available in the project directory

## Usage
To use the algorithm, specify the path to the dataset directory:
In HTML_data.py: directory_path = "specify yhe path"
 
