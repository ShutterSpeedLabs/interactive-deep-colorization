"""
ComfyUI Custom Nodes for Interactive Deep Colorization

Installation:
1. Copy this file to: ComfyUI/custom_nodes/ideepcolor_nodes.py
2. Copy required files to: ComfyUI/custom_nodes/ideepcolor/
   - data/colorize_image.py
   - models/pytorch/caffemodel.pth
   - auto_colorize_from_reference.py
3. Restart ComfyUI

Usage:
- Add "iDeepColor Colorize" node to your workflow
- Connect grayscale image input
- Optionally add color hints
- Get colorized output
"""

import torch
import numpy as np
import cv2
from PIL import Image
import sys
import os

# Add path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'ideepcolor'))

try:
    from data import colorize_image as CI
    from auto_colorize_from_reference import AutoColorizeFromReference
except ImportError:
    print("Warning: iDeepColor modules not found. Please install dependencies.")


class iDeepColorColorize:
    """
    Interactive Deep Colorization Node
    
    Colorizes grayscale images using deep learning with optional color hints.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # Grayscale image
                "model_path": ("STRING", {
                    "default": "models/pytorch/caffemodel.pth"
                }),
                "use_gpu": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "color_hints": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "x,y,r,g,b (one per line)"
                }),
                "use_dynamic_size": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "colorize"
    CATEGORY = "image/colorization"
    
    def __init__(self):
        self.model = None
        self.model_path = None
    
    def load_model(self, model_path, use_gpu):
        """Load colorization model"""
        if self.model is None or self.model_path != model_path:
            print(f"Loading iDeepColor model from {model_path}")
            
            gpu_id = 0 if use_gpu and torch.cuda.is_available() else -1
            
            self.model = CI.ColorizeImageTorch(Xd=256, use_dynamic_size=False)
            self.model.prep_net(gpu_id=gpu_id, path=model_path)
            self.model_path = model_path
            
            print(f"Model loaded on {'GPU' if gpu_id >= 0 else 'CPU'}")
    
    def parse_color_hints(self, color_hints_str):
        """Parse color hints from string"""
        if not color_hints_str or color_hints_str.strip() == "":
            return []
        
        hints = []
        for line in color_hints_str.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    parts = [int(p.strip()) for p in line.split(',')]
                    if len(parts) == 5:
                        hints.append(tuple(parts))
                except:
                    continue
        
        return hints
    
    def colorize(self, image, model_path, use_gpu, color_hints="", use_dynamic_size=False):
        """
        Colorize grayscale image
        
        Args:
            image: Input image tensor (B, H, W, C)
            model_path: Path to model weights
            use_gpu: Whether to use GPU
            color_hints: Color hints as string "x,y,r,g,b"
            use_dynamic_size: Use dynamic image sizing
            
        Returns:
            Colorized image tensor (B, H, W, C)
        """
        # Load model
        self.load_model(model_path, use_gpu)
        
        # Convert tensor to numpy
        img_np = image[0].cpu().numpy()  # (H, W, C)
        
        # Ensure RGB format
        if img_np.shape[2] == 1:
            img_np = np.repeat(img_np, 3, axis=2)
        
        # Convert to uint8
        img_np = (img_np * 255).astype(np.uint8)
        
        # Set image in model
        self.model.set_image(img_np)
        
        # Parse and apply color hints
        hints = self.parse_color_hints(color_hints)
        
        if len(hints) > 0:
            print(f"Applying {len(hints)} color hints")
            
            # Create color hint arrays
            h, w = img_np.shape[:2]
            im_ab = np.zeros((2, h, w))
            im_mask = np.zeros((1, h, w))
            
            for x, y, r, g, b in hints:
                if 0 <= x < w and 0 <= y < h:
                    # Convert RGB to LAB
                    rgb_pixel = np.array([[[r, g, b]]], dtype=np.uint8)
                    lab_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_RGB2LAB)[0, 0]
                    
                    # Set a, b values
                    im_ab[0, y, x] = lab_pixel[1] - 128  # a
                    im_ab[1, y, x] = lab_pixel[2] - 128  # b
                    im_mask[0, y, x] = 1
            
            # Apply hints
            self.model.net_forward(im_ab, im_mask)
        else:
            # No hints - automatic colorization
            im_ab = np.zeros((2, img_np.shape[0], img_np.shape[1]))
            im_mask = np.zeros((1, img_np.shape[0], img_np.shape[1]))
            self.model.net_forward(im_ab, im_mask)
        
        # Get result
        result = self.model.get_img_forward()
        
        # Convert back to tensor
        result_tensor = torch.from_numpy(result.astype(np.float32) / 255.0)
        result_tensor = result_tensor.unsqueeze(0)  # Add batch dimension
        
        return (result_tensor,)


class iDeepColorAutoColorize:
    """
    Auto-colorize from reference image using feature matching
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gray_image": ("IMAGE",),
                "reference_image": ("IMAGE",),
                "num_points": ("INT", {
                    "default": 30,
                    "min": 5,
                    "max": 100,
                    "step": 5
                }),
                "method": (["orb", "sift", "akaze"],),
            }
        }
    
    RETURN_TYPES = ("STRING",)  # Returns color hints as string
    FUNCTION = "auto_colorize"
    CATEGORY = "image/colorization"
    
    def __init__(self):
        self.auto_colorizer = None
    
    def auto_colorize(self, gray_image, reference_image, num_points=30, method="orb"):
        """
        Extract color points from reference image
        
        Returns:
            String with color hints (x,y,r,g,b format)
        """
        # Initialize auto-colorizer
        if self.auto_colorizer is None:
            self.auto_colorizer = AutoColorizeFromReference(
                method=method,
                num_points=num_points,
                match_threshold=0.75
            )
        
        # Convert tensors to numpy
        gray_np = (gray_image[0].cpu().numpy() * 255).astype(np.uint8)
        ref_np = (reference_image[0].cpu().numpy() * 255).astype(np.uint8)
        
        # Extract color points
        color_points, _ = self.auto_colorizer.extract_color_points(
            gray_np, ref_np, visualize=False
        )
        
        # Format as string
        hints_str = ""
        for x, y, r, g, b in color_points:
            hints_str += f"{x},{y},{r},{g},{b}\n"
        
        print(f"Extracted {len(color_points)} color points")
        
        return (hints_str,)


