#!/usr/bin/env python
"""
Masked region colorization - Apply colors only to specific masked regions.

This module allows selective colorization of specific regions defined by a mask.

Usage:
    conda activate rvrt
    python masked_colorization.py --gray input.jpg --mask mask.png --colors colors.txt
"""

import cv2
import numpy as np
import argparse
from skimage import color as skcolor


def load_mask(mask_path, target_shape):
    """
    Load and process mask image
    
    Args:
        mask_path: Path to mask image (white=colorize, black=keep grayscale)
        target_shape: Target shape (H, W)
        
    Returns:
        Binary mask (H, W) with 1=colorize, 0=keep grayscale
    """
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise ValueError(f"Could not load mask: {mask_path}")
    
    # Resize to target shape
    if mask.shape != target_shape:
        mask = cv2.resize(mask, (target_shape[1], target_shape[0]), 
                         interpolation=cv2.INTER_NEAREST)
    
    # Threshold to binary (>128 = colorize)
    mask_binary = (mask > 128).astype(np.float32)
    
    return mask_binary


def apply_masked_colorization(gray_image, colorized_image, mask):
    """
    Apply colorization only to masked regions
    
    Args:
        gray_image: Grayscale image (H, W, 3)
        colorized_image: Fully colorized image (H, W, 3)
        mask: Binary mask (H, W) with 1=colorize, 0=keep grayscale
        
    Returns:
        Result image with selective colorization
    """
    # Expand mask to 3 channels
    mask_3ch = mask[:, :, np.newaxis]
    
    # Blend: result = mask * colorized + (1-mask) * grayscale
    result = (mask_3ch * colorized_image + 
              (1 - mask_3ch) * gray_image).astype(np.uint8)
    
    return result


def create_smooth_mask(mask, blur_size=15):
    """
    Create smooth mask with feathered edges
    
    Args:
        mask: Binary mask (H, W)
        blur_size: Gaussian blur kernel size (odd number)
        
    Returns:
        Smooth mask with values 0-1
    """
    # Ensure odd kernel size
    if blur_size % 2 == 0:
        blur_size += 1
    
    # Apply Gaussian blur for smooth transition
    smooth_mask = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    
    return smooth_mask


def extract_region_colors(image, mask, num_samples=10):
    """
    Extract representative colors from masked region
    
    Args:
        image: Color image (H, W, 3)
        mask: Binary mask (H, W)
        num_samples: Number of color samples to extract
        
    Returns:
        List of (x, y, r, g, b) tuples
    """
    # Get coordinates of masked region
    y_coords, x_coords = np.where(mask > 0.5)
    
    if len(x_coords) == 0:
        return []
    
    # Sample points uniformly
    num_points = min(num_samples, len(x_coords))
    indices = np.linspace(0, len(x_coords)-1, num_points, dtype=int)
    
    color_points = []
    for idx in indices:
        x = int(x_coords[idx])
        y = int(y_coords[idx])
        r, g, b = image[y, x]
        color_points.append((x, y, int(r), int(g), int(b)))
    
    return color_points


def main():
    parser = argparse.ArgumentParser(description='Masked region colorization')
    parser.add_argument('--gray', type=str, required=True, help='Grayscale image')
    parser.add_argument('--colorized', type=str, required=True, help='Fully colorized image')
    parser.add_argument('--mask', type=str, required=True, help='Mask image (white=colorize)')
    parser.add_argument('--output', type=str, default='masked_result.png', help='Output image')
    parser.add_argument('--smooth', action='store_true', help='Use smooth mask edges')
    parser.add_argument('--blur_size', type=int, default=15, help='Blur size for smooth edges')
    
    args = parser.parse_args()
    
    print("="*70)
    print("Masked Region Colorization")
    print("="*70)
    
    # Load images
    print("\n1. Loading images...")
    gray_img = cv2.imread(args.gray)
    colorized_img = cv2.imread(args.colorized)
    
    if gray_img is None:
        print(f"Error: Could not load {args.gray}")
        return
    
    if colorized_img is None:
        print(f"Error: Could not load {args.colorized}")
        return
    
    # Convert to RGB
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB)
    colorized_img = cv2.cvtColor(colorized_img, cv2.COLOR_BGR2RGB)
    
    print(f"   Grayscale: {gray_img.shape}")
    print(f"   Colorized: {colorized_img.shape}")
    
    # Ensure same size
    if gray_img.shape != colorized_img.shape:
        print("   Resizing colorized to match grayscale...")
        colorized_img = cv2.resize(colorized_img, 
                                   (gray_img.shape[1], gray_img.shape[0]))
    
    # Load mask
    print("\n2. Loading mask...")
    mask = load_mask(args.mask, gray_img.shape[:2])
    print(f"   Mask: {mask.shape}")
    print(f"   Masked pixels: {np.sum(mask > 0.5)}/{mask.size} ({100*np.mean(mask):.1f}%)")
    
    # Smooth mask if requested
    if args.smooth:
        print(f"\n3. Smoothing mask edges (blur_size={args.blur_size})...")
        mask = create_smooth_mask(mask, args.blur_size)
        print(f"   Smooth mask created")
    
    # Apply masked colorization
    print("\n4. Applying masked colorization...")
    result = apply_masked_colorization(gray_img, colorized_img, mask)
    print(f"   Result: {result.shape}")
    
    # Save result
    print(f"\n5. Saving result to {args.output}...")
    cv2.imwrite(args.output, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    print(f"   Saved!")
    
    # Save mask visualization
    mask_vis_path = args.output.replace('.png', '_mask.png')
    mask_vis = (mask * 255).astype(np.uint8)
    cv2.imwrite(mask_vis_path, mask_vis)
    print(f"   Saved mask visualization to {mask_vis_path}")
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"Status: ✓ SUCCESS")
    print(f"Output: {args.output}")
    print(f"Mask visualization: {mask_vis_path}")
    print("="*70)


if __name__ == '__main__':
    main()
