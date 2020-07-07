# Analysis Ready Data

The tutorials in this directory cover how to use the orders api to create Analysis Ready Data. These tutorials cover two use cases:
1. *As a software engineer at an ag-tech company, I'd like to be able to order Planet imagery programmatically in a way that enables the data scientist at my organization to create time-series algorithms (e.g. monitoring ndvi curves over time) without further data cleaning and processing.*

2. *As an agriculture customer, I'd like to create an imagery pipeline that provides for trialing different fungicides by ordering Planet imagery within a single field (AOI), cutting the imagery into multiple field blocks (grid within AOI), and comparing values across blocks in two ways. First, comparison is performed by extracting median, mean, variance NDVI values for each day (using random point sampling) in each block. Second, comparison is performed by random point selection in each block.*

The notebooks are meant to be worked through in sequence:
1. [Analysis Ready Data Tutorial Part 1: Introduction and Best Practices](ard_1_intro_and_best_practices.ipynb), provides an introduction to Analysis Ready Data and the Orders and Data APIs and provides best practices for using the APIs to prepare Analysis Ready Data.
1. [Analysis Ready Data Tutorial Part 2: Use Case 1](ard_2_use_case_1.ipynb) runs through the first use case, preparing an NDVI time stack. This part includes a second notebook, [Analysis Ready Data Tutorial Part 2: Use Case 1 - Visualize Images](ard_2_use_case_1_visualize_images.ipynb), for visualizing the NDVI imagery.
1. [Analysis Ready Data Tutorial Part 3: Use Case 2](ard_3_use_case_2.ipynb) runs through the second use case, preparing a gridded NDVI time stack of a field and performing comparisons across the grid blocks.
