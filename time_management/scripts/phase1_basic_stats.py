#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1: 基礎集計 - 全体像の把握
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings('ignore')
from collections import Counter
import os

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Meiryo', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# パス設定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'データ.csv')
OUTPUT_GRAPHS = os.path.join(BASE_DIR, 'output', 'graphs')
OUTPUT_TABLES = os.path.join(BASE_DIR, 'output', 'tables')
OUTPUT_TEXT = os.path.join(BASE_DIR, 'output', 'text')

# ディレクトリ作成
for d in [OUTPUT_GRAPHS, OUTPUT_TABLES, OUTPUT_TEXT]:
    os.makedirs(d, exist_ok=True)

# データ読み込み
print("データを読み込んでいます...")
df = pd.read_csv(DATA_PATH, encoding='utf-8')
print(f"データ読み込み完了: {len(df)}行 x {len(df.columns)}列\n")

# ===== 3.1.1 回答者属性の集計 =====
print("=" * 60)
print("3.1.1 回答者属性の集計")
print("=" * 60)

# 1. 経験年数別
print("\n1. 経験年数別の回答数・割合")
exp_order = ['1年未満', '1〜3年', '4〜6年', '7年以上']
exp_counts = df['経験年数'].value_counts()
exp_counts = exp_counts.reindex([x for x in exp_order if x in exp_counts.index])
exp_pct = (exp_counts / len(df) * 100).round(1)
exp_df = pd.DataFrame({
    '回答数': exp_counts,
    '割合(%)': exp_pct
})
print(exp_df)
exp_df.to_csv(os.path.join(OUTPUT_TABLES, '01_経験年数別.csv'), encoding='utf-8-sig')

# グラフ作成
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
exp_counts.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('経験年数別の回答数', fontsize=14, fontweight='bold')
ax1.set_xlabel('経験年数')
ax1.set_ylabel('回答数')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(exp_counts):
    ax1.text(i, v + 5, str(v), ha='center', va='bottom')

ax2.pie(exp_counts, labels=exp_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
ax2.set_title('経験年数別の割合', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '01_経験年数別.png'), dpi=150, bbox_inches='tight')
plt.close()

# 2. 参加形態別
print("\n2. 参加形態別の回答数")
forms = []
for val in df['形態'].dropna():
    if isinstance(val, str):
        forms.extend([f.strip() for f in val.split(',')])

form_counts = Counter(forms)
form_df = pd.DataFrame({
    '形態': list(form_counts.keys()),
    '回答数': list(form_counts.values())
}).sort_values('回答数', ascending=False)
form_df['割合(%)'] = (form_df['回答数'] / len(df) * 100).round(1)
print(form_df)
form_df.to_csv(os.path.join(OUTPUT_TABLES, '02_参加形態別.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(12, 6))
form_df_sorted = form_df.sort_values('回答数')
colors = plt.cm.Set3(range(len(form_df_sorted)))
ax.barh(form_df_sorted['形態'], form_df_sorted['回答数'], color=colors)
ax.set_title('参加形態別の回答数（複数選択可）', fontsize=14, fontweight='bold')
ax.set_xlabel('回答数')
for i, (idx, row) in enumerate(form_df_sorted.iterrows()):
    ax.text(row['回答数'] + 5, i, f"{row['回答数']} ({row['割合(%)']:.1f}%)", va='center')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '02_参加形態別.png'), dpi=150, bbox_inches='tight')
plt.close()

# 3. 参加立場別
print("\n3. 参加立場別の回答数・割合")
role_counts = df['参加立場'].value_counts()
role_pct = (role_counts / len(df) * 100).round(1)
role_df = pd.DataFrame({
    '回答数': role_counts,
    '割合(%)': role_pct
})
print(role_df)
role_df.to_csv(os.path.join(OUTPUT_TABLES, '03_参加立場別.csv'), encoding='utf-8-sig')

# グラフ
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.Pastel1(range(len(role_counts)))
role_counts.plot(kind='barh', ax=ax, color=colors)
ax.set_title('参加立場別の回答数', fontsize=14, fontweight='bold')
ax.set_xlabel('回答数')
ax.set_ylabel('')
for i, (idx, v) in enumerate(role_counts.items()):
    ax.text(v + 5, i, f'{v} ({role_pct[idx]:.1f}%)', va='center')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '03_参加立場別.png'), dpi=150, bbox_inches='tight')
plt.close()

# 4. システム別
print("\n4. システム別の回答数・割合")
system_cols = ['CoC6', 'CoC7', 'isCoC', 'エモクロア', 'シノビガミ', 'インセイン',
               'D&D', 'DX3rd', 'SW2.0', 'SW2.5', 'その他']
system_counts = {}
for col in system_cols:
    if col in df.columns:
        try:
            count = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int).sum()
            if count > 0:
                system_counts[col] = int(count)
        except:
            pass

# CoC版不明を計算
coc_unknown = df[(df['isCoC'] == 1) & (df['CoC6'] == 0) & (df['CoC7'] == 0)].shape[0]
if coc_unknown > 0:
    system_counts['CoC版不明'] = coc_unknown

system_df = pd.DataFrame({
    'システム': list(system_counts.keys()),
    '回答数': list(system_counts.values())
}).sort_values('回答数', ascending=False)
system_df['割合(%)'] = (system_df['回答数'] / len(df) * 100).round(1)
print(system_df.head(12))
system_df.to_csv(os.path.join(OUTPUT_TABLES, '04_システム別.csv'), encoding='utf-8-sig', index=False)

