#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 6: 除外キーワード版ランキングとワードクラウド
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
print("Phase 6: 除外キーワード版ランキングとワードクラウド")
print("=" * 60)

# 除外するキーワード
EXCLUDE_KEYWORDS = ['時間', 'PL', 'GM']

# ===== 時間意識理由のキーワード分析（除外版） =====
print("\n" + "-" * 40)
print("時間意識理由キーワード（時間・PL・GM除外）")
print("-" * 40)

reasons = df['時間意識_理由'].dropna().astype(str)
all_text = ' '.join(reasons)

# 詳細キーワード（除外対象を除く）
detailed_keywords = ['睡眠', '仕事', '翌日', '体調', '健康', '終電', '会場',
                     '約束', '迷惑', '配慮', '集中', '疲労', '生活',
                     '予定', '眠', '寝る', '社会人', '明日', '管理']

keyword_counts = {}
for kw in detailed_keywords:
    count = len(re.findall(kw, all_text, re.IGNORECASE))
    if count > 0:
        keyword_counts[kw] = count

keyword_df = pd.DataFrame(list(keyword_counts.items()), columns=['キーワード', '出現回数'])
keyword_df = keyword_df.sort_values('出現回数', ascending=False)
print("\n時間意識の理由 - 頻出キーワード（時間・PL・GM除外）:")
print(keyword_df.head(10))
keyword_df.to_csv(os.path.join(OUTPUT_TABLES, '33_時間意識理由_キーワード_除外版.csv'), encoding='utf-8-sig', index=False)

# グラフ（除外版TOP10）
fig, ax = plt.subplots(figsize=(10, 6))
top_kw = keyword_df.head(10)
colors = plt.cm.Pastel1(range(len(top_kw)))
bars = ax.barh(range(len(top_kw)), top_kw['出現回数'], color=colors)
ax.set_yticks(range(len(top_kw)))
ax.set_yticklabels(top_kw['キーワード'])
ax.set_title('時間意識の理由 - 頻出キーワードTOP10\n（「時間」「PL」「GM」除外）', fontsize=12, fontweight='bold')
ax.set_xlabel('出現回数')
ax.invert_yaxis()

# 数値ラベル追加
for i, (kw, count) in enumerate(zip(top_kw['キーワード'], top_kw['出現回数'])):
    ax.text(count + 2, i, str(count), va='center')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_GRAPHS, '23_時間意識理由_キーワード_除外版.png'), dpi=150, bbox_inches='tight')
plt.close()

# ===== ワードクラウド作成 =====
print("\n" + "-" * 40)
print("ワードクラウド作成")
print("-" * 40)

try:
    from wordcloud import WordCloud

    # 日本語フォントパス（Windows）
    font_paths = [
        'C:/Windows/Fonts/msgothic.ttc',
        'C:/Windows/Fonts/YuGothM.ttc',
        'C:/Windows/Fonts/meiryo.ttc',
    ]

    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break

    if font_path is None:
        print("警告: 日本語フォントが見つかりません")
        font_path = 'C:/Windows/Fonts/msgothic.ttc'

    # 除外キーワードを小文字も含めて設定
    stopwords = set(['時間', 'PL', 'GM', 'pl', 'gm', 'Pl', 'Gm'])

    # ワードクラウド生成（キーワード頻度辞書から）
    wc = WordCloud(
        font_path=font_path,
        width=1200,
        height=800,
        background_color='white',
        stopwords=stopwords,
        max_words=50,
        colormap='viridis',
        min_font_size=10
    )

    # キーワード辞書からワードクラウド生成
    wc.generate_from_frequencies(keyword_counts)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('時間意識の理由 - ワードクラウド\n（「時間」「PL」「GM」除外）', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_GRAPHS, '24_時間意識理由_ワードクラウド_除外版.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("ワードクラウドを保存しました")

except ImportError:
    print("wordcloudライブラリがインストールされていません")
    print("pip install wordcloud でインストールしてください")

    # 代替: 簡易的な棒グラフをワードクラウド風に
    fig, ax = plt.subplots(figsize=(12, 8))

    # フォントサイズを出現回数に比例させる
    max_count = keyword_df['出現回数'].max()

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_title('時間意識の理由 - キーワード頻度\n（「時間」「PL」「GM」除外）', fontsize=14, fontweight='bold')

    # 上位キーワードを配置
    positions = [
        (50, 70), (25, 50), (75, 50), (15, 30), (50, 40),
        (85, 30), (35, 20), (65, 20), (20, 80), (80, 80)
    ]

    for i, (_, row) in enumerate(keyword_df.head(10).iterrows()):
        if i < len(positions):
            size = 10 + (row['出現回数'] / max_count) * 30
            ax.text(positions[i][0], positions[i][1], row['キーワード'],
                   fontsize=size, ha='center', va='center',
                   fontweight='bold', color=plt.cm.viridis(row['出現回数'] / max_count))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_GRAPHS, '24_時間意識理由_キーワード図_除外版.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("代替キーワード図を保存しました")

print("\n" + "=" * 60)
print("Phase 6: 完了")
print("=" * 60)
