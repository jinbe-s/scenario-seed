#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4: GM向け詳細分析
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
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
print("Phase 4: GM向け詳細分析")
print("=" * 60)

# GM回答者のフィルタリング
df_gm = df[df['GM回答有無'] == 'ゲームマスター経験者向けの質問に回答する'].copy()
print(f"\nGM回答者数: {len(df_gm)}件 / 全体: {len(df)}件 ({len(df_gm)/len(df)*100:.1f}%)")

# GM回答者かつ引用可能
df_gm_quotable = df_gm[df_gm['引用'] == 'はい'].copy()
print(f"引用可能なGM回答者数: {len(df_gm_quotable)}件")

# ===== 3.4.1 GM回答者の属性 =====
print("\n" + "-" * 40)
print("3.4.1 GM回答者の属性")
print("-" * 40)

# 経験年数分布
gm_exp = df_gm['経験年数'].value_counts()
print("\nGM回答者の経験年数分布:")
print(gm_exp)
gm_exp.to_csv(os.path.join(OUTPUT_TABLES, '21_GM回答者_経験年数.csv'), encoding='utf-8-sig')

# ===== 3.4.2 GM時間配分の手法分析 =====
print("\n" + "-" * 40)
print("3.4.2 GM時間配分の手法分析")
print("-" * 40)

time_alloc = df_gm['GM_時間配分'].dropna().astype(str)
all_alloc = ' '.join(time_alloc)

alloc_categories = {
    '事前準備型': ['テストプレイ', 'テスプレ', '読み込み', '予習', '準備'],
    '目安時間設定型': ['シーン', '時間', '目安', '区切り', '配分', '設定'],
    '経験則型': ['経験', '過去', '傾向', 'いつも', '感覚'],
    '柔軟対応型': ['予備', '余裕', '調整', 'PL', '様子'],
    '計算型': ['計算', '見積', '想定', 'ページ', '進捗'],
}

alloc_cat_counts = {}
for category, keywords in alloc_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_alloc, re.IGNORECASE))
    alloc_cat_counts[category] = count

alloc_df = pd.DataFrame(list(alloc_cat_counts.items()), columns=['手法カテゴリ', '出現回数'])
alloc_df = alloc_df.sort_values('出現回数', ascending=False)
print("\nGM時間配分の手法:")
print(alloc_df)
alloc_df.to_csv(os.path.join(OUTPUT_TABLES, '22_GM時間配分_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# ===== 3.4.3 GM時間意識の工夫分析 =====
print("\n" + "-" * 40)
print("3.4.3 GM時間意識の工夫分析")
print("-" * 40)

effort = df_gm['GM_時間意識工夫'].dropna().astype(str)
all_effort = ' '.join(effort)

effort_categories = {
    '可視化': ['時計', 'タイマー', '表示', '確認', '見る'],
    'コミュニケーション': ['伝える', '共有', '声かけ', 'PL', 'まとめ'],
    '環境整備': ['情報タブ', 'ツール', '整理', 'チャットパレット', '準備'],
    'シーン管理': ['シーン', '区切り', '進捗', 'ページ'],
    '簡略化': ['簡略', '省略', 'セリフ', '演出'],
}

effort_cat_counts = {}
for category, keywords in effort_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_effort, re.IGNORECASE))
    effort_cat_counts[category] = count

effort_df = pd.DataFrame(list(effort_cat_counts.items()), columns=['工夫カテゴリ', '出現回数'])
effort_df = effort_df.sort_values('出現回数', ascending=False)
print("\nGM時間意識の工夫:")
print(effort_df)
effort_df.to_csv(os.path.join(OUTPUT_TABLES, '23_GM時間意識工夫_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# ===== 3.4.4 GM時間超過対処法の分析 =====
print("\n" + "-" * 40)
print("3.4.4 GM時間超過対処法の分析")
print("-" * 40)

handling = df_gm['GM_時間超過対処'].dropna().astype(str)
all_handling = ' '.join(handling)

handling_categories = {
    '削減系': ['省略', 'カット', '簡略', '短縮', '削る'],
    '判定調整': ['判定', 'ダイス', 'ロール', '自動成功'],
    'RP調整': ['RP', 'ロールプレイ', '会話', 'セリフ'],
    'シーン調整': ['シーン', '描写', '情報', 'NPC'],
    '延長系': ['追加日程', '予備', '延長', '次回'],
    'PL協力依頼': ['お願い', '伝える', '相談', 'PL', '協力'],
}

handling_cat_counts = {}
for category, keywords in handling_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_handling, re.IGNORECASE))
    handling_cat_counts[category] = count