# グラフ（上位10件、isCoCを除く）
system_df_filtered = system_df[system_df['システム'] != 'isCoC'].head(10)
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.Set2(range(len(system_df_filtered)))
ax.barh(range(len(system_df_filtered)), system_df_filtered['回答数'], color=colors)
ax.set_yticks(range(len(system_df_filtered)))
ax.set_yticklabels(system_df_filtered['システム'])
ax.set_title('システム別の回答数（上位10件）', fontsize=14, fontweight='bold')
ax.set_xlabel('回答数')
ax.invert_yaxis()
for i, (idx, row) in enumerate(system_df_filtered.iterrows()):
    ax.text(row['回答数'] + 5, i, f"{row['回答数']} ({row['割合(%)']:.1f}%)", va='center')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '04_システム別_上位10件.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 3.1.2 時間意識の全体傾向 =====
print("\n" + "=" * 60)
print("3.1.2 時間意識の全体傾向")
print("=" * 60)

# 1. 終了時間意識の分布
print("\n1. 終了時間意識の分布")
# 主要な回答のみ抽出
main_awareness = ['常に意識している', 'ある程度は意識している', 'あまり意識していない', 'ほとんど意識していない']
awareness_counts = df['終了時間意識'].value_counts()
awareness_main = awareness_counts[awareness_counts.index.isin(main_awareness)]
awareness_other = awareness_counts[~awareness_counts.index.isin(main_awareness)].sum()

awareness_df = pd.DataFrame({
    '回答数': awareness_counts,
    '割合(%)': (awareness_counts / len(df) * 100).round(1)
})
print(awareness_df.head(10))
awareness_df.to_csv(os.path.join(OUTPUT_TABLES, '05_終了時間意識.csv'), encoding='utf-8-sig')

# グラフ（主要4項目）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
awareness_main.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('終了時間意識の分布', fontsize=14, fontweight='bold')
ax1.set_xlabel('意識レベル')
ax1.set_ylabel('回答数')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(awareness_main):
    ax1.text(i, v + 5, str(v), ha='center', va='bottom')

ax2.pie(awareness_main, labels=awareness_main.index, autopct='%1.1f%%', startangle=90, colors=colors)
ax2.set_title('終了時間意識の割合', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '05_終了時間意識.png'), dpi=150, bbox_inches='tight')
plt.close()

# 2. 時間超過頻度の分布
print("\n2. 時間超過頻度の分布")
main_overtime = ['ほとんどない', 'あまりない', 'たまにある', 'よくある']
overtime_counts = df['時間超過'].value_counts()
overtime_main = overtime_counts[overtime_counts.index.isin(main_overtime)]
# 正しい順序で並べ替え
overtime_main = overtime_main.reindex([x for x in main_overtime if x in overtime_main.index])

overtime_df = pd.DataFrame({
    '回答数': overtime_counts,
    '割合(%)': (overtime_counts / len(df) * 100).round(1)
})
print(overtime_df.head(10))
overtime_df.to_csv(os.path.join(OUTPUT_TABLES, '06_時間超過頻度.csv'), encoding='utf-8-sig')

# グラフ
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors = ['#90EE90', '#98D8C8', '#FFD93D', '#FF6B6B']
overtime_main.plot(kind='bar', ax=ax1, color=colors)
ax1.set_title('時間超過頻度の分布', fontsize=14, fontweight='bold')
ax1.set_xlabel('超過頻度')
ax1.set_ylabel('回答数')
ax1.tick_params(axis='x', rotation=45)
for i, v in enumerate(overtime_main):
    ax1.text(i, v + 5, str(v), ha='center', va='bottom')

ax2.pie(overtime_main, labels=overtime_main.index, autopct='%1.1f%%', startangle=90, colors=colors)
ax2.set_title('時間超過頻度の割合', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '06_時間超過頻度.png'), dpi=150, bbox_inches='tight')
plt.close()

# 3. GM回答者の割合
print("\n3. GM回答者の割合")
gm_counts = df['GM回答有無'].value_counts()
gm_pct = (gm_counts / len(df) * 100).round(1)
gm_df = pd.DataFrame({
    '回答数': gm_counts,
    '割合(%)': gm_pct
})
print(gm_df)
gm_df.to_csv(os.path.join(OUTPUT_TABLES, '07_GM回答有無.csv'), encoding='utf-8-sig')

# 4. 時間意識と時間超過のクロス集計
print("\n4. 時間意識 × 時間超過のクロス集計")
df_main = df[df['終了時間意識'].isin(main_awareness) & df['時間超過'].isin(main_overtime)]
cross_tab = pd.crosstab(df_main['終了時間意識'], df_main['時間超過'], margins=True)
print(cross_tab)
cross_tab.to_csv(os.path.join(OUTPUT_TABLES, '08_時間意識×時間超過.csv'), encoding='utf-8-sig')

# クロス集計グラフ（割合）
cross_tab_pct = pd.crosstab(df_main['終了時間意識'], df_main['時間超過'], normalize='index') * 100
fig, ax = plt.subplots(figsize=(12, 6))
cross_tab_pct.plot(kind='bar', stacked=True, ax=ax, color=['#90EE90', '#98D8C8', '#FFD93D', '#FF6B6B'])
ax.set_title('終了時間意識別の時間超過頻度（割合）', fontsize=14, fontweight='bold')
ax.set_xlabel('終了時間意識')
ax.set_ylabel('割合 (%)')
ax.legend(title='時間超過頻度', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '07_時間意識×時間超過.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("Phase 1: 基礎集計完了")
print("=" * 60)
print(f"グラフ出力先: {OUTPUT_GRAPHS}")
print(f"表出力先: {OUTPUT_TABLES}")
