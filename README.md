# 🍃 Leaf Area Calculator (Batch Digital Planimetry)

Measuring the exact physical area of a leaf by hand is tedious and prone to human error. This tool automates the process using a standard scanner, computer vision, and unsupervised machine learning. If you have scanned leaves, this script will tell you exactly how many square centimeters they are—down to the pixel!

## 🧠 How the "Magic" Works

We don't just look at the image; we mathematically reconstruct it to get a perfect measurement. Here is the step-by-step pipeline:

* **Color Separation (K-Means Clustering):** We use K-Means to group every pixel by color, perfectly separating dark leaves from the bright white paper.
* **Digital Glue (Morphological Closing):** Leaves have shiny spots and tiny cracks. We use a 5x5 kernel to act as digital glue, bridging tiny gaps while maintaining the leaf's exact boundary.
* **Ecological Dual-Output:** The algorithm maps both outer boundaries and inner holes to calculate two metrics: **Exact Area** (photosynthetic surface with holes subtracted) and **Filled Area** (biological cost to plant with holes filled).
* **The Final Math:** Knowing the scans are exactly 300 DPI, the script converts the final pixel count directly into square centimeters (cm²).

## 🛠️ Prerequisites & Setup

This tool requires Python. Built-in modules like `os`, `glob`, and `csv` are already included, but you will need to install a few external data science libraries.

1. Open your command prompt or terminal.
2. Install the required dependencies by running:

   ```bash
   pip install opencv-python numpy matplotlib scikit-learn
   ```

3. Download or save the provided script as `leaf_area_calculator.py`.

## 🚀 How to Run the Batch Processor

This tool is designed to run freely and process entire folders of `.tif` or `.tiff` scans automatically.

1. Open your terminal and run the script:

   ```bash
   python leaf_area_calculator.py
   ```

   (or double-click the `.py` file if your system allows it).

2. A prompt will appear asking for the folder path. Paste the path to the folder containing your images and press Enter.
3. The script will automatically create a new `results` folder inside that directory.
4. It will process every image, generating a visual `.png` validation plot for each scan and a single `leaf_areas_report.csv` containing the measurements for your entire dataset.

## 📊 CSV Output Structure

The generated `leaf_areas_report.csv` file will contain three columns for your ecological analysis:

| Filename | Exact_Leaf_Area_cm2 | Filled_Leaf_Area_cm2 |
|---|---|---|
| sample_scan_01.tif | 81.95 | 83.12 |
| sample_scan_02.tif | 204.70 | 221.45 |

* **Exact_Leaf_Area_cm2:** The actual current surface area of the leaf (holes caused by herbivory or damage are subtracted). Useful for stomatal conductance and photosynthesis models.
* **Filled_Leaf_Area_cm2:** The original morphological surface area of the leaf (internal holes are treated as solid leaf). Useful as a proxy for the carbon/biological cost to the plant.
