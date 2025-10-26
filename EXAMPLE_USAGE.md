# Example Usage: Dynamic Image Size

## Quick Start

First, activate the conda environment:
```bash
conda activate rvrt
```

### Before (Fixed 256x256)
```bash
python ideepcolor.py --image_file test_imgs/mortar_pestle.jpg
```
- Image is resized to 256x256 regardless of original size
- Aspect ratio may be distorted

### After (Dynamic Size)
```bash
python ideepcolor.py --use_dynamic_size --image_file test_imgs/mortar_pestle.jpg
```
- Image dimensions are preserved (adjusted to multiples of 4)
- Aspect ratio maintained

## Detailed Examples

### Example 1: Portrait Image (600x800)

**Without dynamic sizing:**
```bash
python ideepcolor.py --image_file portrait.jpg --backend pytorch
```
Result: Image squeezed to 256x256 (aspect ratio lost)

**With dynamic sizing:**
```bash
python ideepcolor.py --use_dynamic_size --image_file portrait.jpg --backend pytorch
```
Result: Image processed at 600x800 (aspect ratio preserved)

### Example 2: Landscape Image (1024x768)

**Without dynamic sizing:**
```bash
python ideepcolor.py --image_file landscape.jpg --backend pytorch
```
Result: Image squeezed to 256x256

**With dynamic sizing:**
```bash
python ideepcolor.py --use_dynamic_size --image_file landscape.jpg --backend pytorch
```
Result: Image processed at 1024x768

### Example 3: Square Image (512x512)

**Without dynamic sizing:**
```bash
python ideepcolor.py --image_file square.jpg --backend pytorch
```
Result: Image resized to 256x256

**With dynamic sizing:**
```bash
python ideepcolor.py --use_dynamic_size --image_file square.jpg --backend pytorch
```
Result: Image processed at 512x512 (higher resolution)

## Command Line Options

### Basic Options
```bash
# Enable dynamic sizing
--use_dynamic_size

# Specify image file
--image_file path/to/image.jpg

# Choose backend
--backend pytorch    # or caffe

# GPU selection
--gpu 0              # Use GPU 0
--gpu -1             # Use CPU
--cpu_mode           # Use CPU (alternative)
```

### Complete Example
```bash
python ideepcolor.py \
    --use_dynamic_size \
    --image_file test_imgs/mortar_pestle.jpg \
    --backend pytorch \
    --gpu 0 \
    --win_size 512
```

## Testing the Feature

### Test Script
```bash
# Activate environment
conda activate rvrt

# Run comparison test
python test_dynamic_size.py --image test_imgs/mortar_pestle.jpg --backend pytorch

# With GPU
python test_dynamic_size.py --image my_image.jpg --backend pytorch --gpu 0

# CPU mode
python test_dynamic_size.py --image my_image.jpg --backend pytorch --gpu -1
```

### Expected Output
```
============================================================
Testing Dynamic Size Colorization
============================================================

Original image size: 800x600

------------------------------------------------------------
Test 1: Fixed size mode (256x256)
------------------------------------------------------------
Model input size: 256x256
Model img_l shape: (1, 256, 256)
Output shape: (256, 256, 3)

------------------------------------------------------------
Test 2: Dynamic size mode (actual dimensions)
------------------------------------------------------------
Model input size: 800x600
Model img_l shape: (1, 600, 800)
Current dimensions: 800x600
Output shape: (600, 800, 3)

============================================================
Summary:
============================================================
Original image: 800x600
Fixed mode output: 256x256
Dynamic mode output: 800x600

Dynamic mode preserves aspect ratio and uses actual dimensions!
============================================================
```

## When to Use Dynamic Sizing

### ✅ Use Dynamic Sizing When:
- Working with non-square images
- Aspect ratio is important
- You want maximum detail preservation
- You have sufficient GPU memory
- Processing single high-quality images

### ❌ Use Fixed Sizing When:
- Batch processing many images
- Limited GPU memory
- Need consistent processing time
- Working with very large images (>2048px)
- Speed is more important than aspect ratio

## Performance Comparison

| Image Size | Fixed Mode | Dynamic Mode | Memory Usage |
|------------|------------|--------------|--------------|
| 256x256    | ~0.1s      | ~0.1s        | ~500MB       |
| 512x512    | ~0.1s      | ~0.3s        | ~1GB         |
| 1024x768   | ~0.1s      | ~0.8s        | ~1.5GB       |
| 1920x1080  | ~0.1s      | ~2.0s        | ~3GB         |

*Times are approximate and depend on GPU*

## Troubleshooting

### Out of Memory Error
```
RuntimeError: CUDA out of memory
```
**Solution:** Use fixed mode or reduce image size:
```bash
conda activate rvrt

# Resize image first
convert input.jpg -resize 1024x1024 resized.jpg
python ideepcolor.py --use_dynamic_size --image_file resized.jpg
```

### Image Dimensions Not Divisible by 4
The system automatically adjusts dimensions to be divisible by 4:
- 1023x767 → 1020x764
- 800x601 → 800x600

### Slow Processing
For very large images, consider:
1. Using fixed mode
2. Resizing image before processing
3. Using a more powerful GPU

## Integration with Existing Workflow

### Python API
```python
from data import colorize_image as CI

# Create model with dynamic sizing
model = CI.ColorizeImageTorch(Xd=256, use_dynamic_size=True)
model.prep_net(gpu_id=0, path='./models/pytorch/caffemodel.pth')

# Load and process image
model.load_image('my_image.jpg')

# Get result
result = model.get_img_fullres()
```

### Batch Processing
```python
import glob
from data import colorize_image as CI

# Initialize model once
model = CI.ColorizeImageTorch(Xd=256, use_dynamic_size=True)
model.prep_net(gpu_id=0, path='./models/pytorch/caffemodel.pth')

# Process multiple images
for img_path in glob.glob('images/*.jpg'):
    model.load_image(img_path)
    result = model.get_img_fullres()
    # Save result...
```

## Additional Resources

- See `DYNAMIC_SIZE_GUIDE.md` for detailed documentation
- See `CHANGES_DYNAMIC_SIZE.md` for technical implementation details
- Run `python test_dynamic_size.py --help` for test script options
