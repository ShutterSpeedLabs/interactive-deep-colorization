# iDeepColor - Complete Usage Guide

## Quick Start

### Launch Application
```bash
conda activate rvrt
python ideepcolor.py --gpu 0 --backend pytorch
```

## Interface Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Color Gamut  │  │ Drawing Pad  │  │   Result     │            │
│  │              │  │              │  │              │            │
│  │  Suggested   │  │   [Image]    │  │  [Colored]   │            │
│  │   Colors     │  │              │  │              │            │
│  │              │  │  • • • •     │  │              │            │
│  │  Recently    │  │              │  │              │            │
│  │   Used       │  │              │  │              │            │
│  │              │  │              │  │              │            │
│  │  Preset      │  │ [Gray][Load] │  │ [Restart]    │            │
│  │  Colors ▼    │  │ [Save]       │  │ [Quit]       │            │
│  │  ┌─┬─┬─┬─┐   │  │              │  │              │            │
│  │  │█│█│█│█│   │  │ Instructions │  │              │            │
│  │  └─┴─┴─┴─┘   │  └──────────────┘  └──────────────┘            │
│  └──────────────┘                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

### 1. Multi-Point Colorization ⭐ NEW
Add multiple color points to different parts of your image:
- **Left-click**: Add or move color points
- **Right-click**: Remove color points
- **Mouse wheel**: Adjust brush size
- **Unlimited points**: Add as many as you need

### 2. Three Color Selection Methods

#### A. Preset Colors (Left Panel)
- 150+ pre-defined realistic colors
- 7 categories: Human, Nature, Earth & Stone, Sky & Water, Materials, Fabrics, Objects
- Dropdown category selector
- Scrollable color grid
- Color name display

#### B. AI-Suggested Colors (Left Panel)
- Automatically generated based on image context
- Updates when you click on the image
- 9-10 color suggestions per click
- Based on distribution model

#### C. Color Gamut (Left Panel)
- ab color space selector
- Manual color picking
- Real-time preview

### 3. Recently Used Colors
- Automatic color history
- Quick access to previous colors
- Maintains consistency across image

## Step-by-Step Workflow

### Basic Colorization

1. **Launch Application**
   ```bash
   python ideepcolor.py --gpu 0 --backend pytorch
   ```

2. **Load Image** (Optional)
   - Click "Load" button or press L
   - Select your black and white image
   - Default test image loads automatically

3. **Select First Color**
   - Choose from Preset Colors dropdown
   - Or click on image to see AI suggestions
   - Or use color gamut

4. **Add First Point**
   - Left-click on image where you want the color
   - Colored square appears
   - Image updates with colorization

5. **Add More Points**
   - Select different color
   - Left-click on different area
   - Repeat for all regions

6. **Adjust Points**
   - Left-click and drag to move points
   - Right-click to remove points
   - Mouse wheel to change brush size

7. **Save Result**
   - Click "Save" button or press S
   - Result saved in timestamped folder

### Advanced Workflow

#### Portrait Colorization
```
Step 1: Select "Human" category
Step 2: Choose "Skin - Medium"
Step 3: Add points on face, neck, hands
Step 4: Choose "Hair - Brown"
Step 5: Add points on hair
Step 6: Choose "Lips - Pink"
Step 7: Add point on lips
Step 8: Choose "Eyes - Blue"
Step 9: Add points on eyes
Step 10: Select "Fabrics" category for clothing
Step 11: Add points on clothing
Step 12: Adjust brush sizes for natural blending
Step 13: Save result
```

#### Landscape Colorization
```
Step 1: Select "Sky & Water" → "Sky - Blue"
Step 2: Add multiple points across sky
Step 3: Select "Nature" → "Grass - Green"
Step 4: Add points on grass areas
Step 5: Select "Nature" → "Leaves - Green"
Step 6: Add points on trees
Step 7: Select "Earth & Stone" → "Ground - Dirt"
Step 8: Add points on ground
Step 9: Add detail points for specific objects
Step 10: Adjust and refine
Step 11: Save result
```

## Mouse Controls

### Drawing Pad (Center Panel)

| Action | Control | Description |
|--------|---------|-------------|
| Add point | Left-click | Add new color point at cursor |
| Move point | Left-click + drag | Move existing point |
| Remove point | Right-click | Delete point at cursor |
| Increase brush | Scroll up | Make brush larger |
| Decrease brush | Scroll down | Make brush smaller |

### Color Selection (Left Panel)

| Action | Control | Description |
|--------|---------|-------------|
| Select preset | Click color square | Choose from preset palette |
| Change category | Dropdown menu | Switch color category |
| Select suggested | Click color square | Choose AI suggestion |
| Select from gamut | Click on gamut | Pick from ab color space |

## Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| **L** | Load | Open file dialog to load image |
| **S** | Save | Save current colorization result |
| **R** | Reset | Remove all points and start over |
| **G** | Gray | Toggle grayscale/color view |
| **Q** | Quit | Save and exit application |

