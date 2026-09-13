# 🍃 Leaf Area Calculator (Batch Digital Planimetry)

Measuring the exact physical area of a leaf by hand is tedious and prone to human error. This tool automates the process using a standard scanner, computer vision, and unsupervised machine learning. If you have scanned leaves, this script will tell you exactly how many square centimeters they are—down to the pixel!

## 🧠 How the "Magic" Works

We don't just look at the image; we mathematically reconstruct it to get a perfect measurement. Here is the step-by-step pipeline:

*   **Color Separation (K-Means Clustering):** We use K-Means to group every pixel by color, perfectly separating dark leaves from the bright white paper.
*   **Digital Glue (Morphological Closing):** Leaves have shiny spots and tiny cracks. We use a 5x5 kernel to act as digital glue, bridging tiny gaps while maintaining the leaf's exact boundary.
*   **Ecological Dual-Output:** The algorithm maps both outer boundaries and inner holes to calculate two metrics: **Exact Area** (photosynthetic surface with holes subtracted) and **Filled Area** (biological cost to plant with holes filled).
*   **The Final Math:** Knowing the scans are exactly 300 DPI, the script converts the final pixel count directly into square centimeters (cm²).

## 🛠️ Prerequisites & Setup

This tool requires Python. Built-in modules like `os`, `glob`, and `csv` are already included, but you will need to install a few external data science libraries. 

1. Open your command prompt or terminal.
2. Install the required dependencies by running:
   ```bash
   pip install opencv-python numpy matplotlib scikit-learn
