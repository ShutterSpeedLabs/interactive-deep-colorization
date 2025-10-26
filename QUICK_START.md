# Quick Start: Dynamic Image Size

## Setup
```bash
conda activate rvrt
```

## Basic Usage

### Default (Fixed 256x256)
```bash
python ideepcolor.py --image_file test_imgs/mortar_pestle.jpg
```

### Dynamic Size (Preserves Aspect Ratio)
```bash
python ideepcolor.py --use_dynamic_size --image_file test_imgs/mortar_pestle.jpg
```

## Common Commands

```bash
# GPU mode (default)
python ideepcolor.py --use_dynamic_size --gpu 0

# CPU mode
python ideepcolor.py --use_dynamic_size --cpu_mode

# PyTorch backend (default)
python ideepcolor.py --use_dynamic_size --backend pytorch

# Caffe backend
python ideepcolor.py --use_dynamic_size --backend caffe

# Custom window size
python ideepcolor.py --use_dynamic_size --win_size 512
```

## Test the Feature

```bash
python test_dynamic_size.py --image test_imgs/mortar_pestle.jpg --backend pytorch
```

## When to Use

✅ **Use `--use_dynamic_size` for:**
- Non-square images
- Preserving aspect ratio
- Maximum detail

❌ **Use default (fixed) for:**
- Batch processing
- Limited GPU memory
- Faster processing

## More Info

- Full guide: `DYNAMIC_SIZE_GUIDE.md`
- Examples: `EXAMPLE_USAGE.md`
- Technical details: `CHANGES_DYNAMIC_SIZE.md`
