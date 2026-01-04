#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2: クロス集計 - 属性による違いの分析
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
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

df = pd.read_csv(DATA_PATH, encoding='utf-8')
print(f"データ読み込み完了: {len(df)}行\n")

# 定数定義
MAIN_AWARENESS = ['常に意識している', 'ある程度は意識している', 'あまり意識していない', 'ほとんど意識していない']
MAIN_OVERTIME = ['ほとんどない', 'あまりない', 'たまにある', 'よくある']
EXP_ORDER = ['1年未満', '1〜3年', '4〜6年', '7年以上']

print("=" * 60)
print("Phase 2: クロス集計")
print("=" * 60)

# ===== 3.2.1 属性別の時間意識比較 =====

# 1. 経験年数 × 終了時間意識
print("\n1. 経験年数 × 終了時間意識")
df_filtered = df[df['終了時間意識'].isin(MAIN_AWARENESS)]

cross1 = pd.crosstab(df_filtered['経験年数'], df_filtered['終了時間意識'])
cross1 = cross1.reindex([x for x in EXP_ORDER if x in cross1.index])
cross1 = cross1[[c for c in MAIN_AWARENESS if c in cross1.columns]]
cross1_pct = cross1.div(cross1.sum(axis=1), axis=0) * 100
print(cross1)
cross1.to_csv(os.path.join(OUTPUT_TABLES, '09_経験年数×終了時間意識.csv'), encoding='utf-8-sig')

# グラフ
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
cross1_pct.plot(kind='bar', stacked=True, ax=ax, color=colors)
ax.set_title('経験年数別の終了時間意識（割合）', fontsize=14, fontweight='bold')
ax.set_xlabel('経験年数')
ax.set_ylabel('割合 (%)')
ax.legend(title='終了時間意識', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '08_経験年数×終了時間意識.png'), dpi=150, bbox_inches='tight')
plt.close()

# 2. 参加立場 × 終了時間意識
print("\n2. 参加立場 × 終了時間意識")
cross2 = pd.crosstab(df_filtered['参加立場'], df_filtered['終了時間意識'])
cross2 = cross2[[c for c in MAIN_AWARENESS if c in cross2.columns]]
cross2_pct = cross2.div(cross2.sum(axis=1), axis=0) * 100
print(cross2)
cross2.to_csv(os.path.join(OUTPUT_TABLES, '10_参加立場×終了時間意識.csv'), encoding='utf-8-sig')

fig, ax = plt.subplots(figsize=(12, 7))
cross2_pct.plot(kind='barh', stacked=True, ax=ax, color=colors)
ax.set_title('参加立場別の終了時間意識（割合）', fontsize=14, fontweight='bold')
ax.set_xlabel('割合 (%)')
ax.set_ylabel('')
ax.legend(title='終了時間意識', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '09_参加立場×終了時間意識.png'), dpi=150, bbox_inches='tight')
plt.close()

# 3. システム別分析 (CoC vs それ以外)
print("\n3. システム別分析: CoC vs それ以外")
df['システム分類'] = df.apply(
    lambda x: 'CoC' if pd.to_numeric(x.get('isCoC', 0), errors='coerce') == 1 else 'それ以外',
    axis=1
)
df_sys = df[df['終了時間意識'].isin(MAIN_AWARENESS)]

cross3 = pd.crosstab(df_sys['システム分類'], df_sys['終了時間意識'])
cross3 = cross3[[c for c in MAIN_AWARENESS if c in cross3.columns]]
cross3_pct = cross3.div(cross3.sum(axis=1), axis=0) * 100
print(cross3)
cross3.to_csv(os.path.join(OUTPUT_TABLES, '11_CoC vs それ以外×終了時間意識.csv'), encoding='utf-8-sig')

fig, ax = plt.subplots(figsize=(10, 5))
cross3_pct.plot(kind='bar', ax=ax, color=colors)
ax.set_title('システム別（CoC vs それ以外）の終了時間意識', fontsize=14, fontweight='bold')
ax.set_xlabel('システム分類')
ax.set_ylabel('割合 (%)')
ax.legend(title='終了時間意識', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '10_CoC vs それ以外×終了時間意識.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 3.2.2 属性別の時間超過頻度比較 =====

# 4. 経験年数 × 時間超過頻度
print("\n4. 経験年数 × 時間超過頻度")
df_overtime = df[df['時間超過'].isin(MAIN_OVERTIME)]

cross4 = pd.crosstab(df_overtime['経験年数'], df_overtime['時間超過'])
cross4 = cross4.reindex([x for x in EXP_ORDER if x in cross4.index])
cross4 = cross4[[c for c in MAIN_OVERTIME if c in cross4.columns]]
cross4_pct = cross4.div(cross4.sum(axis=1), axis=0) * 100
print(cross4)
cross4.to_csv(os.path.join(OUTPUT_TABLES, '12_経験年数×時間超過頻度.csv'), encoding='utf-8-sig')

fig, ax = plt.subplots(figsize=(12, 6))
colors2 = ['#90EE90', '#98D8C8', '#FFD93D', '#FF6B6B']
cross4_pct.plot(kind='bar', stacked=True, ax=ax, color=colors2)
ax.set_title('経験年数別の時間超過頻度（割合）', fontsize=14, fontweight='bold')
ax.set_xlabel('経験年数')
ax.set_ylabel('割合 (%)')
ax.legend(title='時間超過頻度', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '11_経験年数×時間超過頻度.png'), dpi=150, bbox_inches='tight')
plt.close()

