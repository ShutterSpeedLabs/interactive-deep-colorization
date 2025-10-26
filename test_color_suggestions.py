#!/usr/bin/env python
import sys
import numpy as np
sys.path.append('./caffe_files')
from data import colorize_image as CI
import cv2
from skimage import color

# Load models
print("Loading colorization model...")
colorModel = CI.ColorizeImageTorch(Xd=256, maskcent=False)
colorModel.prep_net(path='./models/pytorch/caffemodel.pth')

print("Loading distribution model...")
distModel = CI.ColorizeImageTorchDist(Xd=256, maskcent=False)
distModel.prep_net(path='./models/pytorch/caffemodel.pth', dist=True)

# Load test image
print("Loading test image...")
image_file = './test_imgs/mortar_pestle.jpg'
im_bgr = cv2.imread(image_file)
im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
im_rgb_resized = cv2.resize(im_rgb, (256, 256), interpolation=cv2.INTER_CUBIC)

# Set image in models
print("Setting image in models...")
colorModel.load_image(image_file)
distModel.set_image(im_rgb_resized)

# Create dummy input (no hints)
im_ab0 = np.zeros((2, 256, 256))
im_mask0 = np.zeros((1, 256, 256))

# Run distribution model
print("Running distribution model...")
distModel.net_forward(im_ab0, im_mask0)

# Get color recommendations at center
h, w = 128, 128
print(f"Getting color recommendations at position ({h}, {w})...")
ab_reccs, conf = distModel.get_ab_reccs(h=h, w=w, K=9, N=25000, return_conf=True)

print(f"Got {len(ab_reccs)} color recommendations:")
print(f"AB values shape: {ab_reccs.shape}")
print(f"Confidence values: {conf}")

# Convert to RGB
im_lab = color.rgb2lab(im_rgb_resized)
L = np.tile(im_lab[h, w, 0], (9, 1))
colors_lab = np.concatenate((L, ab_reccs), axis=1)
colors_lab3 = colors_lab[:, np.newaxis, :]
colors_rgb = np.clip(np.squeeze(color.lab2rgb(colors_lab3)), 0, 1)

print(f"RGB colors shape: {colors_rgb.shape}")
print("RGB colors (first 3):")
for i in range(min(3, len(colors_rgb))):
    print(f"  Color {i}: RGB({colors_rgb[i,0]:.3f}, {colors_rgb[i,1]:.3f}, {colors_rgb[i,2]:.3f})")

print("\nColor suggestion test completed successfully!")
