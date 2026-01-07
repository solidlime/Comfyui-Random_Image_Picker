# Code Style and Conventions

## Naming Conventions
- **Classes**: PascalCase (例: `RandomImagePicker`)
- **Functions/Methods**: snake_case (例: `load_image`, `get_image_files`)
- **Constants**: UPPER_SNAKE_CASE (例: `NODE_CLASS_MAPPINGS`)
- **Private methods**: アンダースコアなし（staticmethodを活用）

## Type Hints
- **使用**: 全ての関数/メソッドパラメータと戻り値に型ヒントを使用
- **例**: `def load_image_file(image_path: str) -> Tuple[torch.Tensor, int, int]:`

## Docstrings
- **スタイル**: Google style docstrings
- **必須箇所**: 
  - すべてのクラス
  - すべてのpublicメソッド/関数
  - staticmethod
- **内容**: 
  - 簡潔な説明
  - Args: 引数の説明
  - Returns: 戻り値の説明

## Import Order
1. 標準ライブラリ
2. サードパーティライブラリ
3. ComfyUI関連
4. ローカルモジュール

## ComfyUI Specific
- **INPUT_TYPES**: classmethodで定義、辞書形式で入力パラメータを定義
- **RETURN_TYPES**: タプル形式で出力型を定義
- **RETURN_NAMES**: タプル形式で出力名を定義
- **FUNCTION**: 実行される関数名を文字列で指定
- **CATEGORY**: ノードのカテゴリを文字列で指定
