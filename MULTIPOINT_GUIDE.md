# Multi-Point Colorization Guide

## Overview
The iDeepColor application now supports adding multiple color points to your image, allowing you to colorize different regions with different colors. This guide explains how to use the multi-point feature effectively.

## How It Works

### Basic Concept
Instead of colorizing the entire image with one color, you can:
1. Add multiple color points at different locations
2. Each point influences the surrounding area
3. The AI blends colors naturally between points
4. You can move, modify, or remove points at any time

### Mouse Controls

#### Left-Click: Add or Move Points
- **Click on empty area**: Adds a new color point
- **Click on existing point**: Selects and allows you to move it
- **Drag**: Moves the selected point to a new location

#### Right-Click: Remove Points
- **Right-click on a point**: Removes that color point
- The colorization updates automatically

#### Mouse Wheel: Adjust Brush Size
- **Scroll up**: Increase brush size (larger influence area)
- **Scroll down**: Decrease brush size (smaller influence area)
- Brush size range: 0 to 4x scale

## Workflow

### Step-by-Step Process

#### 1. Load an Image
```
File → Load (or press L)
```

#### 2. Select a Color
Choose from:
- **Preset Colors**: Select category and click a color
- **AI Suggestions**: Click on image to see suggestions
- **Color Gamut**: Click on the ab color space

#### 3. Add First Point
- Left-click on the image where you want to apply the color
- A colored square appears at that location
- The image updates with the colorization

#### 4. Add More Points
- Select a different color (from presets or suggestions)
- Left-click on another area of the image
- Repeat for as many points as needed

#### 5. Adjust Points
- **Move**: Left-click and drag an existing point
- **Resize**: Use mouse wheel to change brush size
- **Remove**: Right-click on a point to delete it

#### 6. Save Result
```
File → Save (or press S)
```

## Example Workflows

### Portrait Colorization

```
1. Add point on face with "Skin - Medium" color
2. Add point on hair with "Hair - Brown" color
3. Add point on lips with "Lips - Pink" color
4. Add point on eyes with "Eyes - Blue" color
5. Add point on clothing with appropriate fabric color
6. Adjust brush sizes for natural blending
7. Save result
```

### Landscape Colorization

```
1. Add point in sky with "Sky - Blue" color
2. Add multiple points in grass with "Grass - Green" color
3. Add points on trees with "Leaves - Green" color
4. Add points on ground with "Ground - Dirt" color
5. Add points on water with "Water - Blue" color
6. Fine-tune with additional points
7. Save result
```

### Historical Photo Restoration

```
1. Start with skin tones on faces
2. Add hair colors for each person
3. Add clothing colors (use Fabrics category)
4. Add background elements (buildings, nature)
5. Add detail points for small objects
6. Adjust and refine
7. Save result
```

## Tips & Best Practices

### For Best Results

1. **Start with large areas**: Add points for major regions first (sky, ground, main subjects)
2. **Use appropriate brush sizes**: Larger for backgrounds, smaller for details
3. **Add multiple points per region**: For large areas, add several points with the same color
4. **Work from background to foreground**: Color distant objects first, then closer ones
5. **Use color variations**: Don't use the exact same color everywhere - add subtle variations

### Point Placement Strategy

#### Good Point Placement:
```
✓ Multiple points in large areas
✓ Points spread evenly across regions
✓ Smaller brush sizes for edges
✓ Larger brush sizes for uniform areas
✓ Points at color boundaries
```

#### Poor Point Placement:
```
✗ Single point for large area
✗ All points clustered together
✗ Same brush size everywhere
✗ Points too close to edges
✗ Conflicting colors too close
```

### Brush Size Guidelines

| Area Type | Recommended Brush Size |
|-----------|----------------------|
| Large backgrounds (sky, water) | 3-4x scale |
| Medium areas (grass, walls) | 2-3x scale |
| Small objects (faces, flowers) | 1-2x scale |
| Fine details (eyes, lips) | 0.5-1x scale |

## Advanced Techniques

### Gradient Effects
1. Add points with similar colors at different locations
2. Use slightly different shades
3. The AI will create smooth gradients between points

### Color Blending
1. Add overlapping points with different colors
2. Adjust brush sizes to control blend area
3. Experiment with color combinations

### Selective Colorization
1. Add points only to specific areas
2. Leave other areas grayscale
3. Creates artistic partial colorization effect

### Iterative Refinement
1. Add initial points for rough colorization
2. Review the result
3. Add more points to refine specific areas
4. Remove points that don't work
5. Adjust brush sizes for better blending

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| L | Load new image |
| S | Save result |
| R | Reset (remove all points) |
| G | Toggle grayscale view |
| Q | Save and quit |

## Visual Indicators

### Point Display
- **Colored squares**: Show where points are placed
- **Border color**: Black or white (for contrast)
- **Size**: Indicates brush size/influence area

### Current State
- **Color indicator**: Shows currently selected color
- **Instruction bar**: Shows available mouse actions
- **Point count**: Visible in console output

## Troubleshooting

### Problem: Points not appearing
**Solution**: Make sure you're clicking within the image area (not in the border)

### Problem: Can't move a point
**Solution**: Click directly on the colored square, then drag

### Problem: Wrong color applied
**Solution**: 
1. Right-click to remove the point
2. Select the correct color
3. Add a new point

### Problem: Colors look unnatural
**Solution**:
1. Add more points for smoother transitions
2. Adjust brush sizes
3. Use colors from the preset palette
4. Combine with AI suggestions

### Problem: Can't remove a point
**Solution**: Right-click directly on the colored square (not near it)

### Problem: Too many points
**Solution**: 
- Press R to reset and start over
- Or right-click to remove points one by one

## Comparison: Single vs Multi-Point

### Single Point Mode (Old Behavior)
```
- One color point at a time
- Entire image influenced by one color
- Limited control over regions
- Fast but less precise
```

### Multi-Point Mode (New Behavior)
```
✓ Multiple color points simultaneously
✓ Different colors in different regions
✓ Fine control over colorization
✓ More realistic results
✓ Matches original repository behavior
```

## Technical Details

### How Points Work
1. Each point stores: position, color, brush size
2. Points are rendered as colored squares on the image
3. The neural network uses all points as hints
4. Colors blend naturally based on image content
5. Points can be added, moved, or removed dynamically

### Point Storage
- Points are stored in `uiControl.userEdits` list
- Each point is a `PointEdit` object
- Points persist until removed or reset
- Points are saved with the result

### Performance
- Adding points: Instant
- Moving points: Real-time update
- Removing points: Instant
- Colorization: ~1-2 seconds per update (GPU)

## Examples from Original Repository

The original interactive-deep-colorization repository demonstrates:
- Multiple points for complex scenes
- Different colors for different objects
- Natural color blending
- Interactive refinement

Our implementation now matches this behavior!

## Future Enhancements

Potential improvements:
- [ ] Point labels/numbers
- [ ] Point color history
- [ ] Undo/redo for individual points
- [ ] Point grouping
- [ ] Copy/paste points
- [ ] Point presets for common objects
- [ ] Batch point application

## Summary

The multi-point feature allows you to:
- ✅ Add unlimited color points to your image
- ✅ Use different colors in different regions
- ✅ Move and adjust points interactively
- ✅ Remove points with right-click
- ✅ Control influence area with brush size
- ✅ Create realistic, natural-looking colorizations

**Start adding multiple points and see the difference!** 🎨
