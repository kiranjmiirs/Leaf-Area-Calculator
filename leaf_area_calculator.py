import os
import glob
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def calculate_leaf_area_robust(image_path, dpi=300):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    pixel_values = img_rgb.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixel_values)

    centers = kmeans.cluster_centers_
    leaf_cluster_label = np.argmin(np.mean(centers, axis=1))

    mask = (labels == leaf_cluster_label).astype(np.uint8)
    mask = mask.reshape(img_rgb.shape[:2])

    kernel = np.ones((5,5), np.uint8)
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(mask_closed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    mask_filled = np.zeros_like(mask) 
    mask_exact = np.zeros_like(mask)  
    
    min_leaf_area = 500  
    min_hole_area = 150  

    if hierarchy is not None:

        for i, cnt in enumerate(contours):
            parent_idx = hierarchy[0][i][3]
            if parent_idx == -1 and cv2.contourArea(cnt) > min_leaf_area:
                cv2.drawContours(mask_filled, [cnt], -1, 1, thickness=cv2.FILLED)
                cv2.drawContours(mask_exact, [cnt], -1, 1, thickness=cv2.FILLED)

        for i, cnt in enumerate(contours):
            parent_idx = hierarchy[0][i][3]
            if parent_idx != -1 and cv2.contourArea(cnt) > min_hole_area:
                cv2.drawContours(mask_exact, [cnt], -1, 0, thickness=cv2.FILLED)


    pixels_per_cm = dpi / 2.54
    area_per_pixel = (1 / pixels_per_cm) ** 2
    
    exact_area_cm2 = np.sum(mask_exact) * area_per_pixel
    filled_area_cm2 = np.sum(mask_filled) * area_per_pixel

    return img_rgb, mask, mask_exact, exact_area_cm2, mask_filled, filled_area_cm2

def batch_process_leaves(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    csv_file_path = os.path.join(output_dir, 'leaf_areas_report.csv')
    search_patterns = [os.path.join(input_dir, '*.tif'), os.path.join(input_dir, '*.tiff'), 
                       os.path.join(input_dir, '*.TIF'), os.path.join(input_dir, '*.TIFF')]
    
    image_paths = []
    for pattern in search_patterns:
        image_paths.extend(glob.glob(pattern))
        
    image_paths = list(set(image_paths)) 
        
    if not image_paths:
        print(f"No .tif or .tiff files found in {input_dir}")
        return

    print(f"Found {len(image_paths)} images. Starting processing...")
    csv_data = []

    for img_path in image_paths:
        filename = os.path.basename(img_path)
        base_name = os.path.splitext(filename)[0]
        print(f"Processing: {filename}...")
        
        try:

            original, noisy_mask, exact_mask, exact_area, filled_mask, filled_area = calculate_leaf_area_robust(img_path)

            csv_data.append([filename, round(exact_area, 4), round(filled_area, 4)])

            fig, ax = plt.subplots(1, 4, figsize=(20, 6))
            
            fig.suptitle(f"Sample: {base_name}", fontsize=20, fontweight='bold', color='darkblue')

            ax[0].imshow(original)
            ax[0].set_title("Original Image", fontsize=14)
            ax[0].axis('off')

            ax[1].imshow(noisy_mask, cmap='viridis')
            ax[1].set_title("Raw K-Means", fontsize=14)
            ax[1].axis('off')

            ax[2].imshow(exact_mask, cmap='plasma')
            ax[2].set_title(f"Exact Area (With Holes)\n{exact_area:.2f} cm²", fontsize=14, fontweight='bold', color='darkred')
            ax[2].axis('off')

            ax[3].imshow(filled_mask, cmap='plasma')
            ax[3].set_title(f"Filled Area (Holes Filled)\n{filled_area:.2f} cm²", fontsize=14, fontweight='bold', color='darkgreen')
            ax[3].axis('off')
            
            plt.tight_layout()
            
            plot_save_path = os.path.join(output_dir, f"{base_name}.png")
            plt.savefig(plot_save_path, bbox_inches='tight', dpi=150)
            plt.close(fig)

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            csv_data.append([filename, "ERROR", "ERROR"])

    print("\nWriting results to CSV...")
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Exact_Leaf_Area_cm2', 'Filled_Leaf_Area_cm2'])
        writer.writerows(csv_data)
        
    print(f"Batch processing complete! Check the results in:\n{output_dir}")

if __name__ == "__main__":
    print("========================================")
    print("      Leaf Area Calculator Tool         ")
    print("========================================")
    
    input_directory = input("Enter the path to the folder containing your .tif images:\n> ").strip()
    
    if input_directory.startswith('"') and input_directory.endswith('"'):
        input_directory = input_directory[1:-1]
        
    if not os.path.isdir(input_directory):
        print(f"\nError: The directory '{input_directory}' does not exist.")
    else:
        output_directory = os.path.join(input_directory, "results")
        print("\nStarting Batch Process...")
        batch_process_leaves(input_directory, output_directory)
        
    print("\nProcess Finished.")
    input("Press Enter to close this window...")