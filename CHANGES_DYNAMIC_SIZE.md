# Changes Summary: Dynamic Image Size Feature

## Overview
Modified the colorization system to support passing actual image dimensions to the model instead of always resizing to 256x256.

## New Command Line Option

```bash
--use_dynamic_size    Use actual image dimensions instead of fixed load_size
```

## Modified Files

### 1. data/colorize_image.py

**ColorizeImageBase class:**
- Added `use_dynamic_size` parameter to `__init__()`
- Modified `load_image()` to conditionally resize based on `use_dynamic_size`
- Modified `set_image()` to conditionally resize based on `use_dynamic_size`
- Added `current_h` and `current_w` attributes to track actual dimensions
- Updated `get_img_gray()` to use dynamic dimensions

**ColorizeImageTorch class:**
- Added `use_dynamic_size` parameter to `__init__()`
- Updated `get_img_gray()` to use dynamic dimensions

**ColorizeImageTorchDist class:**
- Added `use_dynamic_size` parameter to `__init__()`
- Removed fixed-size array initialization from `__init__()`
- Modified `net_forward()` to dynamically allocate arrays based on actual output size

**ColorizeImageCaffe class:**
- Added `use_dynamic_size` parameter to `__init__()`
- Updated `get_img_gray()` to use dynamic dimensions

**ColorizeImageCaffeDist class:**
- Added `use_dynamic_size` parameter to `__init__()`
- Removed fixed-size array initialization from `__init__()`
- Modified `net_forward()` to dynamically allocate arrays based on actual output size

**ColorizeImageCaffeGlobDist class:**
- Added `use_dynamic_size` parameter to `__init__()`

### 2. ideepcolor.py

- Added `--use_dynamic_size` argument to argument parser
- Passed `use_dynamic_size` flag to all model initializations (both Caffe and PyTorch)

### 3. ui/gui_draw.py

**GUIDraw class:**
- Added `actual_load_size` attribute to track model input dimensions
- Modified `read_image()` to:
  - Detect if model uses dynamic sizing
  - Calculate actual model input size
  - Store in `actual_load_size` tuple
  - Pass to UIControl
  - Use for array initialization
- Modified `scale_point()` to use `actual_load_size` instead of fixed `load_size`

### 4. ui/ui_control.py

**UserEdit class:**
- Added `actual_load_size` parameter to `__init__()`
- Modified scale calculation to use `actual_load_size`
- Updated `scale_point()` to use `actual_load_size` dimensions

**PointEdit class:**
- Added `actual_load_size` parameter to `__init__()`
- Passed to parent UserEdit class

**UIControl class:**
- Added `actual_load_size` parameter to `__init__()`
- Added `setActualLoadSize()` method
- Modified `addPoint()` to pass `actual_load_size` to PointEdit
- Modified `get_input()` to use `actual_load_size` for array dimensions

## New Files

### 1. test_dynamic_size.py
Test script to demonstrate and compare fixed vs dynamic sizing modes.

### 2. DYNAMIC_SIZE_GUIDE.md
Comprehensive user guide for the dynamic sizing feature.

### 3. CHANGES_DYNAMIC_SIZE.md
This file - technical summary of all changes.

## Technical Details

### Dimension Handling

**Fixed Mode (default):**
```python
model = ColorizeImageTorch(Xd=256, use_dynamic_size=False)
# All images resized to 256x256
```

**Dynamic Mode:**
```python
model = ColorizeImageTorch(Xd=256, use_dynamic_size=True)
# Images resized to (w//4)*4 x (h//4)*4
# Preserves aspect ratio
```

### Coordinate Transformation

The system now tracks two coordinate spaces:
1. **Window coordinates** - Display window (win_size x win_size)
2. **Model coordinates** - Model input (actual_load_size)

Transformations account for:
- Window padding (dw, dh)
- Display size (win_w, win_h)
- Actual model input size (actual_load_size)

### Array Allocation

Arrays are now dynamically sized:
```python
# Old (fixed):
self.im_ab0 = np.zeros((2, self.load_size, self.load_size))

# New (dynamic):
model_w, model_h = self.actual_load_size
self.im_ab0 = np.zeros((2, model_h, model_w))
```

## Backward Compatibility

- Default behavior unchanged (use_dynamic_size=False)
- All existing code works without modification
- New flag is optional

## Testing

Run the test script:
```bash
conda activate rvrt
python test_dynamic_size.py --image test_imgs/mortar_pestle.jpg --backend pytorch
```

Expected output:
- Shows original image dimensions
- Compares fixed vs dynamic mode outputs
- Demonstrates aspect ratio preservation

## Usage Examples

```bash
# Activate conda environment
conda activate rvrt

# Basic usage with dynamic sizing
python ideepcolor.py --use_dynamic_size

# With specific image
python ideepcolor.py --use_dynamic_size --image_file my_image.jpg

# With GPU selection
python ideepcolor.py --use_dynamic_size --gpu 0

# CPU mode
python ideepcolor.py --use_dynamic_size --cpu_mode

# PyTorch backend
python ideepcolor.py --use_dynamic_size --backend pytorch

# Caffe backend
python ideepcolor.py --use_dynamic_size --backend caffe
```

## Benefits

1. **Preserves aspect ratio** - No distortion from square resizing
2. **Better quality** - Uses actual image resolution
3. **Flexible** - Works with any image size (divisible by 4)
4. **Optional** - Backward compatible with existing workflow

## Considerations

1. **Memory usage** - Larger images use more GPU memory
2. **Processing time** - Scales with image size
3. **Model training** - Model was trained on 256x256, results may vary with very different sizes
