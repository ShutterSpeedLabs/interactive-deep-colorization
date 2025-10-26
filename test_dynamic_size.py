#!/usr/bin/env python
"""
Test script to demonstrate dynamic image size colorization.
This script shows how to use the --use_dynamic_size flag to pass
actual image dimensions to the model instead of resizing to 256x256.

Usage:
    conda activate rvrt
    python test_dynamic_size.py --image test_imgs/mortar_pestle.jpg --backend pytorch
"""

import sys
import argparse
import numpy as np
import cv2
from data import colorize_image as CI

def test_dynamic_size():
    parser = argparse.ArgumentParser(description='Test dynamic size colorization')
    parser.add_argument('--image', type=str, required=True, help='Input image path')
    parser.add_argument('--backend', type=str, default='pytorch', choices=['caffe', 'pytorch'])
    parser.add_argument('--gpu', type=int, default=0, help='GPU ID (-1 for CPU)')
    parser.add_argument('--model', type=str, default='./models/pytorch/caffemodel.pth', 
                        help='Model path')
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Testing Dynamic Size Colorization")
    print("="*60)
    
    # Read image to get dimensions
    img = cv2.imread(args.image)
    if img is None:
        print(f"Error: Could not read image {args.image}")
        return
    
    h, w = img.shape[:2]
    print(f"\nOriginal image size: {w}x{h}")
    
    # Test 1: Fixed size (256x256)
    print("\n" + "-"*60)
    print("Test 1: Fixed size mode (256x256)")
    print("-"*60)
    
    if args.backend == 'pytorch':
        model_fixed = CI.ColorizeImageTorch(Xd=256, use_dynamic_size=False)
        model_fixed.prep_net(gpu_id=args.gpu, path=args.model)
    else:
        print("Caffe backend not tested in this script")
        return
    
    model_fixed.load_image(args.image)
    print(f"Model input size: {model_fixed.img_rgb.shape[1]}x{model_fixed.img_rgb.shape[0]}")
    print(f"Model img_l shape: {model_fixed.img_l.shape}")
    
    # Create dummy input for forward pass
    im_ab = np.zeros((2, model_fixed.img_rgb.shape[0], model_fixed.img_rgb.shape[1]))
    im_mask = np.zeros((1, model_fixed.img_rgb.shape[0], model_fixed.img_rgb.shape[1]))
    
    result_fixed = model_fixed.net_forward(im_ab, im_mask)
    print(f"Output shape: {result_fixed.shape}")
    
    # Test 2: Dynamic size (actual dimensions)
    print("\n" + "-"*60)
    print("Test 2: Dynamic size mode (actual dimensions)")
    print("-"*60)
    
    if args.backend == 'pytorch':
        model_dynamic = CI.ColorizeImageTorch(Xd=256, use_dynamic_size=True)
        model_dynamic.prep_net(gpu_id=args.gpu, path=args.model)
    
    model_dynamic.load_image(args.image)
    print(f"Model input size: {model_dynamic.img_rgb.shape[1]}x{model_dynamic.img_rgb.shape[0]}")
    print(f"Model img_l shape: {model_dynamic.img_l.shape}")
    print(f"Current dimensions: {model_dynamic.current_w}x{model_dynamic.current_h}")
    
    # Create dummy input for forward pass with dynamic size
    im_ab_dyn = np.zeros((2, model_dynamic.img_rgb.shape[0], model_dynamic.img_rgb.shape[1]))
    im_mask_dyn = np.zeros((1, model_dynamic.img_rgb.shape[0], model_dynamic.img_rgb.shape[1]))
    
    result_dynamic = model_dynamic.net_forward(im_ab_dyn, im_mask_dyn)
    print(f"Output shape: {result_dynamic.shape}")
    
    print("\n" + "="*60)
    print("Summary:")
    print("="*60)
    print(f"Original image: {w}x{h}")
    print(f"Fixed mode output: {result_fixed.shape[1]}x{result_fixed.shape[0]}")
    print(f"Dynamic mode output: {result_dynamic.shape[1]}x{result_dynamic.shape[0]}")
    print("\nDynamic mode preserves aspect ratio and uses actual dimensions!")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_dynamic_size()
