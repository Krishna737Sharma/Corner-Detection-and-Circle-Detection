# Image Processing Assignment - Corner Detection and Circle Detection

This repository contains solutions to the image processing assignment, which covers two main tasks: Harris Corner Detection and Hough Transform for Circle Detection. The tasks involve implementing algorithms from scratch, applying them to images, and comparing the results with OpenCV’s implementations.

## Tasks

### Task 1: Harris Corner Detection
- **Objective**: Implement the Harris Corner Detector algorithm from scratch and apply it to an image to detect corners.
  - **Step 1**: Implement the Harris Corner Detector algorithm.
  - **Step 2**: Apply the algorithm to detect corners in `boxes.png`.
  - **Step 3**: Visualize the detected corners by marking them on the image.
  - **Step 4**: Report the total number of corners detected.
  - **Step 5**: Compare the results with OpenCV’s Harris Corner Detector and explain any observed differences.

### Task 2: Hough Transform for Circle Detection
- **Objective**: Implement the Hough Transform for Circle Detection to detect circular shapes in an image.
  - **Step 1**: Use OpenCV’s Canny edge detector to generate the edge map from `clocks.png`.
  - **Step 2**: Implement the Hough Transform for circle detection from scratch using the edge map.
  - **Step 3**: Apply the algorithm to detect clocks in `clocks.png` and report the number of clocks detected.
  - **Step 4**: Visualize the detected circles by annotating them on the image.
  - **Step 5**: Compare your results with OpenCV’s Hough Circle Transform and explain any differences observed.

## Requirements
- Python 3.x
- NumPy
- OpenCV
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/Krishna737Sharma/image-processing-assignment.git
cd image-processing-assignment
