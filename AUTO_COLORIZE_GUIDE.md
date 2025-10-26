# Auto-Colorize from Reference Image Guide

## Overview

This feature automatically detects unique feature points in a reference image and transfers their colors to corresponding points in your grayscale image. It uses computer vision techniques (ORB/SIFT/AKAZE) to find matching features between images.

## How It Works

### 1. Feature Detection
- Detects keypoints in both grayscale and reference images
- Uses ORB (Oriented FAST and Rotated BRIEF) by default
- Finds distinctive features like corners, edges, and textures

### 2. Feature Matching
- Matches features between the two images
- Uses Lowe's ratio test to filter good matches
- Ensures robust correspondence

### 3. Color Transfer
- Extracts colors from matched points in reference image
- Clusters points to get representative samples
- Applies colors to corresponding points in grayscale image

### 4. Automatic Application
- Automatically adds color points to the image
- Triggers colorization model
- Produces colorized result

## Usage

### GUI Method (Recommended)

1. **Load your grayscale image**
   ```bash
   conda activate rvrt
   python ideepcolor.py --gpu 0 --backend pytorch
   ```

2. **Load reference image**
   - In the "Reference Image" panel (right side)
   - Click "Load Reference" button
   - Select a color image similar to your grayscale image

3. **Auto-colorize**
   - Click "Auto-Colorize" button
   - Wait for feature detection and matching
   - Color points are automatically applied!

### Command Line Method

```bash
conda activate rvrt

# Extract color points from reference
python auto_colorize_from_reference.py \
    --gray_image input_gray.jpg \
    --ref_image reference_color.jpg \
    --num_points 50 \
    --output color_points.txt \
    --visualize

# Then use the color points in the GUI
# (Load the grayscale image and manually apply the points)
```

## Parameters

### GUI Parameters (Hardcoded)
- **Method**: ORB (fast and robust)
- **Number of points**: 30 (good balance)
- **Match threshold**: 0.75 (moderate strictness)

### Command Line Parameters

```bash
--gray_image PATH          # Grayscale image to colorize
--ref_image PATH           # Reference color image
--method {orb,sift,akaze}  # Feature detection method
--num_points N             # Number of color points (default: 50)
--match_threshold T        # Matching threshold 0-1 (default: 0.7)
--output PATH              # Output file for color points
--visualize                # Save visualization image
```

## Feature Detection Methods

### ORB (Default)
- **Speed**: Fast ⚡
- **Accuracy**: Good
- **Memory**: Low
- **Best for**: General use, real-time applications

### SIFT
- **Speed**: Slow
- **Accuracy**: Excellent
- **Memory**: High
- **Best for**: High-quality matching, scale variations
- **Note**: May not be available in all OpenCV builds

### AKAZE
- **Speed**: Medium
- **Accuracy**: Very good
- **Memory**: Medium
- **Best for**: Balance between speed and accuracy

## Tips for Best Results

### 1. Choose Good Reference Images

✅ **Good reference images:**
- Similar scene/subject to grayscale image
- Similar viewpoint and angle
- Clear, high-quality images
- Good lighting

❌ **Poor reference images:**
- Completely different scenes
- Very different angles
- Low quality or blurry
- Extreme lighting differences

### 2. Image Similarity

The more similar the images, the better the results:
- **Same scene, different time**: Excellent
- **Same object, different angle**: Good
- **Similar objects**: Moderate
- **Different scenes**: Poor

### 3. Adjust Parameters

If auto-colorization doesn't work well:

**Too few matches:**
- Increase `match_threshold` (e.g., 0.8)
- Try different feature detection method
- Use more similar reference image

**Too many incorrect matches:**
- Decrease `match_threshold` (e.g., 0.6)
- Reduce `num_points`
- Use higher quality images

### 4. Manual Refinement

After auto-colorization:
- Review the result
- Add/remove points manually
- Adjust colors as needed
- Use suggested colors for refinement

## Examples

### Example 1: Same Scene, Different Time

```bash
# Grayscale: old_photo.jpg (black and white)
# Reference: modern_photo.jpg (same location, color)

python auto_colorize_from_reference.py \
    --gray_image old_photo.jpg \
    --ref_image modern_photo.jpg \
    --num_points 50 \
    --visualize
```

**Expected result**: Excellent matching, natural colors

### Example 2: Similar Objects

```bash
# Grayscale: my_car.jpg (black and white)
# Reference: similar_car.jpg (same model, color)

python auto_colorize_from_reference.py \
    --gray_image my_car.jpg \
    --ref_image similar_car.jpg \
    --num_points 30 \
    --match_threshold 0.75
```

**Expected result**: Good matching for similar features

### Example 3: Portrait Colorization

```bash
# Grayscale: old_portrait.jpg
# Reference: modern_portrait.jpg (similar pose)

python auto_colorize_from_reference.py \
    --gray_image old_portrait.jpg \
    --ref_image modern_portrait.jpg \
    --method akaze \
    --num_points 40
```

