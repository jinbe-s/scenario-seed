#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 5: 追加分析 - システム特性・形態別など
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

df = pd.read_csv(DATA_PATH, encoding='utf-8')
print("=" * 60)
print("Phase 5: 追加分析")
print("=" * 60)

MAIN_AWARENESS = ['常に意識している', 'ある程度は意識している', 'あまり意識していない', 'ほとんど意識していない']
MAIN_OVERTIME = ['ほとんどない', 'あまりない', 'たまにある', 'よくある']

# ===== 仮説検証1: CoCとそれ以外で時間超過原因が異なるか =====
print("\n" + "-" * 40)
print("仮説検証1: CoC vs それ以外の時間超過原因")
print("-" * 40)

df['システム分類'] = df.apply(
    lambda x: 'CoC' if pd.to_numeric(x.get('isCoC', 0), errors='coerce') == 1 else 'それ以外',
    axis=1
)

# 時間超過原因のキーワード分析
cause_keywords = {
    'RP': ['RP', 'ロールプレイ', '盛り上が'],
    '戦闘': ['戦闘', 'バトル'],
    '相談': ['相談', '会議', 'PL'],
    '探索': ['探索', '謎解き', '情報'],
}

results = []
for sys_type in ['CoC', 'それ以外']:
    df_sys = df[df['システム分類'] == sys_type]
    causes = df_sys['時間超過_原因'].dropna().astype(str)
    all_causes = ' '.join(causes)

    row = {'システム': sys_type, 'n': len(df_sys)}
    for kw_name, kw_list in cause_keywords.items():
        count = sum(len(re.findall(kw, all_causes, re.IGNORECASE)) for kw in kw_list)
        row[kw_name] = count
    results.append(row)

