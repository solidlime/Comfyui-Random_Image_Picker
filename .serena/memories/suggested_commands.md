# Suggested Commands

## Windows System Commands
- `ls` または `dir`: ディレクトリ内容の表示
- `cd <path>`: ディレクトリ移動
- `Get-Content <file>`: ファイル内容の表示
- `Select-String -Path <file> -Pattern <pattern>`: ファイル内検索

## Git Commands
- `git status`: 変更状況の確認
- `git add .`: 変更をステージング
- `git commit -m "message"`: コミット
- `git push`: リモートへプッシュ

## Python Development
- `python -m py_compile <file>`: Pythonファイルの構文チェック
- `python <file>`: Pythonスクリプトの実行

## ComfyUI Testing
- ComfyUIを起動してカスタムノードをテスト
- カスタムノードは `custom_nodes/Comfyui-Random_Image_Picker/` に配置

## Code Quality (推奨)
- **Black**: `python -m black <file>` - コードフォーマット
- **Flake8**: `python -m flake8 <file>` - リンティング
- **MyPy**: `python -m mypy <file>` - 型チェック

Note: これらのツールは必要に応じてインストール
