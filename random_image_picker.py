"""
Random Image Picker Node Implementation
"""

import os
import random
from pathlib import Path
from typing import Tuple, List
import folder_paths
from PIL import Image
import numpy as np
import torch


class RandomImagePicker:
    """
    ComfyUI node that loads either a single image or a random image from a folder.
    Supports subfolder scanning and outputs image with resolution information.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        # Get default input directory from ComfyUI
        try:
            default_path = folder_paths.get_input_directory()
        except:
            default_path = ""
        
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": default_path, 
                    "multiline": False,
                    "dynamicPrompts": False,
                    "tooltip": "Folder path for random image selection (Folder mode only)"
                }),
                "folder_mode": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "Folder", 
                    "label_off": "Single",
                    "tooltip": "Single: Use file picker | Folder: Random from folder path"
                }),
                "include_subfolders": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "ON", 
                    "label_off": "OFF",
                    "tooltip": "Include subfolders when scanning in Folder mode"
                }),
                "seed": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff,
                    "tooltip": "Random seed for reproducible selection in Folder mode"
                }),
            },
            "optional": {
                "image_data": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "forceInput": True,
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("IMAGE", "width", "height")
    FUNCTION = "load_image"
    CATEGORY = "image"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False, False, False)
    
    @staticmethod
    def get_image_files(directory: str, include_subfolders: bool = False) -> List[str]:
        """
        Get all image files from a directory.
        
        Args:
            directory: Directory path to scan
            include_subfolders: Whether to include subfolders in the scan
            
        Returns:
            List of image file paths
        """
        supported_formats = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif'}
        image_files = []
        
        if include_subfolders:
            for root, _, files in os.walk(directory):
                for file in files:
                    if Path(file).suffix.lower() in supported_formats:
                        image_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and Path(file).suffix.lower() in supported_formats:
                    image_files.append(file_path)
        
        return image_files
    
    @staticmethod
    def load_image_file(image_path: str) -> Tuple[torch.Tensor, int, int]:
        """
        Load an image file and convert to ComfyUI format.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (image_tensor, width, height)
        """
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get dimensions
        width, height = img.size
        
        # Convert to numpy array
        img_array = np.array(img).astype(np.float32) / 255.0
        
        # Convert to torch tensor and add batch dimension
        # ComfyUI expects [batch, height, width, channels]
        img_tensor = torch.from_numpy(img_array)[None,]
        
        return img_tensor, width, height
    
    def load_image(self, folder_path: str, folder_mode: bool, include_subfolders: bool, seed: int, image_data: str = ""):
        """
        Load image based on mode settings.
        
        Args:
            folder_path: Folder path for random selection
            folder_mode: True for explicit folder mode, False for auto-detect
            include_subfolders: Whether to scan subfolders
            seed: Random seed for folder mode
            image_data: Base64 encoded image data from file picker
            
        Returns:
            Tuple of (image_tensor, width, height)
        """
        # Priority 1: Check if folder_path is valid (works for both modes)
        if folder_path and os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Use folder mode (random selection)
            image_files = self.get_image_files(folder_path, include_subfolders)
            
            if not image_files:
                raise ValueError(f"No image files found in directory: {folder_path}")
            
            # Use seed for reproducible random selection
            random.seed(seed)
            selected_image = random.choice(image_files)
            
            mode_str = "Folder Mode" if folder_mode else "Auto (from folder_path)"
            print(f"[Random Image Picker] Mode: {mode_str}")
            print(f"[Random Image Picker] Folder: {folder_path}")
            print(f"[Random Image Picker] Selected: {selected_image}")
            return self.load_image_file(selected_image)
        
        # Priority 2: Use file picker data if available
        if image_data:
            import base64
            import io
            
            try:
                # Remove data URL prefix if present
                if ',' in image_data:
                    image_data = image_data.split(',', 1)[1]
                
                # Decode base64
                img_bytes = base64.b64decode(image_data)
                img = Image.open(io.BytesIO(img_bytes))
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get dimensions
                width, height = img.size
                
                # Convert to numpy array
                img_array = np.array(img).astype(np.float32) / 255.0
                
                # Convert to torch tensor and add batch dimension
                img_tensor = torch.from_numpy(img_array)[None,]
                
                print(f"[Random Image Picker] Mode: File Picker")
                print(f"[Random Image Picker] Loaded: {width}x{height}")
                return (img_tensor, width, height)
                
            except Exception as e:
                raise ValueError(f"Failed to load image from file picker: {str(e)}")
        
        # No valid input provided
        raise ValueError(
            "No valid input provided.\n\n"
            "Please either:\n"
            "1. Enter a folder path in 'folder_path' field, OR\n"
            "2. Use the 📁 Choose File button to select an image"
        )


# Node registration
NODE_CLASS_MAPPINGS = {
    "RandomImagePicker": RandomImagePicker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomImagePicker": "Random Image Picker"
}
