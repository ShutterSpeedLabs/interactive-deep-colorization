# iDeepColor - Changelog

## Latest Updates

### Added Preset Color Palette System

**New Features:**
- Comprehensive preset color palette with 150+ colors organized in 7 categories
- Dropdown category selector for easy navigation
- Scrollable color grid with visual selection feedback
- Color name display showing the selected color
- Integration with existing color selection workflow

**Categories Added:**
1. **Human** (25 colors) - Skin tones, hair, lips, eyes
2. **Nature** (18 colors) - Grass, leaves, wood
3. **Earth & Stone** (13 colors) - Stone, ground, rocks
4. **Sky & Water** (16 colors) - Sky, clouds, water
5. **Materials** (11 colors) - Metals, glass
6. **Fabrics** (15 colors) - Clothing and textile colors
7. **Objects** (26 colors) - Cars, buildings, flowers, etc.

**New Files:**
- `ui/color_presets.py` - Color definitions and utilities
- `ui/gui_preset_palette.py` - Preset palette widget implementation
- `PRESET_COLORS_GUIDE.md` - Comprehensive usage guide

**Modified Files:**
- `ui/gui_design.py` - Added preset palette to main GUI
- `ui/gui_draw.py` - Fixed signal type for used_colors

### Bug Fixes

#### Qt Plugin Conflicts
- **Issue**: OpenCV's bundled Qt plugins conflicted with PyQt5
- **Fix**: Removed cv2's Qt plugin directory
- **Impact**: Application now starts without Qt platform plugin errors

#### GUI Widget Initialization
- **Issue**: NoneType errors when interacting with widgets before image load
- **Fix**: Added None checks in `gui_gamut.py` and `gui_palette.py`
- **Impact**: Widgets handle uninitialized state gracefully

#### Color Signal Type Mismatch
- **Issue**: `used_colors_signal` expected list but received numpy array
- **Fix**: Changed signal type from `list` to `np.ndarray`
- **Impact**: Recently used colors now display correctly

#### Image Loading
- **Issue**: Application crashed when canceling file dialog
- **Fix**: Added check for empty file path in `load_image()`
- **Impact**: Canceling file dialog no longer crashes application

### Technical Improvements

**Signal Handling:**
- Standardized signal types across widgets
- Improved error handling for None values
- Better integration between preset and dynamic palettes

**Code Organization:**
- Separated color definitions into dedicated module
- Modular widget design for easy extension
- Clear separation of concerns

**User Experience:**
- Preset colors available immediately on startup
- No need to click on image to access color palette
- Visual feedback for selected colors
- Descriptive color names for better understanding

## Installation & Usage

### Requirements
- Python 3.8+
- PyTorch
- PyQt5
- OpenCV
- scikit-image
- scikit-learn
- qdarkstyle

### Running the Application
```bash
conda activate rvrt
python ideepcolor.py --gpu 0 --backend pytorch
```

### Quick Start
1. Application opens with default test image
2. Select a category from "Preset Colors" dropdown
3. Click a color from the preset palette
4. Click on the image to apply the color
5. Use AI-suggested colors for additional options
6. Save your colorized result

## Known Issues

None currently reported.

## Future Roadmap

- [ ] Custom color palette import/export
- [ ] Color history persistence
- [ ] Batch processing support
- [ ] Additional preset categories (seasonal, regional)
- [ ] Color mixing and blending tools
- [ ] Undo/redo functionality enhancement
- [ ] Keyboard shortcuts for color categories

## Contributing

To add new preset colors:
1. Edit `ui/color_presets.py`
2. Add colors to existing categories or create new ones
3. Colors should be RGB tuples (0-255)
4. Test with various images

## Version History

### v1.1.0 (Current)
- Added preset color palette system
- Fixed Qt plugin conflicts
- Fixed GUI initialization bugs
- Improved signal handling
- Enhanced documentation

### v1.0.0 (Original)
- Initial release with PyTorch backend support
- Interactive colorization with local hints
- Distribution-based color suggestions
- GUI interface with color gamut
