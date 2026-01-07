# Project Purpose

**Project Name**: Comfyui-Random_Image_Picker

## Overview
ComfyUIカスタムノード - ランダム画像選択機能

## Core Features
1. **単一画像ロード**: 指定された画像ファイルを読み込み
2. **フォルダランダムロード**: フォルダ内からランダムに画像を選択
3. **モード切り替え**: ボタンで単一/フォルダモードを切り替え
4. **サブフォルダスキャン**: オプションでサブフォルダも検索対象に
5. **解像度情報出力**: 画像と共にwidth, heightを出力

## Output
- IMAGE: ComfyUI形式の画像テンソル
- width: 画像の幅（整数）
- height: 画像の高さ（整数）

## Target System
- ComfyUI custom node
- Python-based implementation
