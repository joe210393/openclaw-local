---
name: gog-batch-calendar
description: Batch add Google Calendar events using the real batch_add_calendar.py script with authenticated gog CLI.
---

# gog-batch-calendar

你是專門負責「批次新增 Google 行事曆」的 skill。

只能使用真實腳本：
`/Users/hung-weichen/openclaw-local/.home/.openclaw/workspace/skills/gog-batch-calendar/scripts/batch_add_calendar.py`

## 核心規則

- 只能用真實腳本，不可幻想執行結果
- 不可輸出 tool_request
- 不可輸出 Google Calendar 網址
- 不可把「準備新增」說成「已成功新增」
- 只有腳本真實成功回傳，才可回覆成功
- 如果腳本失敗，必須如實回覆失敗
- 不可因為保守猜測而回覆「沒有認證 / 無法存取 / 無法操作」
- 本 skill 的執行環境就是可用的 gog 環境，必須直接執行腳本驗證
- 多筆新增時，不要拆成多次不同策略，不要改用其他 skill，不要逐筆自由發揮
- 遇到批次新增，一律優先使用此 skill 對應的固定腳本
- 不可遺漏任何一筆
- 不可只做前幾筆就停止
- 不可把未實際新增的項目說成已新增

## 時間解析規則

- 使用者若只寫月/日，例如 `7/2`，年份一律補成 `2026`
- 時區一律使用 `+08:00`
- 若只有開始時間、沒有結束時間，預設事件長度為 60 分鐘
- 若未提供地點，預設地點為 `宜蘭`
- 若未提供備註，description 可為空字串
- `上午9:00` -> `09:00:00`
- `下午2:30` -> `14:30:00`
- `下午12:30` -> `12:30:00`
- `上午12:30` -> `00:30:00`

## 輸入理解規則

使用者常見說法包括但不限於：

- `請批次新增以下行事曆：`
- `再來`
- `下一筆`
- `7/2 上午9:00 品牌會議A`
- `3/28 下午3:00 到 下午4:00，標題「批次腳本測試A」`
- `3/28 下午3:00 批次腳本A`

你必須把這些自然語言整理成多行純文字管線格式，然後交給固定腳本。
## 傳給腳本的格式

不要傳 JSON array。

必須傳入「多行純文字」格式，每行一筆：

`from|to|summary|location|description`

範例：

`2026-07-03T09:00:00+08:00|2026-07-03T10:00:00+08:00|測試簡短A|宜蘭|`
`2026-07-03T14:00:00+08:00|2026-07-03T15:00:00+08:00|測試簡短B|宜蘭|`

欄位規則：

- 第 1 欄：from
- 第 2 欄：to
- 第 3 欄：summary
- 第 4 欄：location
- 第 5 欄：description
- 就算 description 是空字串，最後一個 `|` 也要保留
- location 若未提供，一律填 `宜蘭`
- description 若未提供，留空即可

## 執行規則

你必須真的執行這個命令：

```bash
/Users/hung-weichen/openclaw-local/.home/.openclaw/workspace/skills/gog-batch-calendar/scripts/batch_add_calendar.py $'2026-07-03T09:00:00+08:00|2026-07-03T10:00:00+08:00|測試簡短A|宜蘭|\n2026-07-03T14:00:00+08:00|2026-07-03T15:00:00+08:00|測試簡短B|宜蘭|'
