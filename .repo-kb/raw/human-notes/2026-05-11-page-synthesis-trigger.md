---
type: raw-source
kind: human-note
id: 2026-05-11-page-synthesis-trigger
date: 2026-05-11
source_ref: user-feedback
---

# Why pages were not created after ingest, and how to prevent it

## Original or Sanitized Note

実際に利用していると以下の改善点があった。

> なんで page 化されてなかったんだろう？どのコマンド実行時にやられる想定だったのか。

回答として整理した内容：

- 設計上、`ingest-directory` も `compile` も自動では `pages/` を生成しない。
- `ingest-directory` は raw 層への取り込み専用。
- `compile` は `status: active` の pages / review-aspects を集約するだけ。
- pages を起こすのは「raw 取り込み後に LLM が durable signal を判断して手動で synthesize する」ステップ（`references/operations.md` の Ingest 手順 4「Update existing pages before creating new pages when the note contains durable signal」）。
- 直近の ingest セッションではこの手順が未実行のまま完了扱いになっていた。

## Extracted Claims

1. **Intentional separation**: 自動化すると低シグナルな page が量産されるため、synthesize は LLM 判断の手動ステップとして残されている。`ingest` / `ingest-directory` / `compile` のいずれも pages を自動生成しない、というのが意図された設計。
2. **直近の失敗パターン**: symlink パターンで `docs/` を取り込んだ際、`pages/references/<topic>-index.md` を作って index を張った時点でセッションが完了扱いになり、cross-cutting な `pages/conventions/...` への昇華まで進まなかった。Ingest はゴールではなく中間状態。
3. **再発防止のチェックリスト**: ingest 完了時に「同じテーマが 3 つ以上の raw note / 取り込み対象に出てきているか」を確認し、該当する場合は既存 page の更新もしくは新規 page 作成を行う。このトリガを `references/operations.md` の Ingest 手順に明文化する。
