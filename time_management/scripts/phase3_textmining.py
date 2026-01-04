#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3: テキストマイニング - 自由記述の分析
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')
import os

plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Meiryo', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# パス設定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'データ.csv')
OUTPUT_GRAPHS = os.path.join(BASE_DIR, 'output', 'graphs')
OUTPUT_TABLES = os.path.join(BASE_DIR, 'output', 'tables')
OUTPUT_TEXT = os.path.join(BASE_DIR, 'output', 'text')

df = pd.read_csv(DATA_PATH, encoding='utf-8')
print("=" * 60)
print("Phase 3: テキストマイニング")
print("=" * 60)

# 引用可能な回答のみ抽出
df_quotable = df[df['引用'] == 'はい'].copy()
print(f"\n引用可能な回答数: {len(df_quotable)}件 / 全体: {len(df)}件")

# ===== 3.3.1 時間意識の理由分析 =====
print("\n" + "-" * 40)
print("3.3.1 時間意識の理由分析")
print("-" * 40)

# キーワード辞書（カテゴリ別）
reason_categories = {
    '健康・生活': ['睡眠', '体調', '健康', '疲労', '疲れ', '眠', '寝', '生活', '体力'],
    '仕事・学業': ['仕事', '翌日', '明日', '出勤', '学校', '予定', '社会人'],
    '物理的制約': ['会場', '終電', '帰宅', '閉館', '場所'],
    'マナー・配慮': ['約束', '迷惑', '配慮', '守る', '相手', '他の', '参加者'],
    'セッション品質': ['集中', '満足', '楽しさ', '楽しい', 'ダレ', 'だれ', '長すぎ'],
    '時間管理意識': ['時間', 'GM', 'KP', 'ゲームマスター', '管理', '意識'],
}

# 全テキストの結合
reasons = df['時間意識_理由'].dropna().astype(str)
all_text = ' '.join(reasons)

# カテゴリ別集計
category_counts = {}
for category, keywords in reason_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_text, re.IGNORECASE))
    category_counts[category] = count

category_df = pd.DataFrame(list(category_counts.items()), columns=['カテゴリ', '出現回数'])
category_df = category_df.sort_values('出現回数', ascending=False)
print("\n時間意識の理由 - カテゴリ別出現回数:")
print(category_df)
category_df.to_csv(os.path.join(OUTPUT_TABLES, '17_時間意識理由_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# 詳細キーワード抽出
detailed_keywords = ['睡眠', '仕事', '翌日', '時間', '体調', '健康', '終電', '会場',
                     '約束', '迷惑', '配慮', '集中', '疲労', '生活', 'GM', 'PL',
                     '予定', '眠', '寝る', '社会人', '明日', '管理']
keyword_counts = {}
for kw in detailed_keywords:
    count = len(re.findall(kw, all_text, re.IGNORECASE))
    if count > 0:
        keyword_counts[kw] = count

keyword_df = pd.DataFrame(list(keyword_counts.items()), columns=['キーワード', '出現回数'])
keyword_df = keyword_df.sort_values('出現回数', ascending=False)
print("\n時間意識の理由 - 頻出キーワード:")
print(keyword_df.head(15))
keyword_df.to_csv(os.path.join(OUTPUT_TABLES, '18_時間意識理由_キーワード.csv'), encoding='utf-8-sig', index=False)

# グラフ作成
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# カテゴリ別
colors1 = plt.cm.Set2(range(len(category_df)))
ax1.barh(range(len(category_df)), category_df['出現回数'], color=colors1)
ax1.set_yticks(range(len(category_df)))
ax1.set_yticklabels(category_df['カテゴリ'])
ax1.set_title('時間意識の理由 - カテゴリ別', fontsize=12, fontweight='bold')
ax1.set_xlabel('出現回数')
ax1.invert_yaxis()

# キーワード別（上位10件）
top_kw = keyword_df.head(10)
colors2 = plt.cm.Pastel1(range(len(top_kw)))
ax2.barh(range(len(top_kw)), top_kw['出現回数'], color=colors2)
ax2.set_yticks(range(len(top_kw)))
ax2.set_yticklabels(top_kw['キーワード'])
ax2.set_title('時間意識の理由 - 頻出キーワードTOP10', fontsize=12, fontweight='bold')
ax2.set_xlabel('出現回数')
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '16_時間意識理由_分析.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 3.3.2 時間超過原因の分析 =====
print("\n" + "-" * 40)
print("3.3.2 時間超過原因の分析")
print("-" * 40)

# カテゴリ辞書
cause_categories = {
    'RP要因': ['RP', 'ロールプレイ', '盛り上が', 'ロープレ', '会話', 'キャラ'],
    '戦闘要因': ['戦闘', 'ダイス', '出目', 'バトル', '判定'],
    '相談要因': ['相談', '会議', 'PL', '話し合', '打ち合わせ'],
    '探索・推理要因': ['探索', '謎解き', '情報', '推理', '調査'],
    'GM要因': ['描写', '進行', '準備', 'シナリオ', '想定'],
    '技術要因': ['タイピング', 'テキスト', '入力', 'ツール', 'システム'],
    '雑談要因': ['雑談', '脱線', '関係ない'],
}

causes = df['時間超過_原因'].dropna().astype(str)
all_causes = ' '.join(causes)

cause_cat_counts = {}
for category, keywords in cause_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_causes, re.IGNORECASE))
    cause_cat_counts[category] = count

