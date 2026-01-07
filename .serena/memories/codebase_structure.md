# Codebase Structure

## Directory Layout
```
Comfyui-Random_Image_Picker/
├── .github/
│   └── copilot-instructions.md  # AI assistant instructions
├── .serena/                      # Serena project config
├── __init__.py                   # Package entry point
└── random_image_picker.py        # Main node implementation
```

## File Descriptions

### `__init__.py`
- パッケージのエントリーポイント
- `NODE_CLASS_MAPPINGS`と`NODE_DISPLAY_NAME_MAPPINGS`をインポートしてエクスポート
- ComfyUIがカスタムノードを認識するために必要

### `random_image_picker.py`
- メインの実装ファイル
- `RandomImagePicker`クラス: ノードの本体
  - `INPUT_TYPES()`: 入力パラメータの定義
  - `get_image_files()`: 画像ファイルのリスト取得
  - `load_image_file()`: 画像ファイルの読み込みとテンソル変換
  - `load_image()`: メイン処理（モードに応じた画像読み込み）
- ノード登録用の定数

## Future Extensions
- 追加の画像処理機能
- フィルタリングオプション
- プレビュー機能
