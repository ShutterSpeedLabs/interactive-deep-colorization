# Preset Color Palette Guide

## Overview
A comprehensive preset color palette system has been added to iDeepColor, providing easy access to realistic colors for common objects and materials when colorizing black and white images.

## Features

### 7 Color Categories with 150+ Preset Colors

#### 1. **Human** (25 colors)
Colors for realistic human features:
- **Skin Tones**: Fair, Light, Medium, Tan, Brown, Dark (6 variations)
- **Hair Colors**: Blonde, Light Brown, Brown, Dark Brown, Black, Red, Auburn, Gray, White (9 variations)
- **Lips**: Light Pink, Pink, Rose, Red, Dark Red (5 variations)
- **Eyes**: Blue, Green, Brown, Hazel, Gray (5 variations)

#### 2. **Nature** (18 colors)
Natural vegetation and wood colors:
- **Grass**: Light Green, Green, Dark Green, Yellow Green, Dry (5 variations)
- **Leaves**: Spring Green, Green, Dark Green, Autumn Yellow, Autumn Orange, Autumn Red, Brown (7 variations)
- **Wood**: Light, Oak, Walnut, Dark, Mahogany, Tree Bark (6 variations)

#### 3. **Earth & Stone** (13 colors)
Ground and stone materials:
- **Stone**: Light Gray, Gray, Dark Gray, Granite, Marble, Sandstone (6 variations)
- **Ground**: Sand, Dirt, Clay, Mud, Soil (5 variations)
- **Rock**: Brown, Red (2 variations)

#### 4. **Sky & Water** (16 colors)
Atmospheric and water colors:
- **Sky**: Light Blue, Blue, Deep Blue, Sunset Orange, Sunset Pink, Sunset Purple, Overcast (7 variations)
- **Clouds**: White, Gray, Dark Gray (3 variations)
- **Water**: Light Blue, Blue, Deep Blue, Turquoise, Teal, Dark (6 variations)

#### 5. **Materials** (11 colors)
Common material colors:
- **Metals**: Silver, Gold, Bronze, Copper, Iron, Steel, Chrome (7 variations)
- **Glass**: Clear, Blue, Green, Amber (4 variations)

#### 6. **Fabrics** (15 colors)
Textile and clothing colors:
- **Neutrals**: White, Cream, Beige, Gray, Black (5 variations)
- **Colors**: Red, Blue, Navy, Green, Yellow, Orange, Purple, Pink, Brown, Denim (10 variations)

#### 7. **Objects** (26 colors)
Common objects in photographs:
- **Cars**: Red, Blue, Black, White, Silver, Yellow (6 variations)
- **Buildings**: Brick Red, Concrete, White, Beige (4 variations)
- **Roads**: Asphalt, Concrete (2 variations)
- **Roofs**: Red Tile, Gray Shingle, Black (3 variations)
- **Doors**: Wood, White, Red (3 variations)
- **Windows**: Glass (1 variation)
- **Flowers**: Red, Pink, Yellow, Purple, White, Orange (6 variations)

## How to Use

### In the GUI:
1. **Launch the application** with the preset palette visible on the left side
2. **Select a category** from the dropdown menu (e.g., "Human", "Nature", "Objects")
3. **Click on any color** in the palette to select it
4. **The selected color name** will be displayed below the palette
5. **Click on the image** to apply the color at that location

### Workflow Tips:
- **Start with broad categories**: Use "Sky & Water" for backgrounds, "Nature" for landscapes
- **Use Human colors** for portraits: Select appropriate skin tone, then hair, eyes, and lips
- **Layer colors**: Apply base colors first, then add details with more specific colors
- **Combine with AI suggestions**: Use preset colors alongside the AI-suggested colors for best results

## Technical Details

### File Structure:
```
ui/
├── color_presets.py          # Color definitions and utilities
├── gui_preset_palette.py     # Preset palette widget
└── gui_design.py             # Updated to include preset palette
```

### Color Format:
- All colors are stored as RGB tuples (0-255)
- Colors are organized in dictionaries by category
- Easy to extend with new categories or colors

### Adding Custom Colors:
Edit `ui/color_presets.py` to add new colors or categories:

```python
# Add to existing category
HUMAN_COLORS['Skin - Custom'] = (200, 150, 100)

# Or create new category
CUSTOM_COLORS = {
    'Custom Color 1': (255, 128, 0),
    'Custom Color 2': (128, 255, 0),
}

# Add to COLOR_CATEGORIES
COLOR_CATEGORIES['Custom'] = CUSTOM_COLORS
```

## Use Cases

### Portrait Colorization:
1. Select "Human" category
2. Choose appropriate skin tone for face
3. Select hair color for hair regions
4. Add eye colors
5. Apply lip color
6. Use "Fabrics" for clothing

### Landscape Colorization:
1. Select "Sky & Water" for sky
2. Use "Nature" for grass and trees
3. Apply "Earth & Stone" for ground and rocks
4. Add "Objects" colors for buildings or vehicles

### Historical Photo Restoration:
1. Use realistic "Human" tones for people
2. Apply period-appropriate "Fabrics" colors
3. Use "Objects" colors for vehicles and buildings
4. Add natural "Nature" and "Sky & Water" colors

### Architectural Photos:
1. Use "Objects" for building materials
2. Apply "Materials" for metal and glass elements
3. Add "Nature" for landscaping
4. Use "Sky & Water" for backgrounds

## Benefits

1. **Speed**: Quickly select realistic colors without guessing
2. **Consistency**: Use the same color across multiple areas
3. **Realism**: Pre-selected colors are based on real-world objects
4. **Learning**: Color names help understand what colors work for different materials
5. **Flexibility**: Combine with AI suggestions and manual color selection

## Keyboard Shortcuts

The preset palette works seamlessly with existing shortcuts:
- **R**: Reset all colors
- **S**: Save result
- **L**: Load new image
- **G**: Toggle grayscale view
- **Q**: Save and quit

## Future Enhancements

Potential additions:
- Custom color palette saving/loading
- Color history across sessions
- Color mixing tools
- Import colors from reference images
- Seasonal color variations
- Regional color palettes (e.g., Mediterranean, Nordic)

## Credits

Color values are based on:
- Standard RGB color references
- Real-world material colors
- Photography color grading standards
- Digital art color palettes