cause_comparison = pd.DataFrame(results)
print("\nCoC vs それ以外の時間超過原因キーワード出現回数:")
print(cause_comparison)
cause_comparison.to_csv(os.path.join(OUTPUT_TABLES, '27_CoC vs それ以外_時間超過原因.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(cause_keywords))
width = 0.35
colors = ['#FF6B6B', '#4ECDC4']

coc_vals = cause_comparison[cause_comparison['システム'] == 'CoC'][list(cause_keywords.keys())].values[0]
other_vals = cause_comparison[cause_comparison['システム'] == 'それ以外'][list(cause_keywords.keys())].values[0]

ax.bar([i - width/2 for i in x], coc_vals, width, label='CoC', color=colors[0])
ax.bar([i + width/2 for i in x], other_vals, width, label='それ以外', color=colors[1])
ax.set_xlabel('時間超過原因')
ax.set_ylabel('出現回数')
ax.set_title('システム別の時間超過原因（キーワード出現回数）', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(list(cause_keywords.keys()))
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '19_CoC vs それ以外_時間超過原因.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 仮説検証2: 経験年数と時間超過の関係 =====
print("\n" + "-" * 40)
print("仮説検証2: 経験年数と時間超過の関係")
print("-" * 40)

# 経験年数別の「ほとんどない」+「あまりない」の割合
exp_order = ['1年未満', '1〜3年', '4〜6年', '7年以上']
df_overtime = df[df['時間超過'].isin(MAIN_OVERTIME)]

exp_overtime_pct = []
for exp in exp_order:
    df_exp = df_overtime[df_overtime['経験年数'] == exp]
    if len(df_exp) > 0:
        low_overtime = df_exp[df_exp['時間超過'].isin(['ほとんどない', 'あまりない'])].shape[0]
        pct = low_overtime / len(df_exp) * 100
        exp_overtime_pct.append({'経験年数': exp, 'n': len(df_exp), '超過少ない割合(%)': round(pct, 1)})

exp_overtime_df = pd.DataFrame(exp_overtime_pct)
print("\n経験年数別の時間超過が少ない割合:")
print(exp_overtime_df)
exp_overtime_df.to_csv(os.path.join(OUTPUT_TABLES, '28_経験年数×時間超過少ない割合.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(exp_overtime_df['経験年数'], exp_overtime_df['超過少ない割合(%)'], color=['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
ax.set_xlabel('経験年数')
ax.set_ylabel('時間超過が少ない割合 (%)')
ax.set_title('経験年数別：時間超過が少ない人の割合', fontsize=14, fontweight='bold')
for i, row in exp_overtime_df.iterrows():
    ax.text(i, row['超過少ない割合(%)'] + 1, f"{row['超過少ない割合(%)']}%", ha='center')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '20_経験年数×時間超過少ない割合.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 仮説検証3: GMの方がPLより時間意識が高いか =====
print("\n" + "-" * 40)
print("仮説検証3: 参加立場と時間意識の関係")
print("-" * 40)

# 参加立場別の「常に意識している」の割合
df_awareness = df[df['終了時間意識'].isin(MAIN_AWARENESS)]
role_awareness_pct = []

for role in df_awareness['参加立場'].unique():
    df_role = df_awareness[df_awareness['参加立場'] == role]
    if len(df_role) > 10:  # サンプルサイズが十分なもののみ
        high_awareness = df_role[df_role['終了時間意識'] == '常に意識している'].shape[0]
        pct = high_awareness / len(df_role) * 100
        role_awareness_pct.append({'参加立場': role, 'n': len(df_role), '常に意識している割合(%)': round(pct, 1)})

role_awareness_df = pd.DataFrame(role_awareness_pct).sort_values('常に意識している割合(%)', ascending=False)
print("\n参加立場別の「常に意識している」割合:")
print(role_awareness_df)
role_awareness_df.to_csv(os.path.join(OUTPUT_TABLES, '29_参加立場×常に意識している割合.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(12, 5))
ax.barh(range(len(role_awareness_df)), role_awareness_df['常に意識している割合(%)'], color=plt.cm.Set2(range(len(role_awareness_df))))
ax.set_yticks(range(len(role_awareness_df)))
ax.set_yticklabels(role_awareness_df['参加立場'])
ax.set_xlabel('「常に意識している」割合 (%)')
ax.set_title('参加立場別：時間を「常に意識している」人の割合', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for i, row in role_awareness_df.iterrows():
    ax.text(row['常に意識している割合(%)'] + 0.5, list(role_awareness_df.index).index(i), f"{row['常に意識している割合(%)']}%", va='center')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '21_参加立場×常に意識している割合.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== 仮説検証4: オンラインとオフラインの違い =====
print("\n" + "-" * 40)
print("仮説検証4: オンラインとオフラインの時間意識")
print("-" * 40)

# 形態別に分析
df['オンラインのみ'] = df['形態'].apply(lambda x: 'オンラインのみ' if isinstance(x, str) and 'オンライン' in x and 'オフライン' not in x else
                                      ('オフライン含む' if isinstance(x, str) and 'オフライン' in x else 'その他'))

online_comparison = []
for form_type in ['オンラインのみ', 'オフライン含む']:
    df_form = df[(df['オンラインのみ'] == form_type) & (df['終了時間意識'].isin(MAIN_AWARENESS))]
    if len(df_form) > 0:
        high = df_form[df_form['終了時間意識'] == '常に意識している'].shape[0]
        pct = high / len(df_form) * 100
        online_comparison.append({'形態': form_type, 'n': len(df_form), '常に意識している割合(%)': round(pct, 1)})

online_df = pd.DataFrame(online_comparison)
print("\nオンライン vs オフラインの時間意識:")
print(online_df)
online_df.to_csv(os.path.join(OUTPUT_TABLES, '30_オンラインvsオフライン_時間意識.csv'), encoding='utf-8-sig', index=False)

# ===== 仮説検証5: システム特性と時間超過 =====
print("\n" + "-" * 40)
print("仮説検証5: システム特性と時間超過")
print("-" * 40)

# 戦闘重視 vs RP重視
df['システム特性'] = 'その他'
# 戦闘重視: D&D, SW2.5, DX3rd
df.loc[(df['D&D'] == 1) | (df['SW2.5'] == 1) | (df['DX3rd'] == 1), 'システム特性'] = '戦闘重視'
# RP重視: CoC, エモクロア
df.loc[(df['isCoC'] == 1) | (df['エモクロア'] == 1), 'システム特性'] = 'RP重視'
# シーン制: シノビガミ, インセイン
df.loc[(df['シノビガミ'] == 1) | (df['インセイン'] == 1), 'システム特性'] = 'シーン制'

system_type_overtime = []
for sys_type in ['戦闘重視', 'RP重視', 'シーン制']:
    df_sys = df[(df['システム特性'] == sys_type) & (df['時間超過'].isin(MAIN_OVERTIME))]
    if len(df_sys) > 0:
        low = df_sys[df_sys['時間超過'].isin(['ほとんどない', 'あまりない'])].shape[0]
        pct = low / len(df_sys) * 100
        system_type_overtime.append({'システム特性': sys_type, 'n': len(df_sys), '超過少ない割合(%)': round(pct, 1)})

system_type_df = pd.DataFrame(system_type_overtime)
print("\nシステム特性別の時間超過が少ない割合:")
print(system_type_df)
system_type_df.to_csv(os.path.join(OUTPUT_TABLES, '31_システム特性×時間超過少ない割合.csv'), encoding='utf-8-sig', index=False)

# グラフ
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(system_type_df['システム特性'], system_type_df['超過少ない割合(%)'], color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax.set_xlabel('システム特性')
ax.set_ylabel('時間超過が少ない割合 (%)')
ax.set_title('システム特性別：時間超過が少ない人の割合', fontsize=14, fontweight='bold')
for i, row in system_type_df.iterrows():
    ax.text(i, row['超過少ない割合(%)'] + 0.5, f"{row['超過少ない割合(%)']}%", ha='center')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '22_システム特性×時間超過少ない割合.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("Phase 5: 追加分析完了")
print("=" * 60)
