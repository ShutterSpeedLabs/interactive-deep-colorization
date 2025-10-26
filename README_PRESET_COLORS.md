# Preset Color Palette - Quick Reference

## What's New?

A new **Preset Colors** panel has been added to iDeepColor, providing instant access to 150+ realistic colors organized by category. This makes colorizing black and white images faster and more intuitive.

## Quick Start

### 1. Launch the Application
```bash
conda activate rvrt
python ideepcolor.py --gpu 0 --backend pytorch
```

### 2. Using Preset Colors

**The preset palette is located on the left side of the interface:**

```
┌─────────────────────────────────┐
│  ab Color Gamut                 │
├─────────────────────────────────┤
│  Suggested colors (AI)          │
├─────────────────────────────────┤
│  Recently used colors           │
├─────────────────────────────────┤
│  ┌───────────────────────────┐  │
│  │ Preset Colors             │  │
│  │ [Category Dropdown ▼]     │  │
│  │ ┌─┬─┬─┬─┬─┬─┐            │  │
│  │ │█│█│█│█│█│█│            │  │
│  │ ├─┼─┼─┼─┼─┼─┤            │  │
│  │ │█│█│█│█│█│█│ (scrollable)│  │
│  │ └─┴─┴─┴─┴─┴─┘            │  │
│  │ Selected: Skin - Medium   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### 3. Workflow

1. **Select Category**: Choose from dropdown (Human, Nature, Objects, etc.)
2. **Pick Color**: Click on any color square
3. **Apply**: Click on the image where you want to apply the color
4. **Repeat**: Select different colors for different areas

## Color Categories

### 🧑 Human (25 colors)
Perfect for portraits and people:
- 6 skin tones (Fair to Dark)
- 9 hair colors (Blonde to White)
- 5 lip colors (Light Pink to Dark Red)
- 5 eye colors (Blue, Green, Brown, Hazel, Gray)

**Example Use**: Colorizing old family photos

### 🌳 Nature (18 colors)
For landscapes and vegetation:
- 5 grass variations
- 7 leaf colors (including autumn)
- 6 wood tones

**Example Use**: Colorizing landscape photographs

### 🪨 Earth & Stone (13 colors)
Ground and stone materials:
- 6 stone types
- 5 ground variations
- 2 rock colors

**Example Use**: Architectural photos, geological images

### ☁️ Sky & Water (16 colors)
Atmospheric elements:
- 7 sky colors (including sunset)
- 3 cloud variations
- 6 water colors

**Example Use**: Outdoor scenes, seascapes

### 🔩 Materials (11 colors)
Common materials:
- 7 metal types (Silver, Gold, Bronze, etc.)
- 4 glass variations

**Example Use**: Industrial photos, jewelry

### 👕 Fabrics (15 colors)
Clothing and textiles:
- 5 neutral colors
- 10 vibrant colors

**Example Use**: Fashion photos, clothing

### 🚗 Objects (26 colors)
Common objects:
- 6 car colors
- 4 building colors
- 3 roof types
- 6 flower colors
- And more...

**Example Use**: Street scenes, urban photography

## Tips & Tricks

### For Best Results:

1. **Start with backgrounds**: Apply sky, water, or ground colors first
2. **Work from large to small**: Color large areas before details
3. **Use multiple categories**: Combine colors from different categories
4. **Combine with AI**: Use preset colors alongside AI suggestions
5. **Experiment**: Try different shades to find the best match

### Common Workflows:

**Portrait Colorization:**
```
1. Human → Skin tone (face, hands)
2. Human → Hair color
3. Human → Eye color
4. Human → Lip color
5. Fabrics → Clothing
6. Nature/Objects → Background
```

**Landscape Colorization:**
```
1. Sky & Water → Sky
2. Nature → Grass/trees
3. Earth & Stone → Ground/rocks
4. Objects → Buildings/vehicles
```

**Historical Photos:**
```
1. Human → Realistic skin tones
2. Fabrics → Period-appropriate colors
3. Objects → Historical vehicle/building colors
4. Nature → Natural environment
```

## Keyboard Shortcuts

- **R**: Reset all colors
- **S**: Save result
- **L**: Load new image
- **G**: Toggle grayscale view
- **Q**: Save and quit

## Advantages Over Manual Selection

| Feature | Manual Selection | Preset Colors |
|---------|-----------------|---------------|
| Speed | Slow (trial & error) | Fast (one click) |
| Accuracy | Variable | Realistic |
| Consistency | Difficult | Easy |
| Learning Curve | Steep | Gentle |
| Color Names | Unknown | Descriptive |

## Examples

### Before Preset Colors:
1. Click on image
2. Wait for AI suggestions
3. Try to guess appropriate color
4. Adjust in color gamut
5. Hope it looks realistic

### With Preset Colors:
1. Select "Human" category
2. Click "Skin - Medium"
3. Click on face
4. Done! ✓

## Troubleshooting

**Q: Preset palette not showing?**
A: Make sure you're running the latest version with all files updated.

**Q: Colors look wrong?**
A: Try different shades from the same category, or combine with AI suggestions.

**Q: Can I add my own colors?**
A: Yes! Edit `ui/color_presets.py` to add custom colors.

**Q: How do I know which color to use?**
A: Color names are descriptive (e.g., "Skin - Medium", "Grass - Green"). Hover or select to see the name.

## Technical Notes

- Colors are stored as RGB values (0-255)
- All colors are based on real-world references
- Easy to extend with new categories
- Integrates seamlessly with existing features

## Support

For issues or suggestions:
1. Check the full guide: `PRESET_COLORS_GUIDE.md`
2. Review changelog: `CHANGELOG.md`
3. Check fixes applied: `FIXES_APPLIED.md`

## Summary

The preset color palette makes colorizing black and white images:
- ✅ **Faster** - No guessing or trial and error
- ✅ **Easier** - One-click color selection
- ✅ **More Realistic** - Pre-selected accurate colors
- ✅ **More Intuitive** - Organized by category
- ✅ **More Consistent** - Same colors across images

**Start colorizing with confidence!** 🎨