handling_df = pd.DataFrame(list(handling_cat_counts.items()), columns=['対処法カテゴリ', '出現回数'])
handling_df = handling_df.sort_values('出現回数', ascending=False)
print("\nGM時間超過対処法:")
print(handling_df)
handling_df.to_csv(os.path.join(OUTPUT_TABLES, '24_GM時間超過対処_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# ===== 3.4.5 時間管理と満足度のバランス =====
print("\n" + "-" * 40)
print("3.4.5 時間管理と満足度のバランス")
print("-" * 40)

balance = df_gm['GM_時間管理と満足度'].dropna().astype(str)
all_balance = ' '.join(balance)

balance_categories = {
    '時間優先': ['時間を守る', '時間厳守', '時間が大事', '時間優先', '守ること'],
    '満足度優先': ['満足度', '楽しさ', '楽しい', '満足', 'やりたい'],
    'バランス重視': ['バランス', '両立', '両方', '半々', '5:5'],
    'メンバー次第': ['メンバー', 'PL', '相手', '状況', '場合'],
    '予備日確保': ['予備', '余裕', '追加', '日程'],
}

balance_cat_counts = {}
for category, keywords in balance_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_balance, re.IGNORECASE))
    balance_cat_counts[category] = count

balance_df = pd.DataFrame(list(balance_cat_counts.items()), columns=['スタンス', '出現回数'])
balance_df = balance_df.sort_values('出現回数', ascending=False)
print("\n時間管理と満足度のバランス:")
print(balance_df)
balance_df.to_csv(os.path.join(OUTPUT_TABLES, '25_時間管理と満足度_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# ===== 3.4.6 GMのコツまとめ =====
print("\n" + "-" * 40)
print("3.4.6 GMのコツまとめ")
print("-" * 40)

tips = df_gm['GM_コツ'].dropna().astype(str)
all_tips = ' '.join(tips)

tips_categories = {
    '事前準備': ['準備', 'テストプレイ', '読み込み', '予習', 'シナリオ'],
    '時間確認': ['時計', 'タイマー', '確認', '見る'],
    'PL協力': ['PL', '協力', 'お願い', '伝える', '共有'],
    'シーン管理': ['シーン', '区切り', 'キリ', '進捗'],
    '簡略化': ['省略', '簡略', 'カット', '削る'],
    '予備日確保': ['予備', '余裕', '日程', '多め'],
    'ぶっちゃけ': ['ぶっちゃけ', '正直', '素直', '伝える'],
}

tips_cat_counts = {}
for category, keywords in tips_categories.items():
    count = 0
    for kw in keywords:
        count += len(re.findall(kw, all_tips, re.IGNORECASE))
    tips_cat_counts[category] = count

tips_df = pd.DataFrame(list(tips_cat_counts.items()), columns=['コツカテゴリ', '出現回数'])
tips_df = tips_df.sort_values('出現回数', ascending=False)
print("\nGMのコツ:")
print(tips_df)
tips_df.to_csv(os.path.join(OUTPUT_TABLES, '26_GMコツ_カテゴリ別.csv'), encoding='utf-8-sig', index=False)

# ===== グラフ作成 =====
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 時間配分
colors = plt.cm.Set2(range(len(alloc_df)))
axes[0, 0].barh(range(len(alloc_df)), alloc_df['出現回数'], color=colors)
axes[0, 0].set_yticks(range(len(alloc_df)))
axes[0, 0].set_yticklabels(alloc_df['手法カテゴリ'])
axes[0, 0].set_title('GM時間配分の手法', fontsize=11, fontweight='bold')
axes[0, 0].invert_yaxis()

# 時間意識工夫
axes[0, 1].barh(range(len(effort_df)), effort_df['出現回数'], color=plt.cm.Pastel1(range(len(effort_df))))
axes[0, 1].set_yticks(range(len(effort_df)))
axes[0, 1].set_yticklabels(effort_df['工夫カテゴリ'])
axes[0, 1].set_title('GM時間意識の工夫', fontsize=11, fontweight='bold')
axes[0, 1].invert_yaxis()

# 時間超過対処
axes[0, 2].barh(range(len(handling_df)), handling_df['出現回数'], color=plt.cm.Set3(range(len(handling_df))))
axes[0, 2].set_yticks(range(len(handling_df)))
axes[0, 2].set_yticklabels(handling_df['対処法カテゴリ'])
axes[0, 2].set_title('GM時間超過対処法', fontsize=11, fontweight='bold')
axes[0, 2].invert_yaxis()

# 時間と満足度
axes[1, 0].barh(range(len(balance_df)), balance_df['出現回数'], color=plt.cm.Accent(range(len(balance_df))))
axes[1, 0].set_yticks(range(len(balance_df)))
axes[1, 0].set_yticklabels(balance_df['スタンス'])
axes[1, 0].set_title('時間管理と満足度のバランス', fontsize=11, fontweight='bold')
axes[1, 0].invert_yaxis()

# GMのコツ
axes[1, 1].barh(range(len(tips_df)), tips_df['出現回数'], color=plt.cm.Paired(range(len(tips_df))))
axes[1, 1].set_yticks(range(len(tips_df)))
axes[1, 1].set_yticklabels(tips_df['コツカテゴリ'])
axes[1, 1].set_title('GMのコツ', fontsize=11, fontweight='bold')
axes[1, 1].invert_yaxis()

# GM経験年数
gm_exp_sorted = gm_exp.sort_index()
axes[1, 2].bar(range(len(gm_exp_sorted)), gm_exp_sorted.values, color=['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
axes[1, 2].set_xticks(range(len(gm_exp_sorted)))
axes[1, 2].set_xticklabels(gm_exp_sorted.index, rotation=45)
axes[1, 2].set_title('GM回答者の経験年数', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '18_GM詳細分析まとめ.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 引用集の作成 =====
print("\n引用集を作成中...")

# GMのコツ引用集
quotable_tips = df_gm_quotable['GM_コツ'].dropna()
sample_tips = quotable_tips[quotable_tips.str.len() > 15].head(40).tolist()

with open(os.path.join(OUTPUT_TEXT, '03_引用例_GMコツ.md'), 'w', encoding='utf-8') as f:
    f.write("# GMの時間管理コツ - 引用例\n\n")
    f.write("※引用許可のあった回答より抜粋\n\n")
    for i, tip in enumerate(sample_tips, 1):
        f.write(f"{i}. {tip}\n\n")

# GM時間配分引用集
quotable_alloc = df_gm_quotable['GM_時間配分'].dropna()
sample_alloc = quotable_alloc[quotable_alloc.str.len() > 15].head(30).tolist()

with open(os.path.join(OUTPUT_TEXT, '04_引用例_GM時間配分.md'), 'w', encoding='utf-8') as f:
    f.write("# GM時間配分の手法 - 引用例\n\n")
    f.write("※引用許可のあった回答より抜粋\n\n")
    for i, alloc in enumerate(sample_alloc, 1):
        f.write(f"{i}. {alloc}\n\n")

# GM時間超過対処引用集
quotable_handling = df_gm_quotable['GM_時間超過対処'].dropna()
sample_handling = quotable_handling[quotable_handling.str.len() > 10].head(30).tolist()

with open(os.path.join(OUTPUT_TEXT, '05_引用例_GM時間超過対処.md'), 'w', encoding='utf-8') as f:
    f.write("# GM時間超過時の対処法 - 引用例\n\n")
    f.write("※引用許可のあった回答より抜粋\n\n")
    for i, h in enumerate(sample_handling, 1):
        f.write(f"{i}. {h}\n\n")

print(f"引用例を {OUTPUT_TEXT} に保存しました")

print("\n" + "=" * 60)
print("Phase 4: GM向け詳細分析完了")
print("=" * 60)
