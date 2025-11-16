#!/bin/bash
# Installation script for iDeepColor ComfyUI nodes

echo "=========================================="
echo "iDeepColor ComfyUI Installation"
echo "=========================================="

# Check if ComfyUI path is provided
if [ -z "$1" ]; then
    echo "Usage: ./install_comfyui.sh /path/to/ComfyUI"
    echo "Example: ./install_comfyui.sh ~/ComfyUI"
    exit 1
fi

COMFYUI_PATH="$1"
CUSTOM_NODES_PATH="$COMFYUI_PATH/custom_nodes"

# Check if ComfyUI exists
if [ ! -d "$COMFYUI_PATH" ]; then
    echo "Error: ComfyUI directory not found: $COMFYUI_PATH"
    exit 1
fi

echo "ComfyUI path: $COMFYUI_PATH"
echo "Custom nodes path: $CUSTOM_NODES_PATH"

# Create custom_nodes directory if it doesn't exist
mkdir -p "$CUSTOM_NODES_PATH"

# Create ideepcolor directory
echo ""
echo "Creating ideepcolor directory..."
mkdir -p "$CUSTOM_NODES_PATH/ideepcolor"
mkdir -p "$CUSTOM_NODES_PATH/ideepcolor/data"
mkdir -p "$CUSTOM_NODES_PATH/ideepcolor/models/pytorch"

# Copy node file
echo "Copying node file..."
cp comfyui_nodes.py "$CUSTOM_NODES_PATH/ideepcolor_nodes.py"

# Copy required modules
echo "Copying required modules..."
cp -r data/*.py "$CUSTOM_NODES_PATH/ideepcolor/data/"
cp auto_colorize_from_reference.py "$CUSTOM_NODES_PATH/ideepcolor/"

# Copy model if it exists
if [ -f "models/pytorch/caffemodel.pth" ]; then
    echo "Copying model weights..."
    cp models/pytorch/caffemodel.pth "$CUSTOM_NODES_PATH/ideepcolor/models/pytorch/"
else
    echo "Warning: Model file not found. Please copy manually:"
    echo "  cp models/pytorch/caffemodel.pth $CUSTOM_NODES_PATH/ideepcolor/models/pytorch/"
fi

# Create __init__.py files
echo "Creating __init__.py files..."
touch "$CUSTOM_NODES_PATH/ideepcolor/__init__.py"
touch "$CUSTOM_NODES_PATH/ideepcolor/data/__init__.py"

echo ""
echo "=========================================="
echo "Installation Summary"
echo "=========================================="
echo "✓ Node file copied"
echo "✓ Modules copied"
echo "✓ Directory structure created"

if [ -f "$CUSTOM_NODES_PATH/ideepcolor/models/pytorch/caffemodel.pth" ]; then
    echo "✓ Model weights copied"
else
    echo "⚠ Model weights not copied (manual copy required)"
fi

echo ""
echo "Next steps:"
echo "1. Install dependencies in ComfyUI environment:"
echo "   cd $COMFYUI_PATH"
echo "   pip install scikit-learn scikit-image opencv-python"
echo ""
echo "2. Restart ComfyUI"
echo ""
echo "3. Look for 'iDeepColor' nodes in the node menu"
echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