class iDeepColorMaskedColorize:
    """
    Apply colorization only to masked regions
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gray_image": ("IMAGE",),
                "colorized_image": ("IMAGE",),
                "mask": ("MASK",),
                "smooth_edges": ("BOOLEAN", {"default": True}),
                "blur_size": ("INT", {
                    "default": 15,
                    "min": 1,
                    "max": 51,
                    "step": 2
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "masked_colorize"
    CATEGORY = "image/colorization"
    
    def masked_colorize(self, gray_image, colorized_image, mask, 
                       smooth_edges=True, blur_size=15):
        """
        Apply colorization only to masked regions
        """
        # Convert to numpy
        gray_np = gray_image[0].cpu().numpy()
        color_np = colorized_image[0].cpu().numpy()
        mask_np = mask[0].cpu().numpy()
        
        # Smooth mask if requested
        if smooth_edges:
            if blur_size % 2 == 0:
                blur_size += 1
            mask_np = cv2.GaussianBlur(mask_np, (blur_size, blur_size), 0)
        
        # Expand mask to 3 channels
        mask_3ch = mask_np[:, :, np.newaxis]
        
        # Blend
        result = mask_3ch * color_np + (1 - mask_3ch) * gray_np
        
        # Convert back to tensor
        result_tensor = torch.from_numpy(result.astype(np.float32))
        result_tensor = result_tensor.unsqueeze(0)
        
        return (result_tensor,)


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "iDeepColorColorize": iDeepColorColorize,
    "iDeepColorAutoColorize": iDeepColorAutoColorize,
    "iDeepColorMaskedColorize": iDeepColorMaskedColorize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "iDeepColorColorize": "iDeepColor Colorize",
    "iDeepColorAutoColorize": "iDeepColor Auto-Colorize",
    "iDeepColorMaskedColorize": "iDeepColor Masked Colorize",
}
