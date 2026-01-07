# Random Image Picker - ComfyUI Custom Node

A ComfyUI custom node that provides flexible image loading with support for both single file and random folder selection.

## Features

- **Single Image Mode**: Load a specific image file
- **Folder Mode**: Randomly select an image from a folder
- **Subfolder Support**: Option to include subfolders in the search
- **Resolution Output**: Automatically outputs image width and height
- **Reproducible Random**: Seed control for consistent random selection
- **🆕 Image Preview**: Real-time preview of loaded images in the UI
- **🆕 File Browser**: Convenient "Browse..." button for file/folder selection

## Installation

1. Clone or download this repository to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes
   git clone <repository-url> Comfyui-Random_Image_Picker
   ```

2. Restart ComfyUI

3. The node will appear in the "image" category as "Random Image Picker"

## Usage Tips

- **Using the Browse Button**: Click "Browse..." to open your system's file/folder selector
  - Note: Due to browser security limitations, you may need to manually enter the full path
- **Default Path**: The input field defaults to your ComfyUI input directory
- **Path Format**: Use forward slashes `/` or double backslashes `\\` on Windows
- **Preview**: The loaded image automatically appears in the node's preview area

## Usage

### Node Inputs

- **path** (STRING): 
  - In Single mode: Full path to an image file
  - In Folder mode: Full path to a folder containing images
  - 🆕 **Browse Button**: Click "Browse..." to select files/folders using your file explorer
  - Default: ComfyUI input directory

- **folder_mode** (BOOLEAN):
  - `OFF` (Single): Load the specified image file
  - `ON` (Folder): Randomly select an image from the folder
  - Note: The browse dialog changes based on this setting

- **include_subfolders** (BOOLEAN):
  - `OFF`: Only scan the specified folder
  - `ON`: Include all subfolders in the search

- **seed** (INT): 
  - Random seed for reproducible image selection in Folder mode
  - Range: 0 to 18446744073709551615

### Node Outputs

- **IMAGE**: The loaded image in ComfyUI tensor format (with real-time preview)
- **width** (INT): Image width in pixels
- **height** (INT): Image height in pixels

### Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)
- BMP (.bmp)
- GIF (.gif)

## Examples

### Single Image Mode
```
path: D:/images/photo.png
folder_mode: OFF
include_subfolders: OFF
seed: 0
```
Loads the specific image at `D:/images/photo.png`

### Random Folder Mode
```
path: D:/images/
folder_mode: ON
include_subfolders: OFF
seed: 42
```
Randomly selects one image from `D:/images/` (excluding subfolders)

### Random with Subfolders
```
path: D:/images/
folder_mode: ON
include_subfolders: ON
seed: 42
```
Randomly selects one image from `D:/images/` and all its subfolders

## Technical Details

- Images are converted to RGB format
- Output tensor format: `[batch, height, width, channels]`
- Pixel values normalized to 0.0-1.0 range
- Uses PyTorch tensors for ComfyUI compatibility
- Real-time preview in ComfyUI UI (OUTPUT_NODE enabled)
- Custom JavaScript widget for enhanced file selection

## License

MIT License

## Author

Created for ComfyUI
