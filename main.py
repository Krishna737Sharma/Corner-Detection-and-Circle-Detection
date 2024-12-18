# **TASK-1**
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

"""# **Scratch**"""

# Calculate image gradients
def compute_gradients(image, kernel_x, kernel_y):
    grad_x = cv2.filter2D(image, ddepth=-1, kernel=kernel_x)
    grad_y = cv2.filter2D(image, ddepth=-1, kernel=kernel_y)
    return grad_x, grad_y

# Apply Gaussian filter
def gaussian_smooth(grad_x, grad_y):
    gaussian_kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
    gx2 = grad_x * grad_x
    gy2 = grad_y ** 2
    gxgy = grad_x * grad_y
    smoothed_gx = cv2.filter2D(gx2, ddepth=-1, kernel=gaussian_kernel)
    smoothed_gy = cv2.filter2D(gy2, ddepth=-1, kernel=gaussian_kernel)
    smoothed_gx_gy = cv2.filter2D(gxgy, ddepth=-1, kernel=gaussian_kernel)
    return smoothed_gx, smoothed_gy, smoothed_gx_gy

# Compute Harris response

def harris_response(image, k_factor):
    grad_x, grad_y = compute_gradients(image, np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]), np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]))
    Ixx, Iyy, Ixy = gaussian_smooth(grad_x, grad_y)
    det_M = (Ixx * Iyy) - (Ixy**2)
    trace_M = Ixx + Iyy
    response = det_M - k_factor * (trace_M**2)
    return response

def extract_corners(image, threshold_value, k_factor):
    R = harris_response(image, k_factor)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(np.uint8(R > threshold_value))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    return cv2.cornerSubPix(image, np.float32(centroids), (5,5), (-1,-1), criteria)

def draw_harris_corners(image, corners):
    for corner in corners:
        x, y = corner.ravel()
        x, y = int(round(x)), int(round(y))
        cv2.circle(image, (x, y), radius=3, color=(255, 0, 0), thickness=-1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

def main():
    image = cv2.imread('/content/boxes.png', cv2.IMREAD_GRAYSCALE)
    image = np.float32(image)
    min_val = np.min(image)
    max_val = np.max(image)
    image = (image - min_val) / (max_val - min_val)

    corners = extract_corners(image, 0.01, 0.04)
    draw_harris_corners(cv2.imread('boxes.png'), corners)
    print("The number of corners detected is:", len(corners))

if __name__ == "__main__":
    main()

"""# **Opencv**"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('boxes.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)
dst = cv2.dilate(dst, None)
image[dst > 0.01 * dst.max()] = (0, 0, 255)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
print("The number of corners detected by OpenCV is:", np.sum(dst > 0.01 * dst.max()))



"""# **Task-2**"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

imag= cv.imread('/content/clocks.png', cv.IMREAD_GRAYSCALE)
img=cv.resize(imag,(128,128))
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

"""# **OpenCV**"""

import cv2
import numpy as np
from google.colab.patches import cv2_imshow

# Load clock image
def load_image(path):
    return cv2.imread(path)

clocks = load_image('/content/clocks.png')

# Preprocess image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    return cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

preprocessed_img = preprocess_image(clocks)

# Detect circles using Hough Circle Transform
def detect_circles(image):
    return cv2.HoughCircles(image[:, :, 0], cv2.HOUGH_GRADIENT, dp=1, minDist=90, param1=55, param2=60, minRadius=8, maxRadius=75)

circles = detect_circles(preprocessed_img)

# Draw detected circles
def draw_circles(image, circles):
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x, y, r in circles[0]:
            cv2.circle(image, (x, y), r, (0, 255, 0), 6)  # Outer circle
            cv2.circle(image, (x, y), 2, (0, 0, 255), 3)    # Inner circle
    return image

clocks_with_circles = draw_circles(clocks, circles)

# Count total circles (outer and inner)
def count_circles(circles):
    if circles is not None:
        outer_circles = circles.shape[1]
        inner_circles = outer_circles  # Assuming one inner circle per outer circle
        total_circles = outer_circles + inner_circles
        return total_circles
    else:
        return 0

total_circles = count_circles(circles)
plt.imshow(cv2.cvtColor(clocks_with_circles, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
# Print total circle count
print("Total circles detected:", total_circles)

"""# **Scratch**"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Step 2: Hough Circle Transform from Scratch
def hough_circle_transform_scratch(edges, dp, minDist, param2, minRadius, maxRadius):
    rows, cols = edges.shape

    # Accumulator array
    max_radius = maxRadius if maxRadius > 0 else min(max(rows, cols) // 2, 50)  # Limit max radius to a sensible value
    accumulator = np.zeros((rows, cols, max_radius), dtype=np.uint64)

    # Edge points
    edge_points = np.argwhere(edges > 0)

    # Precompute sin and cos values for angles
    angles = np.arange(0, 360, step=1)  # Higher precision with angle step size of 1 degree
    sin_table = np.sin(np.deg2rad(angles))
    cos_table = np.cos(np.deg2rad(angles))

    # Fill accumulator based on edge points and circle equations
    for r in range(minRadius, max_radius):
        for x, y in edge_points:
            for sin_val, cos_val in zip(sin_table, cos_table):
                a = int(x - r * cos_val / dp)  # Adjust by dp
                b = int(y - r * sin_val / dp)

                if 0 <= a < rows and 0 <= b < cols:
                    accumulator[a, b, r] += 1

    return accumulator

# Step 3: Detect Circles from Accumulator Array
def detect_circles_scratch(accumulator, param2, minDist):
    circles = []
    rows, cols, radii_range = accumulator.shape

    for r in range(radii_range):
        for a in range(rows):
            for b in range(cols):
                if accumulator[a, b, r] >= param2:  # Threshold for circle detection
                    # Ensure minimum distance between detected circles
                    too_close = False
                    for (a_, b_, r_) in circles:
                        if np.sqrt((a - a_)**2 + (b - b_)**2) < minDist:
                            too_close = True
                            break
                    if not too_close:
                        circles.append((a, b, r))
    return circles

# Step 4: Draw Detected Circles
def draw_circles_scratch(image, circles):
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for a, b, r in circles:
        cv2.circle(output_image, (b, a), r, (0, 255, 0), 2)   # Draw outer circle
        cv2.circle(output_image, (b, a), 1, (0, 0, 255), 3)   # Draw smaller center of circle
    return output_image

# Main function to apply Hough Circle Transform from scratch
def main():
    file_path = '/content/clocks.png'
    assert os.path.exists(file_path), "File not found! Check the path."

    # Step 2: Apply Hough Circle Transform from scratch
    dp = 1
    minDist = 20
    param2 = 30
    minRadius = 0
    maxRadius = 0

    accumulator = hough_circle_transform_scratch(edges, dp, minDist, param2, minRadius, maxRadius)

    # Step 3: Detect circles
    circles = detect_circles_scratch(accumulator, param2, minDist)

    # Step 4: Draw detected circles
    output_image = draw_circles_scratch(img, circles)

    # Display results
    print(f"Number of circles detected: {len(circles)}")

    plt.subplot(121), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(122), plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Circles'), plt.xticks([]), plt.yticks([])

    plt.show()

# Run the algorithm
main()
