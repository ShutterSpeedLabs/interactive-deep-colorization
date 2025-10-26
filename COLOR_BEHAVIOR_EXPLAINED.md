# Color Selection Behavior Explained

## Why Colors Change When Clicking

When you select a color and then click on the image, you may notice the color changes. This is **intentional behavior** for proper colorization.

## How It Works

### The LAB Color Space

The colorization system uses the LAB color space, which separates:
- **L (Lightness)**: 0 (black) to 100 (white)
- **a**: Green to Red
- **b**: Blue to Yellow

### Color Calibration Process

When you click on the image:

1. **You select a color** (e.g., bright red: RGB 255, 0, 0)
2. **System reads the L value** at the clicked position from the grayscale image
3. **Color is calibrated** to match that L value while preserving the a,b (hue/saturation)

### Example

**Scenario:** You select bright red and click on a dark area

- **Selected color:** Bright red (L=53, a=80, b=67)
- **Image L value at click:** 20 (dark area)
- **Result:** Dark red (L=20, a=80, b=67)

The system keeps your chosen hue (red) but adjusts the brightness to match the grayscale image.

## Why This Matters

This ensures:
- ✅ Colors match the original image's lighting
- ✅ Dark areas stay dark, bright areas stay bright
- ✅ Natural-looking colorization
- ✅ Consistent with the grayscale structure

## Visual Workflow

```
1. Select Color from Gamut/Palette
   └─> User Color: RGB(255, 0, 0) - Bright Red
   
2. Click on Image Position
   └─> Read L value at position: L=20 (dark)
   
3. Calibrate Color
   └─> Keep a,b (redness) but adjust L
   └─> Result: RGB(76, 0, 0) - Dark Red
   
4. Apply to Image
   └─> Color matches the grayscale brightness
```

## Understanding the Gamut Widget

The **ab Color Gamut** widget shows:
- Valid colors for the current L value
- Cursor position shows the selected color's a,b values
- When you click different positions, the gamut updates to show valid colors for that brightness level

### Gamut Updates

1. **Before clicking:** Shows default L=50 (mid-gray)
2. **After clicking dark area:** Shows L=20 (limited color range)
3. **After clicking bright area:** Shows L=80 (wider color range)

## Tips for Best Results

### 1. Click First, Then Adjust Color
- Click on the area you want to colorize
- The gamut will update to show valid colors for that brightness
- Select a color from the updated gamut

### 2. Understand Brightness Constraints
- **Dark areas** (L < 30): Limited color intensity
- **Mid-tones** (L 30-70): Full color range
- **Bright areas** (L > 70): Lighter colors only

### 3. Use Color Suggestions
- After clicking, the system suggests appropriate colors
- These suggestions already match the L value
- They're based on the color distribution model

## Common Questions

### Q: Why does my bright color become dark?
**A:** You clicked on a dark area. The system preserves the darkness while applying your chosen hue.

### Q: Can I force a bright color on a dark area?
**A:** No, this would create unrealistic results. The L value from the grayscale image is preserved.

### Q: Why does the gamut cursor jump when I click?
**A:** The cursor shows the calibrated color (after L adjustment), not your original selection.

### Q: How do I get the exact color I want?
**A:** Click on an area with similar brightness to your desired color. The gamut will show achievable colors for that brightness level.

## Technical Details

### Color Calibration Algorithm

The `snap_ab` function:
1. Takes your selected RGB color
2. Converts to LAB
3. Replaces L with the image's L value at clicked position
4. Iteratively adjusts a,b to ensure the result is in RGB gamut
5. Returns the calibrated RGB color

```python
# Simplified process
input_color = RGB(255, 0, 0)  # Bright red
input_lab = rgb_to_lab(input_color)  # L=53, a=80, b=67
image_L = 20  # Dark area

calibrated_lab = (20, 80, 67)  # Keep a,b, use image L
calibrated_rgb = lab_to_rgb(calibrated_lab)  # RGB(76, 0, 0) - Dark red
```

### Why This Approach?

1. **Preserves Structure:** Maintains the original image's lighting and shadows
2. **Realistic Results:** Colors look natural and believable
3. **Gamut Compliance:** Ensures all colors are displayable in RGB
4. **Consistent:** Same approach used in research papers on colorization

## Workflow Recommendations

### For Best User Experience:

1. **Load your grayscale image**
2. **Click on the area** you want to colorize
3. **Observe the L value** (printed in console)
4. **Check the updated gamut** - shows valid colors for that brightness
5. **Select from suggested colors** or choose from the gamut
6. **Apply and see the result**

### For Multiple Points:

1. Click different areas to see how L values vary
2. Use similar colors for similar brightness levels
3. Use the "Used Colors" palette to maintain consistency
4. Adjust colors by clicking on existing points

## Debug Information

When you click, the console shows:
```
Position (x, y): L value = 45.2
Color calibrated: user_color=(255, 0, 0) -> snap_color=(180, 0, 0)
Gamut cursor updated: color=[180 0 0], lab=[45.2 80.1 67.2], pos=(165.3, 98.7)
```

This helps you understand:
- The L value at the clicked position
- How your color was adjusted
- Where the gamut cursor moved

## Summary

The color change behavior is **by design** to ensure:
- Natural-looking colorization
- Preservation of image structure
- Realistic color application

Understanding this workflow will help you achieve better colorization results!