# 5. 参加立場 × 時間超過頻度
print("\n5. 参加立場 × 時間超過頻度")
cross5 = pd.crosstab(df_overtime['参加立場'], df_overtime['時間超過'])
cross5 = cross5[[c for c in MAIN_OVERTIME if c in cross5.columns]]
cross5_pct = cross5.div(cross5.sum(axis=1), axis=0) * 100
print(cross5)
cross5.to_csv(os.path.join(OUTPUT_TABLES, '13_参加立場×時間超過頻度.csv'), encoding='utf-8-sig')

fig, ax = plt.subplots(figsize=(12, 7))
cross5_pct.plot(kind='barh', stacked=True, ax=ax, color=colors2)
ax.set_title('参加立場別の時間超過頻度（割合）', fontsize=14, fontweight='bold')
ax.set_xlabel('割合 (%)')
ax.set_ylabel('')
ax.legend(title='時間超過頻度', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '12_参加立場×時間超過頻度.png'), dpi=150, bbox_inches='tight')
plt.close()

# 6. CoC vs それ以外 × 時間超過頻度
print("\n6. CoC vs それ以外 × 時間超過頻度")
df_overtime['システム分類'] = df.loc[df_overtime.index, 'システム分類']
cross6 = pd.crosstab(df_overtime['システム分類'], df_overtime['時間超過'])
cross6 = cross6[[c for c in MAIN_OVERTIME if c in cross6.columns]]
cross6_pct = cross6.div(cross6.sum(axis=1), axis=0) * 100
print(cross6)
cross6.to_csv(os.path.join(OUTPUT_TABLES, '14_CoC vs それ以外×時間超過頻度.csv'), encoding='utf-8-sig')

fig, ax = plt.subplots(figsize=(10, 5))
cross6_pct.plot(kind='bar', ax=ax, color=colors2)
ax.set_title('システム別（CoC vs それ以外）の時間超過頻度', fontsize=14, fontweight='bold')
ax.set_xlabel('システム分類')
ax.set_ylabel('割合 (%)')
ax.legend(title='時間超過頻度', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '13_CoC vs それ以外×時間超過頻度.png'), dpi=150, bbox_inches='tight')
plt.close()

# 7. 主要システム別の時間意識
print("\n7. 主要システム別の時間意識")
system_cols = ['CoC6', 'CoC7', 'エモクロア', 'シノビガミ', 'インセイン', 'D&D', 'DX3rd', 'SW2.5']
system_awareness = []

for sys in system_cols:
    if sys in df.columns:
        df_sys = df[(df[sys] == 1) & (df['終了時間意識'].isin(MAIN_AWARENESS))]
        if len(df_sys) > 0:
            counts = df_sys['終了時間意識'].value_counts()
            total = counts.sum()
            row = {'システム': sys, 'n': total}
            for awareness in MAIN_AWARENESS:
                row[awareness] = round(counts.get(awareness, 0) / total * 100, 1)
            system_awareness.append(row)

sys_awareness_df = pd.DataFrame(system_awareness)
print(sys_awareness_df)
sys_awareness_df.to_csv(os.path.join(OUTPUT_TABLES, '15_主要システム別×終了時間意識.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(sys_awareness_df))
width = 0.2
for i, awareness in enumerate(MAIN_AWARENESS):
    values = sys_awareness_df[awareness].values
    ax.bar([xi + i*width for xi in x], values, width, label=awareness, color=colors[i])
ax.set_xlabel('システム')
ax.set_ylabel('割合 (%)')
ax.set_title('主要システム別の終了時間意識', fontsize=14, fontweight='bold')
ax.set_xticks([xi + 1.5*width for xi in x])
ax.set_xticklabels(sys_awareness_df['システム'], rotation=45)
ax.legend(title='終了時間意識', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '14_主要システム別×終了時間意識.png'), dpi=150, bbox_inches='tight')
plt.close()

# 8. 主要システム別の時間超過頻度
print("\n8. 主要システム別の時間超過頻度")
system_overtime = []

for sys in system_cols:
    if sys in df.columns:
        df_sys = df[(df[sys] == 1) & (df['時間超過'].isin(MAIN_OVERTIME))]
        if len(df_sys) > 0:
            counts = df_sys['時間超過'].value_counts()
            total = counts.sum()
            row = {'システム': sys, 'n': total}
            for overtime in MAIN_OVERTIME:
                row[overtime] = round(counts.get(overtime, 0) / total * 100, 1)
            system_overtime.append(row)

sys_overtime_df = pd.DataFrame(system_overtime)
print(sys_overtime_df)
sys_overtime_df.to_csv(os.path.join(OUTPUT_TABLES, '16_主要システム別×時間超過頻度.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(sys_overtime_df))
width = 0.2
for i, overtime in enumerate(MAIN_OVERTIME):
    values = sys_overtime_df[overtime].values
    ax.bar([xi + i*width for xi in x], values, width, label=overtime, color=colors2[i])
ax.set_xlabel('システム')
ax.set_ylabel('割合 (%)')
ax.set_title('主要システム別の時間超過頻度', fontsize=14, fontweight='bold')
ax.set_xticks([xi + 1.5*width for xi in x])
ax.set_xticklabels(sys_overtime_df['システム'], rotation=45)
ax.legend(title='時間超過頻度', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '15_主要システム別×時間超過頻度.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("Phase 2: クロス集計完了")
print("=" * 60)
