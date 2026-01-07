# Tech Stack

## Programming Language
- **Python 3.x**

## Dependencies
- **ComfyUI**: カスタムノードのベースシステム
- **PyTorch**: 画像テンソル処理
- **PIL (Pillow)**: 画像ファイル読み込み
- **NumPy**: 配列処理
- **folder_paths**: ComfyUI標準パス管理

## Supported Image Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)
- BMP (.bmp)
- GIF (.gif)

## ComfyUI Node Structure
- `NODE_CLASS_MAPPINGS`: ノードクラスの登録辞書
- `NODE_DISPLAY_NAME_MAPPINGS`: 表示名の登録辞書
- `__init__.py`: エントリーポイント