## Tips & Best Practices

### General Tips
1. **Start with large areas**: Color backgrounds and major regions first
2. **Use multiple points**: Don't rely on single points for large areas
3. **Adjust brush size**: Larger for backgrounds, smaller for details
4. **Combine methods**: Use preset colors + AI suggestions together
5. **Work iteratively**: Add points, review, adjust, repeat

### Color Selection Tips
1. **Use preset colors for realism**: Pre-selected colors are based on real objects
2. **Check AI suggestions**: They're context-aware and often accurate
3. **Maintain consistency**: Use "Recently Used" for same colors
4. **Experiment**: Try different colors to see what works best

### Point Placement Tips
1. **Spread points evenly**: Don't cluster all points in one area
2. **Use appropriate density**: More points for complex areas
3. **Consider boundaries**: Place points at color transitions
4. **Layer colors**: Add base colors first, then details

### Brush Size Guidelines
- **Sky/Water**: 3-4x scale (large influence)
- **Grass/Ground**: 2-3x scale (medium influence)
- **Objects**: 1-2x scale (small influence)
- **Details**: 0.5-1x scale (precise control)

## Common Workflows

### Workflow 1: Quick Colorization
```
1. Load image
2. Select preset colors
3. Add 5-10 points across image
4. Save result
Time: 2-3 minutes
```

### Workflow 2: Detailed Colorization
```
1. Load image
2. Analyze image regions
3. Select appropriate preset categories
4. Add 20-30 points with varying brush sizes
5. Use AI suggestions for refinement
6. Adjust and fine-tune
7. Save result
Time: 10-15 minutes
```

### Workflow 3: Artistic Colorization
```
1. Load image
2. Use non-realistic colors from presets
3. Add selective points (partial colorization)
4. Experiment with color combinations
5. Save multiple variations
Time: 5-10 minutes per variation
```

## Troubleshooting

### Application Issues

**Q: Application won't start**
- Check conda environment is activated
- Verify PyQt5 is installed
- Check GPU availability

**Q: Application crashes on click**
- Update to latest version
- Check all files are present
- Review error log

### Colorization Issues

**Q: Colors look unnatural**
- Use preset colors for realistic results
- Add more points for smoother transitions
- Adjust brush sizes
- Check grayscale toggle is off

**Q: Can't add points**
- Click within image area (not border)
- Check if image is loaded
- Try clicking different location

**Q: Points won't move**
- Click directly on colored square
- Hold and drag
- Release to place

**Q: Can't remove points**
- Right-click directly on point
- Or press R to reset all

### Performance Issues

**Q: Slow colorization**
- Use GPU mode (--gpu 0)
- Reduce number of points
- Close other applications

**Q: Out of memory**
- Use smaller images
- Reduce batch size
- Use CPU mode if needed

## File Output

### Save Location
Results are saved in a timestamped folder next to the input image:
```
input_image_pytorch_YYMMDD_HHMMSS/
├── ours.png              # Colorized result (256x256)
├── ours_fullres.png      # Full resolution result
├── input.png             # Input with hints (256x256)
├── input_fullres.png     # Full resolution input
├── input_ab.png          # Color hints visualization
├── input_mask.png        # Mask showing hint locations
├── im_l.npy              # Luminance channel
├── im_ab.npy             # Color channels
└── im_mask.npy           # Mask data
```

### File Descriptions
- **ours.png**: Main colorized result at model resolution
- **ours_fullres.png**: Upsampled to original image size
- **input_*.png**: Shows your color hints
- ***.npy**: Raw data for further processing

## Advanced Features

### Distribution Model
- Predicts color distribution at each pixel
- Provides AI-suggested colors
- Enables intelligent colorization

### Color Gamut
- Shows valid colors for given luminance
- Prevents impossible color combinations
- Real-time gamut updates

### Brush Size Control
- Adjustable influence area
- Mouse wheel control
- Visual feedback

## Performance

### Speed
- Point addition: Instant
- Colorization update: 1-2 seconds (GPU)
- Full resolution save: 2-3 seconds

### Quality
- Model resolution: 256x256
- Output resolution: Original image size
- Upsampling: Bilinear interpolation

## Resources

### Documentation
- `README_PRESET_COLORS.md` - Preset color guide
- `MULTIPOINT_GUIDE.md` - Multi-point feature guide
- `PRESET_COLORS_GUIDE.md` - Detailed color reference
- `CHANGELOG.md` - Version history
- `FIXES_APPLIED.md` - Technical fixes

### Examples
- Test images in `test_imgs/` directory
- Sample results in saved folders

## Support

For issues or questions:
1. Check this guide
2. Review documentation files
3. Check GitHub repository
4. Report issues with error logs

## Credits

Based on "Real-Time User-Guided Image Colorization with Learned Deep Priors"
by Zhang et al., SIGGRAPH 2017

Enhanced with:
- Preset color palette system
- Multi-point colorization
- Improved user interface
- Comprehensive documentation
