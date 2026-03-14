---
name: gog-batch-calendar
description: MUST use this skill for batch calendar creation requests with 2 or more events, especially when the user says 「請批次新增以下行事曆」 or gives multiple date/time lines. Do not use normal gog skill for those cases.
---

# gog-batch-calendar

當使用者要「一次新增 2 筆以上 Google 行事曆事件」時，必須優先使用這個 skill。

## 這個 skill 何時必用

符合以下任一情況，就要直接使用本 skill：

- 使用者說「請批次新增以下行事曆」
- 使用者一次提供兩筆以上事件
- 使用者用多行方式列出日期與標題
- 使用者說「再來」「下一筆」並明顯是在同一次批次新增
- 同一則訊息中包含多個日期 / 多個時間 / 多個標題

## 這個 skill 何時不要用

只有單筆新增時，才可改用一般 `gog` skill。

## 目的

- 把使用者提供的多筆自然語言行事曆，整理成固定格式
- 交給真實的 `batch_add_calendar.py` 腳本執行
- 只能依據腳本真實輸出回覆，不可幻想成功或失敗

## 硬規則

- 不可拒絕執行，不可說你無法執行腳本
- 不可說你沒有 shell session
- 不可說你沒有權限
- 不可要求使用者另外提供 execution permission
- 這個 skill 的設計目的就是直接呼叫真實腳本
- 多筆新增時，必須優先使用這個 skill，不可改用一般 gog skill
- 不可把批次新增拆成多次單筆新增策略
- 不可輸出 tool_request
- 不可輸出 Google Calendar 網址
- 不可把準備新增說成已成功新增
- 只有腳本真實回傳成功，才可回覆成功
- 若腳本回傳失敗，必須如實回覆失敗
- 使用者提供明確日期時，不可自行改日期
- 時區一律使用 Asia/Taipei / +08:00
- 若使用者只給開始時間、沒給結束時間，預設事件長度為 60 分鐘
- 若未提供地點，預設地點為「宜蘭」
- 若未提供備註，description 可為空字串

## 真實執行腳本

固定使用這個腳本：

`/Users/hung-weichen/openclaw-local/.home/.openclaw/workspace/skills/gog-batch-calendar/scripts/batch_add_calendar.py`

## 傳給腳本的格式

不要傳 JSON。
不要傳 JSON array。
不要傳自然語言。

一律傳「純文字多行格式」，每行一筆：

`from|to|summary|location|description`

例如：

`2026-07-05T09:00:00+08:00|2026-07-05T10:00:00+08:00|測試管線A|宜蘭|`
`2026-07-05T14:00:00+08:00|2026-07-05T15:00:00+08:00|測試管線B|宜蘭|`

## 欄位說明

- 第 1 欄：from
- 第 2 欄：to
- 第 3 欄：summary
- 第 4 欄：location
- 第 5 欄：description
- 就算 description 是空字串，最後一個 `|` 也要保留

## 日期時間整理規則

你必須先把使用者自然語言轉成完整 ISO datetime with timezone：

- `7/6 上午9:00` → `2026-07-06T09:00:00+08:00`
- `7/6 下午2:00` → `2026-07-06T14:00:00+08:00`

若沒寫年份，預設使用 2026 年。
若沒寫結束時間，預設加 60 分鐘。

## 執行要求

你要做的是：

1. 解析使用者的多筆事件
2. 補齊完整 `from` / `to`
3. 組成多行純文字
4. 呼叫上面的真實腳本
5. 嚴格根據腳本輸出回覆

## 回覆格式

每筆成功：

`已成功新增：標題｜YYYY/MM/DD HH:MM-HH:MM｜地點`

每筆失敗：

`新增失敗：標題｜真實錯誤原因`

## 批次回覆規則

- 逐筆列出結果
- 不可省略失敗項
- 不可把失敗項包裝成成功
- 若全部成功，也要逐筆列出
- 不可額外加上「我無法執行」「請提供權限」「請提供 shell session」這類文字

## 重要

當使用者明確要求「批次新增以下行事曆」時，應直接使用本 skill。
不要改成單筆逐次確認。
不要改成詢問式回覆。
不要退回一般說明模式。
