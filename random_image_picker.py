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
from nodes import SaveImage


class RandomImagePicker(SaveImage):
    """
    ComfyUI node that loads either a single image or a random image from a folder.
    Supports subfolder scanning and outputs image with resolution information.
    """
    
    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
        self.compress_level = 4
    
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
                "image_data": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Base64 image data from file picker (auto-filled)"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "load_image"
    CATEGORY = "image"
    OUTPUT_NODE = True
    
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
            folder_path: Folder path for random selection (used when folder_mode=True)
            folder_mode: True=Folder random selection, False=File picker
            include_subfolders: Whether to scan subfolders
            seed: Random seed for folder mode
            image_data: Base64 encoded image data from file picker (used when folder_mode=False)
            
        Returns:
            Dict with ui (for preview) and result (IMAGE tensor)
        """
        if folder_mode:
            # Folder mode: random selection from folder_path
            if not folder_path or not os.path.exists(folder_path):
                raise ValueError(f"Folder mode is enabled but folder_path is invalid: {folder_path}")
            
            if not os.path.isdir(folder_path):
                raise ValueError(f"Folder mode requires a directory path, not a file: {folder_path}")
            
            image_files = self.get_image_files(folder_path, include_subfolders)
            
            if not image_files:
                raise ValueError(f"No image files found in directory: {folder_path}")
            
            # Use seed for reproducible random selection
            random.seed(seed)
            selected_image = random.choice(image_files)
            
            print(f"[Random Image Picker] Mode: Folder")
            print(f"[Random Image Picker] Folder: {folder_path}")
            print(f"[Random Image Picker] Selected: {selected_image}")
            
            img_tensor, width, height = self.load_image_file(selected_image)
            print(f"[Random Image Picker] Resolution: {width}x{height}")
            
            # Save for preview and return with image tensor
            preview = self.save_images(img_tensor, filename_prefix="RandomPicker")
            return {"ui": preview["ui"], "result": (img_tensor,)}
        else:
            # Single file mode: use file picker (image_data)
            if not image_data:
                raise ValueError(
                    "Single file mode is enabled but no image selected.\n\n"
                    "Please use the 📁 Choose File button to select an image."
                )
            
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
                
                print(f"[Random Image Picker] Mode: Single (File Picker)")
                print(f"[Random Image Picker] Resolution: {width}x{height}")
                
                # Save for preview and return with image tensor
                preview = self.save_images(img_tensor, filename_prefix="RandomPicker")
                return {"ui": preview["ui"], "result": (img_tensor,)}
                
            except Exception as e:
                raise ValueError(f"Failed to load image from file picker: {str(e)}")


# Node registration
NODE_CLASS_MAPPINGS = {
    "RandomImagePicker": RandomImagePicker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomImagePicker": "Random Image Picker"
}