**Expected result**: Good for faces, clothing, background

## Workflow

### Complete Workflow

1. **Prepare images**
   - Grayscale image to colorize
   - Similar color reference image

2. **Load in GUI**
   ```bash
   conda activate rvrt
   python ideepcolor.py --use_dynamic_size --gpu 0
   ```

3. **Load grayscale image**
   - File → Load Image
   - Or use `--image_file` parameter

4. **Load reference image**
   - Click "Load Reference" in Reference Image panel
   - Select your color reference image

5. **Auto-colorize**
   - Click "Auto-Colorize" button
   - Wait for processing (5-10 seconds)
   - Review results

6. **Refine (optional)**
   - Add more color points manually
   - Adjust existing colors
   - Remove incorrect points

7. **Save result**
   - File → Save
   - Use `ours_fullres.png` for final output

## Understanding the Output

### Console Output

```
Detecting features using ORB...
Found 487 keypoints in grayscale image
Found 523 keypoints in reference image
Matching features...
Found 156 good matches
Clustering to 30 representative points...
Extracted 30 color points
Applying 30 color points automatically...
Applied 28 color points successfully!
```

### What This Means

- **Keypoints found**: More is generally better (>100)
- **Good matches**: Should be >20 for decent results
- **Extracted points**: Final number of color hints
- **Applied points**: Successfully added to image

### Visualization (Command Line)

When using `--visualize`, you get:
- Top: Grayscale image with color points marked
- Bottom: Feature matches between images

This helps you understand:
- Which features were matched
- Where colors are being applied
- Quality of the matching

## Troubleshooting

### No Matches Found

**Problem**: "Found 0 good matches"

**Solutions:**
1. Use more similar reference image
2. Increase match_threshold to 0.8 or 0.9
3. Try different feature detection method
4. Ensure images are not too different

### Too Few Matches

**Problem**: "Found 5 good matches" (too few)

**Solutions:**
1. Use higher quality images
2. Increase match_threshold
3. Ensure images have similar content
4. Try AKAZE or SIFT method

### Incorrect Colors

**Problem**: Colors applied to wrong locations

**Solutions:**
1. Decrease match_threshold to 0.6
2. Reduce num_points
3. Use more similar reference image
4. Manually refine after auto-colorization

### Slow Performance

**Problem**: Takes too long to process

**Solutions:**
1. Use ORB method (fastest)
2. Reduce num_points
3. Resize images to smaller size
4. Use command-line tool for batch processing

## Advanced Usage

### Batch Processing

```python
from auto_colorize_from_reference import AutoColorizeFromReference
import cv2
import glob

# Initialize once
auto_colorizer = AutoColorizeFromReference(
    method='orb',
    num_points=30,
    match_threshold=0.75
)

# Process multiple images
for gray_path in glob.glob('grayscale/*.jpg'):
    gray_img = cv2.imread(gray_path)
    ref_img = cv2.imread('reference.jpg')
    
    color_points, _ = auto_colorizer.extract_color_points(
        gray_img, ref_img
    )
    
    # Save or apply color points
    print(f"{gray_path}: {len(color_points)} points")
```

### Custom Parameters

```python
# High quality, slow
auto_colorizer = AutoColorizeFromReference(
    method='sift',
    num_points=100,
    match_threshold=0.6
)

# Fast, fewer points
auto_colorizer = AutoColorizeFromReference(
    method='orb',
    num_points=20,
    match_threshold=0.8
)
```

## Limitations

1. **Image Similarity**: Works best with similar images
2. **Feature-rich Images**: Needs distinctive features (corners, edges, textures)
3. **Uniform Areas**: May not work well on plain/uniform regions
4. **Scale Differences**: Large scale differences can reduce matches
5. **Rotation**: Large rotations may affect matching (ORB handles some rotation)

## Comparison with Manual Colorization

| Aspect | Auto-Colorize | Manual |
|--------|---------------|--------|
| **Speed** | Fast (seconds) | Slow (minutes) |
| **Accuracy** | Depends on reference | High (user control) |
| **Effort** | Low | High |
| **Best for** | Similar images | Any image |
| **Refinement** | Often needed | Not needed |

**Recommendation**: Use auto-colorize as a starting point, then refine manually!

## Future Enhancements

Possible improvements:
- [ ] Adjustable parameters in GUI
- [ ] Multiple reference images
- [ ] Region-based matching
- [ ] Deep learning-based matching
- [ ] Real-time preview

## Summary

Auto-colorization from reference images:
- ✅ Fast and automatic
- ✅ Works well with similar images
- ✅ Good starting point for colorization
- ✅ Can be refined manually
- ✅ Uses robust computer vision techniques

**Best practice**: Auto-colorize → Review → Refine → Save
