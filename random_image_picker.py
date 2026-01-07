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
                "path": ("STRING", {
                    "default": default_path, 
                    "multiline": False,
                    "placeholder": "Path to image file or folder"
                }),
                "folder_mode": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "Folder", 
                    "label_off": "Single"
                }),
                "include_subfolders": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "ON", 
                    "label_off": "OFF"
                }),
                "seed": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff
                }),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("IMAGE", "width", "height")
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
    
    def load_image(self, path: str, folder_mode: bool, include_subfolders: bool, seed: int):
        """
        Load image based on mode settings.
        
        Args:
            path: File or folder path
            folder_mode: True for folder mode, False for single file mode
            include_subfolders: Whether to scan subfolders
            seed: Random seed for folder mode
            
        Returns:
            Tuple of (image_tensor, width, height)
        """
        if not path or not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
        
        if folder_mode:
            # Folder mode: pick random image
            if not os.path.isdir(path):
                raise ValueError(f"Folder mode enabled but path is not a directory: {path}")
            
            image_files = self.get_image_files(path, include_subfolders)
            
            if not image_files:
                raise ValueError(f"No image files found in directory: {path}")
            
            # Use seed for reproducible random selection
            random.seed(seed)
            selected_image = random.choice(image_files)
            
            print(f"[Random Image Picker] Selected: {selected_image}")
            return self.load_image_file(selected_image)
        else:
            # Single file mode
            if not os.path.isfile(path):
                raise ValueError(f"Single file mode enabled but path is not a file: {path}")
            
            return self.load_image_file(path)


# Node registration
NODE_CLASS_MAPPINGS = {
    "RandomImagePicker": RandomImagePicker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomImagePicker": "Random Image Picker"
}
