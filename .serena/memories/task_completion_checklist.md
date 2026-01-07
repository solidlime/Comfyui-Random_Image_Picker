# Task Completion Checklist

## タスク完了時の必須作業

### 1. コード品質チェック
- [ ] 構文エラーがないことを確認
- [ ] 型ヒントが正しく付与されているか
- [ ] Docstringsが適切に書かれているか

### 2. ComfyUI互換性
- [ ] `INPUT_TYPES`が正しく定義されているか
- [ ] `RETURN_TYPES`と`RETURN_NAMES`が一致しているか
- [ ] ノードの登録（`NODE_CLASS_MAPPINGS`）が正しいか

### 3. ドキュメント
- [ ] README.mdが最新の情報か
- [ ] 使用方法が明確に記載されているか
- [ ] 公開情報に個人情報が含まれていないか

### 4. Git管理
- [ ] 変更をコミット: `git add . && git commit -m "descriptive message"`
- [ ] 適切なタイミングでプッシュ: `git push`

### 5. テスト
- [ ] ComfyUIでノードが正しく読み込まれるか
- [ ] 単一画像モードが動作するか
- [ ] フォルダモードが動作するか
- [ ] サブフォルダスキャンが動作するか
- [ ] 出力（IMAGE, width, height）が正しいか

## 区切りのいいタイミング
- 機能追加完了時
- バグ修正完了時
- リファクタリング完了時
