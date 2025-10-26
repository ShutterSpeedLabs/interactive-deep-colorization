# Auto-Colorize Quick Start

## What is Auto-Colorize?

Automatically transfer colors from a reference image to your grayscale image using computer vision feature matching.

## Quick Usage

### Method 1: GUI (Easiest)

```bash
conda activate rvrt
python ideepcolor.py --gpu 0 --backend pytorch
```

**Steps:**
1. Load your grayscale image (File → Load Image)
2. In "Reference Image" panel, click "Load Reference"
3. Select a similar color image
4. Click "Auto-Colorize" button
5. Done! Colors are automatically applied

### Method 2: Command Line

```bash
conda activate rvrt

# Test with default image
python test_auto_colorize.py

# Test with your images
python test_auto_colorize.py --gray my_gray.jpg --ref my_reference.jpg

# Extract color points
python auto_colorize_from_reference.py \
    --gray_image my_gray.jpg \
    --ref_image my_reference.jpg \
    --num_points 50 \
    --visualize
```

## When to Use

✅ **Use auto-colorize when:**
- You have a similar color reference image
- You want a quick starting point
- The images have similar content/structure
- You want to save time

❌ **Don't use when:**
- Reference image is very different
- Images have different viewpoints
- You need precise control
- Images lack distinctive features

## Tips

1. **Best results**: Use reference images of the same scene/object
2. **Start point**: Use auto-colorize, then refine manually
3. **Adjust**: If results are poor, try different reference image
4. **Combine**: Mix auto-colorize with manual color points

## Example Workflow

```bash
# 1. Test the feature
python test_auto_colorize.py --gray old_photo.jpg --ref modern_photo.jpg

# 2. Check visualization
# Open: test_auto_colorize_visualization.png

# 3. If good, use in GUI
python ideepcolor.py --gpu 0 --backend pytorch
# Load images and click "Auto-Colorize"

# 4. Refine manually if needed
# Add/remove/adjust color points

# 5. Save result
# File → Save
```

## Parameters

### GUI (Fixed)
- Method: ORB
- Points: 30
- Threshold: 0.75

### Command Line (Adjustable)
```bash
--method orb              # Feature detector (orb/sift/akaze)
--num_points 50           # Number of color points
--match_threshold 0.7     # Matching strictness (0-1)
```

## Troubleshooting

**No matches found?**
- Use more similar reference image
- Try `--match_threshold 0.8`

**Wrong colors?**
- Use `--match_threshold 0.6` (stricter)
- Reduce `--num_points 20`

**Too slow?**
- Use `--method orb` (fastest)
- Reduce `--num_points 20`

## More Info

- Full guide: `AUTO_COLORIZE_GUIDE.md`
- Test script: `test_auto_colorize.py`
- Core module: `auto_colorize_from_reference.py`

## Status

✅ Implemented and tested  
✅ GUI integration complete  
✅ Command-line tools available  
✅ Documentation complete  
