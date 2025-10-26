# User Guide: Interactive Colorization

## Quick Start

```bash
conda activate rvrt
python ideepcolor.py --gpu 0 --backend pytorch
```

## Understanding the Interface

### Main Panels

1. **Drawing Pad (Center)** - Your grayscale image
2. **Result (Right)** - Colorized output
3. **ab Color Gamut (Left)** - Color selector
4. **Color Palettes (Left)** - Suggested and preset colors

## How to Colorize

### Basic Workflow

1. **Load Image**
   - File → Load Image
   - Or use `--image_file` parameter

2. **Click on Image**
   - Left-click where you want to add color
   - Watch console for L value (brightness)

3. **Select Color**
   - From gamut widget
   - From suggested colors
   - From preset palettes

4. **See Result**
   - Result updates automatically
   - Toggle grayscale view with checkbox

5. **Save Result**
   - File → Save
   - Saves full resolution output

### Important: Color Calibration

**Why colors change when you click:**

The system adjusts your selected color to match the brightness (L value) at the clicked position. This ensures natural-looking results.

**Example:**
- You select: Bright Red (RGB 255, 0, 0)
- You click on: Dark area (L=20)
- System applies: Dark Red (RGB 76, 0, 0)

This is **correct behavior** - it preserves the image's lighting structure.

## Tips for Best Results

### 1. Click First, Then Choose Color

✅ **Good workflow:**
```
1. Click on area
2. See L value in console
3. Gamut updates for that brightness
4. Select appropriate color
5. Apply
```

❌ **Confusing workflow:**
```
1. Select bright color
2. Click on dark area
3. Color becomes dark (unexpected!)
```

### 2. Understand Brightness Levels

- **Dark areas (L < 30)**: Use darker colors
- **Mid-tones (L 30-70)**: Full color range available
- **Bright areas (L > 70)**: Use lighter colors

### 3. Use Suggested Colors

After clicking, the system suggests colors that:
- Match the L value at that position
- Are based on learned color distributions
- Work well for that area

### 4. Use Multiple Points

- Add points to different areas
- Use similar colors for similar brightness
- Build up the colorization gradually

## Interface Features

### Drawing Pad

- **Left-click**: Add/move color point
- **Right-click**: Remove color point
- **Mouse wheel**: Adjust brush size
- **Toggle grayscale**: Show/hide colorization

### ab Color Gamut

- Shows valid colors for current L value
- Crosshair cursor shows selected color
- Updates when you click on image
- Click to select new color

### Color Palettes

1. **Suggested Colors**: AI-generated suggestions for clicked position
2. **Used Colors**: Recently used colors
3. **Preset Palette**: Common colors
4. **Reference Colors**: Colors from reference image

### Keyboard Shortcuts

- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+S**: Save
- **Ctrl+O**: Open image

## Command Line Options

### Basic Usage

```bash
# Default (fixed 256x256)
python ideepcolor.py --gpu 0 --backend pytorch

# Dynamic sizing (preserves aspect ratio)
python ideepcolor.py --use_dynamic_size --gpu 0 --backend pytorch

# CPU mode
python ideepcolor.py --cpu_mode --backend pytorch

# Custom window size
python ideepcolor.py --win_size 512 --gpu 0
```

### All Options

```bash
--image_file PATH          # Input image path
--gpu ID                   # GPU ID (0, 1, etc.) or -1 for CPU
--cpu_mode                 # Use CPU instead of GPU
--backend {pytorch,caffe}  # Backend to use
--win_size SIZE            # Window size (default: 512)
--load_size SIZE           # Model input size (default: 256)
--use_dynamic_size         # Use actual image dimensions
```

## Output Files

When you save, the system creates a folder with:

- `ours_fullres.png` - **Main output** (original resolution)
- `ours.png` - Model resolution output
- `input_fullres.png` - Original input (full res)
- `input.png` - Model resolution input
- `input_mask.png` - Mask showing where you added colors
- `input_ab.png` - Your color hints
- `im_l.npy`, `im_ab.npy`, `im_mask.npy` - Raw data

**Use `ours_fullres.png` for final results!**

## Troubleshooting

### Colors Look Wrong

**Q:** My bright color became dark!
**A:** You clicked on a dark area. The system preserves brightness. Click on a brighter area or use a darker color.

**Q:** Gamut cursor jumps around
**A:** It shows the calibrated color (after brightness adjustment), not your original selection.

### Performance Issues

**Q:** Application is slow
**A:** Try:
- Use fixed size mode (default)
- Reduce window size: `--win_size 256`
- Use CPU mode if GPU has issues

**Q:** Out of memory error
**A:** Use fixed size mode or smaller images

### Image Quality

**Q:** Output is blurry
**A:** The system upsamples to original resolution. For best results:
- Use high-quality input images
- Add more color points
- Use dynamic sizing: `--use_dynamic_size`

## Advanced Features

### Dynamic Image Sizing

Preserves aspect ratio and uses actual dimensions:

```bash
python ideepcolor.py --use_dynamic_size --gpu 0
```

**Benefits:**
- Preserves aspect ratio
- Better quality for non-square images
- Uses actual resolution

**Trade-offs:**
- Slower for large images
- More GPU memory required

See `DYNAMIC_SIZE_GUIDE.md` for details.

### Batch Processing

Process multiple images:

```python
from data import colorize_image as CI

model = CI.ColorizeImageTorch(Xd=256)
model.prep_net(gpu_id=0, path='./models/pytorch/caffemodel.pth')

for img_path in image_list:
    model.load_image(img_path)
    # Add your color hints here
    result = model.get_img_fullres()
    # Save result
```

## Understanding the Console Output

When you use the application, you'll see:

```
Gamut updated for L=50.0          # Gamut initialized
Color set: RGB=(255, 0, 0)        # You selected a color
mouse press QPoint(200, 150)      # You clicked
Position (100, 75): L value = 25.3  # Brightness at that position
Color calibrated: user_color=(255, 0, 0) -> snap_color=(95, 0, 0)  # Adjustment
Gamut cursor updated: ...         # Gamut shows new color
```

This helps you understand what's happening behind the scenes.

## Best Practices

### For Natural Results

1. Start with key areas (faces, objects)
2. Use suggested colors when available
3. Add points gradually
4. Check result frequently
5. Adjust colors as needed

### For Consistent Colors

1. Use "Used Colors" palette
2. Apply similar colors to similar areas
3. Consider the lighting in the scene
4. Respect brightness levels

### For High Quality

1. Use high-resolution input images
2. Add sufficient color points
3. Use dynamic sizing for non-square images
4. Save full resolution output

## Getting Help

- **Color behavior**: See `COLOR_BEHAVIOR_EXPLAINED.md`
- **Dynamic sizing**: See `DYNAMIC_SIZE_GUIDE.md`
- **Examples**: See `EXAMPLE_USAGE.md`
- **Technical details**: See `CHANGES_DYNAMIC_SIZE.md`
- **Recent fixes**: See `FIXES_SUMMARY.md`

## Summary

Key points to remember:

1. **Colors are calibrated** to match image brightness
2. **Click first**, then select color for best results
3. **Use suggested colors** when available
4. **Full resolution output** is automatically saved
5. **Dynamic sizing** available for better quality

Happy colorizing!
