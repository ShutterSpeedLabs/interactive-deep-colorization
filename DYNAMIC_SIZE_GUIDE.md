# Dynamic Image Size Feature

## Overview

By default, the colorization model resizes all input images to a fixed size (256x256) before processing. This new feature allows you to pass the actual image dimensions to the model instead, preserving the original aspect ratio and potentially improving quality for non-square images.

## Usage

### Command Line

First, activate the conda environment:

```bash
conda activate rvrt
```

Then add the `--use_dynamic_size` flag when running the application:

```bash
# Using PyTorch backend with dynamic sizing
python ideepcolor.py --use_dynamic_size --image_file test_imgs/mortar_pestle.jpg

# Using Caffe backend with dynamic sizing
python ideepcolor.py --use_dynamic_size --backend caffe --image_file test_imgs/mortar_pestle.jpg

# Specify GPU
python ideepcolor.py --use_dynamic_size --gpu 0 --image_file test_imgs/mortar_pestle.jpg

# CPU mode
python ideepcolor.py --use_dynamic_size --cpu_mode --image_file test_imgs/mortar_pestle.jpg
```

### How It Works

**Fixed Size Mode (Default):**
- All images are resized to `load_size x load_size` (default: 256x256)
- Aspect ratio is not preserved
- Faster processing for very large images

**Dynamic Size Mode (`--use_dynamic_size`):**
- Images are resized to preserve aspect ratio
- Dimensions are adjusted to be divisible by 4 (required by the model)
- Original proportions are maintained
- Better quality for non-square images

### Example

For an image with original size 800x600:

**Fixed mode:**
- Input to model: 256x256 (aspect ratio changed)

**Dynamic mode:**
- Input to model: 800x600 (rounded to nearest multiple of 4)
- Aspect ratio preserved

## Testing

A test script is provided to compare both modes:

```bash
conda activate rvrt
python test_dynamic_size.py --image test_imgs/mortar_pestle.jpg --backend pytorch
```

This will show:
- Original image dimensions
- Model input size in fixed mode
- Model input size in dynamic mode
- Output dimensions for both modes

## Implementation Details

### Modified Files

1. **data/colorize_image.py**
   - Added `use_dynamic_size` parameter to all colorization classes
   - Modified `load_image()` and `set_image()` to handle dynamic sizing
   - Updated dimension tracking with `current_h` and `current_w` attributes

2. **ideepcolor.py**
   - Added `--use_dynamic_size` command line argument
   - Passes flag to model initialization

3. **ui/gui_draw.py**
   - Updated to track actual model input size
   - Modified point scaling to work with dynamic dimensions

4. **ui/ui_control.py**
   - Added `actual_load_size` parameter
   - Updated coordinate transformations for dynamic sizing

### Key Changes

- Images are resized to `(w//4)*4 x (h//4)*4` to ensure dimensions are divisible by 4
- The `Xd` parameter is updated to `max(h, w)` for compatibility
- All coordinate transformations account for actual dimensions
- Distribution arrays are dynamically allocated based on actual size

## Limitations

- Very large images may require more GPU memory
- Processing time increases with image size
- Model was trained on 256x256 images, so results may vary with very different sizes

## Recommendations

- Use dynamic sizing for:
  - Non-square images
  - Images where aspect ratio is important
  - High-resolution images where you want to preserve detail

- Use fixed sizing for:
  - Batch processing of many images
  - Limited GPU memory
  - Consistent processing time requirements

## Performance Considerations

Dynamic sizing will:
- Use more GPU memory for larger images
- Take longer to process larger images
- Produce better results for images with important aspect ratios

Example memory usage (approximate):
- 256x256: ~500MB GPU memory
- 512x512: ~1GB GPU memory
- 1024x1024: ~2GB GPU memory
