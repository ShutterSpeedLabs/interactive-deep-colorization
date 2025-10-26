#!/usr/bin/env python
import sys
import torch
import numpy as np
sys.path.append('./caffe_files')
from data import colorize_image as CI

print("=" * 70)
print("GPU AVAILABILITY TEST")
print("=" * 70)

# Check CUDA availability
print(f"\nPyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    print(f"Current GPU: {torch.cuda.current_device()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")

print("\n" + "=" * 70)
print("LOADING MODELS")
print("=" * 70)

# Load colorization model
print("\n1. Loading colorization model...")
colorModel = CI.ColorizeImageTorch(Xd=256, maskcent=False)
colorModel.prep_net(gpu_id=0, path='./models/pytorch/caffemodel.pth')

# Check if model is on GPU
device = next(colorModel.net.parameters()).device
print(f"   Model device: {device}")

# Load distribution model
print("\n2. Loading distribution model...")
distModel = CI.ColorizeImageTorchDist(Xd=256, maskcent=False)
distModel.prep_net(gpu_id=0, path='./models/pytorch/caffemodel.pth', dist=True)

# Check if model is on GPU
device = next(distModel.net.parameters()).device
print(f"   Model device: {device}")

print("\n" + "=" * 70)
print("TESTING INFERENCE")
print("=" * 70)

# Load test image
print("\nLoading test image...")
image_file = './test_imgs/mortar_pestle.jpg'
colorModel.load_image(image_file)

# Create dummy input
im_ab0 = np.zeros((2, 256, 256))
im_mask0 = np.zeros((1, 256, 256))

# Test forward pass
print("Running forward pass...")
import time
start = time.time()
result = colorModel.net_forward(im_ab0, im_mask0)
end = time.time()

print(f"Forward pass completed in {end - start:.3f} seconds")
print(f"Result shape: {result.shape if hasattr(result, 'shape') else 'N/A'}")

# Check GPU memory usage
if torch.cuda.is_available():
    print(f"\nGPU Memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
    print(f"GPU Memory cached: {torch.cuda.memory_reserved(0) / 1024**2:.2f} MB")

print("\n" + "=" * 70)
print("TEST COMPLETED SUCCESSFULLY!")
print("=" * 70)
