# Analysis Ready Data

The tutorials in this directory cover how to use the data and orders APIs to create Analysis Ready Data. These tutorials provide an introduction to concepts necessary in creating Analysis Ready Data and an introduction to the data and orders APIs, best practices for utilizing the data and orders APIs to create Analysis Ready Data, and a walkthrough of a real-world use case. 

The use case covered is:
*As an agriculture customer, I'd like to create an imagery pipeline that provides for trialing different fungicides by ordering Planet imagery within a single field (AOI), cutting the imagery into multiple field blocks (grid within AOI), and comparing values across blocks in two ways. First, comparison is performed by extracting median, mean, variance NDVI values for each day (using random point sampling) in each block. Second, comparison is performed by random point selection in each block.*

The notebooks are meant to be worked through in sequence:
1. [Analysis Ready Data Tutorial Part 1: Introduction and Best Practices](ard_1_intro_and_best_practices.ipynb), provides an introduction to Analysis Ready Data and the Orders and Data APIs and provides best practices for using the APIs to prepare Analysis Ready Data.
1. [Analysis Ready Data Tutorial Part 2: Use Case 1](ard_2_use_case_1.ipynb) runs through the use case, preparing an NDVI time stack. This part includes a second notebook, [Analysis Ready Data Tutorial Part 2: Use Case 1 - Visualize Images](ard_2_use_case_1_visualize_images.ipynb), for visualizing the NDVI imagery.