cause_cat_df = pd.DataFrame(list(cause_cat_counts.items()), columns=['カテゴリ', '出現回数'])
cause_cat_df = cause_cat_df.sort_values('出現回数', ascending=False)
print("\n時間超過原因 - カテゴリ別出現回数:")
print(cause_cat_df)
cause_cat_df.to_csv(os.path.join(OUTPUT_TABLES, '19_時間超過原因_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# 詳細キーワード
cause_keywords = ['RP', 'ロールプレイ', '戦闘', 'ダイス', '相談', '会議',
                  '探索', '謎解き', '情報', 'シナリオ', 'テキスト',
                  'タイピング', '雑談', '想定', '盛り上が', '長引']
cause_kw_counts = {}
for kw in cause_keywords:
    count = len(re.findall(kw, all_causes, re.IGNORECASE))
    if count > 0:
        cause_kw_counts[kw] = count

cause_kw_df = pd.DataFrame(list(cause_kw_counts.items()), columns=['原因キーワード', '出現回数'])
cause_kw_df = cause_kw_df.sort_values('出現回数', ascending=False)
print("\n時間超過原因 - 頻出キーワード:")
print(cause_kw_df)
cause_kw_df.to_csv(os.path.join(OUTPUT_TABLES, '20_時間超過原因_キーワード.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

colors1 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
ax1.barh(range(len(cause_cat_df)), cause_cat_df['出現回数'], color=colors1[:len(cause_cat_df)])
ax1.set_yticks(range(len(cause_cat_df)))
ax1.set_yticklabels(cause_cat_df['カテゴリ'])
ax1.set_title('時間超過原因 - カテゴリ別', fontsize=12, fontweight='bold')
ax1.set_xlabel('出現回数')
ax1.invert_yaxis()

top_cause = cause_kw_df.head(10)
ax2.barh(range(len(top_cause)), top_cause['出現回数'], color=plt.cm.Set3(range(len(top_cause))))
ax2.set_yticks(range(len(top_cause)))
ax2.set_yticklabels(top_cause['原因キーワード'])
ax2.set_title('時間超過原因 - 頻出キーワードTOP10', fontsize=12, fontweight='bold')
ax2.set_xlabel('出現回数')
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '17_時間超過原因_分析.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 引用集の作成 =====
print("\n" + "-" * 40)
print("引用集の作成")
print("-" * 40)

# 時間意識の理由（引用可能な回答から代表例）
quotable_reasons = df_quotable['時間意識_理由'].dropna()
sample_reasons = quotable_reasons[quotable_reasons.str.len() > 20].head(30).tolist()

with open(os.path.join(OUTPUT_TEXT, '01_引用例_時間意識理由.md'), 'w', encoding='utf-8') as f:
    f.write("# 時間意識の理由 - 引用例\n\n")
    f.write("※引用許可のあった回答より抜粋\n\n")
    for i, reason in enumerate(sample_reasons, 1):
        f.write(f"{i}. {reason}\n\n")

# 時間超過原因
quotable_causes = df_quotable['時間超過_原因'].dropna()
sample_causes = quotable_causes[quotable_causes.str.len() > 10].head(30).tolist()

with open(os.path.join(OUTPUT_TEXT, '02_引用例_時間超過原因.md'), 'w', encoding='utf-8') as f:
    f.write("# 時間超過原因 - 引用例\n\n")
    f.write("※引用許可のあった回答より抜粋\n\n")
    for i, cause in enumerate(sample_causes, 1):
        f.write(f"{i}. {cause}\n\n")

print(f"引用例を {OUTPUT_TEXT} に保存しました")

print("\n" + "=" * 60)
print("Phase 3: テキストマイニング完了")
print("=" * 60)
