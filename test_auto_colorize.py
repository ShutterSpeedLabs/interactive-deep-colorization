#!/usr/bin/env python
"""
Test script for auto-colorization from reference image.

This script demonstrates the automatic feature detection and color transfer
from a reference image to a grayscale image.

Usage:
    conda activate rvrt
    python test_auto_colorize.py --gray test_imgs/mortar_pestle.jpg --ref test_imgs/mortar_pestle.jpg
"""

import cv2
import numpy as np
import argparse
import sys
import os

# Add current directory to path
sys.path.append('.')

from auto_colorize_from_reference import AutoColorizeFromReference


def create_grayscale_version(color_image):
    """Create a grayscale version of a color image"""
    gray = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    return gray_rgb


def test_auto_colorize(gray_path, ref_path, method='orb', num_points=30):
    """Test auto-colorization"""
    
    print("="*70)
    print("Auto-Colorization Test")
    print("="*70)
    
    # Load images
    print(f"\n1. Loading images...")
    print(f"   Grayscale: {gray_path}")
    print(f"   Reference: {ref_path}")
    
    gray_img = cv2.imread(gray_path)
    ref_img = cv2.imread(ref_path)
    
    if gray_img is None:
        print(f"   ERROR: Could not load {gray_path}")
        return False
    
    if ref_img is None:
        print(f"   ERROR: Could not load {ref_path}")
        return False
    
    # Convert BGR to RGB
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB)
    ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)
    
    print(f"   ✓ Grayscale image: {gray_img.shape}")
    print(f"   ✓ Reference image: {ref_img.shape}")
    
    # If images are different sizes, resize reference
    if gray_img.shape[:2] != ref_img.shape[:2]:
        print(f"\n2. Resizing reference image to match grayscale...")
        ref_img = cv2.resize(ref_img, (gray_img.shape[1], gray_img.shape[0]))
        print(f"   ✓ Resized to: {ref_img.shape}")
    else:
        print(f"\n2. Images are same size ✓")
    
    # Initialize auto-colorizer
    print(f"\n3. Initializing auto-colorizer...")
    print(f"   Method: {method.upper()}")
    print(f"   Target points: {num_points}")
    
    auto_colorizer = AutoColorizeFromReference(
        method=method,
        num_points=num_points,
        match_threshold=0.75
    )
    print(f"   ✓ Initialized")
    
    # Extract color points
    print(f"\n4. Detecting features and matching...")
    color_points, vis_image = auto_colorizer.extract_color_points(
        gray_img, ref_img, visualize=True
    )
    
    if len(color_points) == 0:
        print(f"   ✗ No color points extracted!")
        return False
    
    print(f"   ✓ Extracted {len(color_points)} color points")
    
    # Analyze color points
    print(f"\n5. Analyzing color points...")
    
    # Calculate color distribution
    colors = np.array([c[2:] for c in color_points])  # Extract RGB values
    mean_color = np.mean(colors, axis=0)
    std_color = np.std(colors, axis=0)
    
    print(f"   Mean color: RGB({mean_color[0]:.1f}, {mean_color[1]:.1f}, {mean_color[2]:.1f})")
    print(f"   Color std:  RGB({std_color[0]:.1f}, {std_color[1]:.1f}, {std_color[2]:.1f})")
    
    # Calculate spatial distribution
    positions = np.array([c[:2] for c in color_points])  # Extract x, y
    mean_pos = np.mean(positions, axis=0)
    
    print(f"   Mean position: ({mean_pos[0]:.1f}, {mean_pos[1]:.1f})")
    print(f"   Position range: X=[{positions[:,0].min()}, {positions[:,0].max()}], Y=[{positions[:,1].min()}, {positions[:,1].max()}]")
    
    # Save results
    print(f"\n6. Saving results...")
    
    # Save color points
    output_txt = 'test_color_points.txt'
    with open(output_txt, 'w') as f:
        f.write("# x, y, r, g, b\n")
        for x, y, r, g, b in color_points:
            f.write(f"{x}, {y}, {r}, {g}, {b}\n")
    print(f"   ✓ Saved color points to: {output_txt}")
    
    # Save visualization
    if vis_image is not None:
        output_vis = 'test_auto_colorize_visualization.png'
        cv2.imwrite(output_vis, cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR))
        print(f"   ✓ Saved visualization to: {output_vis}")
    
    # Create a preview with color points marked
    preview = gray_img.copy()
    for x, y, r, g, b in color_points:
        cv2.circle(preview, (x, y), 5, (int(r), int(g), int(b)), -1)
        cv2.circle(preview, (x, y), 6, (255, 255, 255), 1)
    
    output_preview = 'test_auto_colorize_preview.png'
    cv2.imwrite(output_preview, cv2.cvtColor(preview, cv2.COLOR_RGB2BGR))
    print(f"   ✓ Saved preview to: {output_preview}")
    
    # Print sample points
    print(f"\n7. Sample color points (first 10):")
    for i, (x, y, r, g, b) in enumerate(color_points[:10]):
        print(f"   {i+1:2d}. Position ({x:3d}, {y:3d}) -> Color RGB({r:3d}, {g:3d}, {b:3d})")
    
    if len(color_points) > 10:
        print(f"   ... and {len(color_points) - 10} more points")
    
    # Summary
    print(f"\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Status: ✓ SUCCESS")
    print(f"Color points extracted: {len(color_points)}")
    print(f"Output files:")
    print(f"  - {output_txt}")
    print(f"  - {output_vis}")
    print(f"  - {output_preview}")
    print("="*70)
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Test auto-colorization from reference')
    parser.add_argument('--gray', type=str, help='Grayscale image path')
    parser.add_argument('--ref', type=str, help='Reference color image path')
    parser.add_argument('--method', type=str, default='orb', choices=['orb', 'sift', 'akaze'],
                        help='Feature detection method')
    parser.add_argument('--num_points', type=int, default=30, help='Number of color points')
    parser.add_argument('--create_gray', action='store_true', 
                        help='Create grayscale version from reference (for testing)')
    
    args = parser.parse_args()
    
    # If no arguments provided, use default test
    if args.gray is None and args.ref is None:
        print("No images provided. Using default test image...")
        
        # Check if test image exists
        test_img = 'test_imgs/mortar_pestle.jpg'
        if not os.path.exists(test_img):
            print(f"Error: Test image not found: {test_img}")
            print("\nUsage:")
            print("  python test_auto_colorize.py --gray <gray_image> --ref <ref_image>")
            return
        
        # Load test image
        ref_img = cv2.imread(test_img)
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)
        
        # Create grayscale version
        gray_img = create_grayscale_version(ref_img)
        
        # Save temporary files
        cv2.imwrite('temp_gray.jpg', cv2.cvtColor(gray_img, cv2.COLOR_RGB2BGR))
        cv2.imwrite('temp_ref.jpg', cv2.cvtColor(ref_img, cv2.COLOR_RGB2BGR))
        
        print(f"Created grayscale version from: {test_img}")
        
        # Run test
        success = test_auto_colorize('temp_gray.jpg', 'temp_ref.jpg', args.method, args.num_points)
        
        # Cleanup
        os.remove('temp_gray.jpg')
        os.remove('temp_ref.jpg')
        
    else:
        if args.gray is None or args.ref is None:
            print("Error: Both --gray and --ref are required")
            return
        
        # If create_gray flag is set, create grayscale from reference
        if args.create_gray:
            print("Creating grayscale version from reference image...")
            ref_img = cv2.imread(args.ref)
            ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)
            gray_img = create_grayscale_version(ref_img)
            
            gray_path = args.gray.replace('.jpg', '_gray.jpg').replace('.png', '_gray.png')
            cv2.imwrite(gray_path, cv2.cvtColor(gray_img, cv2.COLOR_RGB2BGR))
            print(f"Saved grayscale version to: {gray_path}")
            
            args.gray = gray_path
        
        # Run test
        success = test_auto_colorize(args.gray, args.ref, args.method, args.num_points)
    
    if success:
        print("\n✓ Test completed successfully!")
        print("\nNext steps:")
        print("1. Open the visualization image to see feature matches")
        print("2. Open the preview image to see color points on grayscale")
        print("3. Use the GUI to apply these colors:")
        print("   conda activate rvrt")
        print("   python ideepcolor.py --gpu 0 --backend pytorch")
    else:
        print("\n✗ Test failed!")


if __name__ == '__main__':
    main()
