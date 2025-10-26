# Feature: Dynamic Image Size Support

## What's New

The colorization system now supports passing actual image dimensions to the model instead of always resizing to 256x256.

## Quick Usage

```bash
# Activate environment
conda activate rvrt

# Use dynamic sizing
python ideepcolor.py --use_dynamic_size --gpu 0 --backend pytorch
```

## Comparison

| Mode | Command | Image Size | Aspect Ratio |
|------|---------|------------|--------------|
| **Fixed (Default)** | `python ideepcolor.py` | Always 256x256 | Not preserved |
| **Dynamic** | `python ideepcolor.py --use_dynamic_size` | Actual size (÷4) | Preserved |

## Example

For a 600x507 image:

**Fixed mode:**
- Input: 256x256 ❌ (aspect ratio changed)

**Dynamic mode:**
- Input: 600x504 ✅ (aspect ratio preserved, adjusted to multiple of 4)

## When to Use

### Use Dynamic Mode (`--use_dynamic_size`) when:
- ✅ Working with non-square images
- ✅ Aspect ratio is important
- ✅ You want maximum detail
- ✅ You have sufficient GPU memory

### Use Fixed Mode (default) when:
- ✅ Batch processing many images
- ✅ Limited GPU memory
- ✅ Need consistent processing time
- ✅ Speed is priority

## Test Results

Tested and verified:
- ✅ PyTorch backend
- ✅ GPU mode (CUDA)
- ✅ Aspect ratio preservation
- ✅ Backward compatibility
- ✅ UI functionality

See `TEST_RESULTS.md` for detailed test results.

## Documentation

- **Quick Start:** `QUICK_START.md`
- **User Guide:** `DYNAMIC_SIZE_GUIDE.md`
- **Examples:** `EXAMPLE_USAGE.md`
- **Technical Details:** `CHANGES_DYNAMIC_SIZE.md`
- **Test Results:** `TEST_RESULTS.md`

## Implementation

Modified files:
- `data/colorize_image.py` - Core colorization classes
- `ideepcolor.py` - Command-line interface
- `ui/gui_draw.py` - UI drawing logic
- `ui/ui_control.py` - UI control logic

New files:
- `test_dynamic_size.py` - Test script
- Documentation files (*.md)

## Status

✅ **READY FOR USE**

The feature has been implemented, tested, and documented. It's ready for production use with the `rvrt` conda environment.
