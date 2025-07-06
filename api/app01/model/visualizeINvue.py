
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


def get_slice_count(nii_file_path):
    """Return the number of slices in the NIfTI file."""
    img = nib.load(nii_file_path)
    return img.shape[2]


def visualize_slice_and_prediction(gt_file_path, pred_file_path,save_path, slice_idx=None):
    """
    Visualize a specific slice from the ground truth NIfTI file and overlay the prediction.

    Args:
        gt_file_path (str): Path to the ground truth NIfTI file.
        pred_file_path (str): Path to the prediction NIfTI file.
        slice_idx (int, optional): Index of the slice to visualize. Defaults to the middle slice.
    """
    # Load images
    gt_img = nib.load(gt_file_path).get_fdata()
    pred_img = nib.load(pred_file_path).get_fdata()



    # Get number of slices
    slice_count = gt_img.shape[2]

    # Set default slice index if not provided
    if slice_idx is None:
        slice_idx = slice_count // 2

    # Check if the slice index is within bounds
    if not (0 <= slice_idx < slice_count):
        print(f"Error: Slice index {slice_idx} out of range. Valid range: 0 to {slice_count - 1}.")
        return

    # Extract the slices
    gt_slice = gt_img[:, :, slice_idx]
    pred_slice = pred_img[:, :, slice_idx]

    # Plot ground truth and overlayed prediction
    plt.figure(figsize=(6, 6))
    plt.imshow(gt_slice, cmap="gray")
    plt.imshow(pred_slice, cmap="jet", alpha=0.5)  # Overlay prediction
    plt.colorbar()
    plt.title(f"Prediction Overlay on Ground Truth (Slice {slice_idx})")
    plt.axis("off")
    # plt.show()
    plt.savefig(save_path)

# Example usage
if __name__ == "__main__":
    # gt_file = "./predictions_Acdc/patient001_frame01_gt.nii.gz"
    # pred_file = "./predictions_Acdc/patient001_frame01_pred.nii.gz"
    gt_file = "./predictions/case0001_gt.nii.gz"
    pred_file = "./predictions/case0001_pred.nii.gz"

    # Get slice count
    slice_count = get_slice_count(gt_file)
    print(f"Number of slices in the ground truth file: {slice_count}")


    # Visualize a specific slice (e.g., middle slice)
    visualize_slice_and_prediction(gt_file, pred_file, slice_idx=None)

