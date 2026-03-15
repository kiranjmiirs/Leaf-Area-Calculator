# 🍃 Leaf Area Calculator (Digital Planimetry)

Measuring the exact physical area of a leaf by hand is tedious and prone to human error. This project automates the process using a standard scanner, computer vision, and unsupervised machine learning. 

If you have a leaf and a scanner, this script will tell you exactly how many square centimeters that leaf is—down to the pixel!

## 🧠 How the "Magic" Works

We don't just look at the image; we mathematically tear it apart and rebuild it to get a perfect measurement. Here is the step-by-step pipeline:

1. **Color Separation (K-Means Clustering):** Instead of guessing what is a leaf and what is paper, we use K-Means to group every pixel by color. It perfectly separates the dark leaf from the bright white paper.
2. **Digital Glue (Morphological Closing):** Leaves aren't perfect. They have bright veins, shiny spots, and little cracks that the scanner picks up as "holes." We use a 5x5 kernel to act as digital glue—expanding the leaf to bridge the gaps, then shrinking it back down to its exact original size.
3. **The Solid Fill (Contour Filling):** To guarantee a perfect area calculation, the script traces the final outer boundary of the leaf and flood-fills the inside. 
4. **The Final Math:** Knowing the scans are exactly 300 DPI (Dots Per Inch), the script converts the final pixel count directly into square centimeters (cm²).

## 🚀 How to Use It

**1. Set up your environment**
Make sure you have the necessary libraries installed. 
```bash
pip install opencv-python numpy matplotlib scikit-learn
