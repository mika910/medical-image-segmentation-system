import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from medpy.metric.binary import hd95, dc  # Import HD95 and Dice coefficient functions
from matplotlib import cm  # Import colormap module

# Set the backend to 'TkAgg' or 'Qt5Agg' for interactive plotting
# import matplotlib
# matplotlib.use('TkAgg')  # or 'Qt5Agg'

def prediction(gt_file, pred_file,slice_idx,save_file):

    # Load NIfTI images
    # gt_file = "./predictions_Acdc/patient001_frame01_gt.nii.gz"
    # pred_file = "./predictions_Acdc/patient001_frame01_pred.nii.gz"

    gt_img = nib.load(gt_file).get_fdata()
    pred_img = nib.load(pred_file).get_fdata()

    # Get number of slices
    slice_count = gt_img.shape[2]

    # Define organ labels and corresponding colors
    organ_labels = {
        1: "Right Ventricle",
        2: "Myocardium",
        3: "Left Ventricle"
    }

    # Get the 'jet' colormap
    jet_colormap = cm.get_cmap('jet')

    # Map prediction values to colors
    organ_colors = {
        organ_id: jet_colormap(organ_id / (len(organ_labels)))  # Normalize organ_id to [0, 1]
        for organ_id in organ_labels.keys()
    }

    # Function to calculate Dice and HD95 for a single slice
    def calculate_metrics(gt_slice, pred_slice):
        """
        Calculate Dice coefficient and HD95 for a single slice.

        Args:
            gt_slice (np.ndarray): Ground truth slice (2D array).
            pred_slice (np.ndarray): Prediction slice (2D array).

        Returns:
            dice (float): Dice coefficient.
            hd95 (float): Hausdorff Distance 95.
        """
        # Ensure the slices are binary (0s and 1s)
        gt_slice = (gt_slice > 0).astype(np.uint8)
        pred_slice = (pred_slice > 0).astype(np.uint8)

        # Calculate Dice coefficient
        dice = dc(gt_slice, pred_slice)

        # Calculate HD95 (skip if slices are empty)
        if np.any(gt_slice) and np.any(pred_slice):
            hd95_val = hd95(pred_slice, gt_slice)
        else:
            hd95_val = np.nan  # Handle empty slices

        return dice, hd95_val

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.2)  # Leave space for the slider

    # Display initial slice
    # slice_idx = slice_count // 2
    gt_slice = gt_img[:, :, slice_idx]
    pred_slice = pred_img[:, :, slice_idx]

    # Calculate metrics for the initial slice
    dice, hd95_val = calculate_metrics(gt_slice, pred_slice)

    # Show images
    img_display = ax.imshow(gt_slice, cmap="gray")
    overlay = ax.imshow(pred_slice, cmap="jet", alpha=0.7)
    ax.set_title(f"Slice {slice_idx}/{slice_count-1}\nDice: {dice:.4f}, HD95: {hd95_val:.4f}")
    ax.axis("off")

    # Add color legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=organ_colors[organ_id], label=organ_labels[organ_id]) for organ_id in organ_labels.keys()]
    ax.legend(handles=legend_elements, loc="upper right", title="Organs")

    # Add slider
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # Adjust position
    slider = Slider(ax_slider, "Slice", 0, slice_count-1, valinit=slice_idx, valfmt="%d")

    # Update function
    def update(val):
        slice_idx = int(slider.val)
        gt_slice = gt_img[:, :, slice_idx]
        pred_slice = pred_img[:, :, slice_idx]

        # Calculate metrics for the current slice
        dice, hd95_val = calculate_metrics(gt_slice, pred_slice)

        # Update the displayed slice and metrics
        img_display.set_data(gt_slice)
        overlay.set_data(pred_slice)
        ax.set_title(f"Slice {slice_idx}/{slice_count-1}\nDice: {dice:.4f}, HD95: {hd95_val:.4f}")
        fig.canvas.draw_idle()

    # Connect slider to update function
    slider.on_changed(update)

    # Ensure interactive mode works
    # plt.show(block=True)
    plt.savefig(save_file)