import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


new_data = {
    'International_recipes.json': {
        'Original size (KB)': 2.65,
        'LZW': {'Compressed Size (KB)': 2.3, 'Compression Ratio (%)': 86.89, 'Space Saved (%)': 13.11},
        'RLE': {'Compressed Size (KB)': 2.56, 'Compression Ratio (%)': 96.47, 'Space Saved (%)': 3.53},
        'tANS': {'Compressed Size (KB)': 1.67, 'Compression Ratio (%)': 62.96, 'Space Saved (%)': 37.04},
        'LZW + tANS': {'Compressed Size (KB)': 2.34, 'Compression Ratio (%)': 88.07, 'Space Saved (%)': 11.93},
        'RLE + LZW': {'Compressed Size (KB)': 2.31, 'Compression Ratio (%)': 87.04, 'Space Saved (%)': 12.96},
        'RLE + tANS': {'Compressed Size (KB)': 1.64, 'Compression Ratio (%)': 61.78, 'Space Saved (%)': 38.22},
        'RLE + LZW + tANS': {'Compressed Size (KB)': 2.35, 'Compression Ratio (%)': 88.73, 'Space Saved (%)': 11.27},
    },
    'Mediterranean recipes.yaml': {
        'Original size (KB)': 2.53,
        'LZW': {'Compressed Size (KB)': 2.27, 'Compression Ratio (%)': 89.78, 'Space Saved (%)': 10.22},
        'RLE': {'Compressed Size (KB)': 2.53, 'Compression Ratio (%)': 99.85, 'Space Saved (%)': 0.15},
        'tANS': {'Compressed Size (KB)': 1.62, 'Compression Ratio (%)': 63.98, 'Space Saved (%)': 36.02},
        'LZW + tANS': {'Compressed Size (KB)': 2.3, 'Compression Ratio (%)': 90.67, 'Space Saved (%)': 9.33},
        'RLE + LZW': {'Compressed Size (KB)': 2.28, 'Compression Ratio (%)': 90.17, 'Space Saved (%)': 9.83},
        'RLE + tANS': {'Compressed Size (KB)': 1.63, 'Compression Ratio (%)': 64.52, 'Space Saved (%)': 35.48},
        'RLE + LZW + tANS': {'Compressed Size (KB)': 2.31, 'Compression Ratio (%)': 91.09, 'Space Saved (%)': 8.91},
    },
    'receptek.html': {
        'Original size (KB)': 4.49,
        'LZW': {'Compressed Size (KB)': 3.28, 'Compression Ratio (%)': 73.0, 'Space Saved (%)': 27.0},
        'RLE': {'Compressed Size (KB)': 3.82, 'Compression Ratio (%)': 85.0, 'Space Saved (%)': 15.0},
        'tANS': {'Compressed Size (KB)': 2.67, 'Compression Ratio (%)': 59.5, 'Space Saved (%)': 40.5},
        'LZW + tANS': {'Compressed Size (KB)': 2.91, 'Compression Ratio (%)': 64.7, 'Space Saved (%)': 35.3}, 
        'RLE + LZW': {'Compressed Size (KB)': 3.21, 'Compression Ratio (%)': 71.39, 'Space Saved (%)': 28.61},
        'RLE + tANS': {'Compressed Size (KB)': 2.36, 'Compression Ratio (%)': 52.57, 'Space Saved (%)': 47.43},
        'RLE + LZW + tANS': {'Compressed Size (KB)': 2.86, 'Compression Ratio (%)': 63.7, 'Space Saved (%)': 36.3},
    },
    'receptek.pdf': {
        'Original size (KB)': 35.72,
        'LZW': {'Compressed Size (KB)': 64.38, 'Compression Ratio (%)': 180.26, 'Space Saved (%)': -80.26},
        'RLE': {'Compressed Size (KB)': 35.73, 'Compression Ratio (%)': 100.04, 'Space Saved (%)': -0.04},
        'tANS': {'Compressed Size (KB)': 19.13, 'Compression Ratio (%)': 53.56, 'Space Saved (%)': 46.44},
        'LZW + tANS': {'Compressed Size (KB)': 33.46, 'Compression Ratio (%)': 93.68, 'Space Saved (%)':6.32 },
        'RLE + LZW': {'Compressed Size (KB)': 64.52, 'Compression Ratio (%)': 180.65, 'Space Saved (%)': -80.65},
        'RLE + tANS': {'Compressed Size (KB)': 19.13, 'Compression Ratio (%)': 53.57, 'Space Saved (%)': 46.43},
        'RLE + LZW + tANS': {'Compressed Size (KB)': 33.53, 'Compression Ratio (%)': 93.87, 'Space Saved (%)': 6.13},
    },
    'receptek.txt': {
        'Original size (KB)': 2.31,
        'LZW': {'Compressed Size (KB)': 2.2, 'Compression Ratio (%)': 95.35, 'Space Saved (%)': 4.65},
        'RLE': {'Compressed Size (KB)': 2.09, 'Compression Ratio (%)': 90.49, 'Space Saved (%)': 9.51},
        'tANS': {'Compressed Size (KB)': 1.55, 'Compression Ratio (%)': 67.2, 'Space Saved (%)': 32.8},
        'LZW + tANS': {'Compressed Size (KB)': 2.27, 'Compression Ratio (%)': 98.06, 'Space Saved (%)': 1.94},
        'RLE + LZW': {'Compressed Size (KB)': 2.17, 'Compression Ratio (%)': 94.0, 'Space Saved (%)': 6.0},
        'RLE + tANS': {'Compressed Size (KB)': 1.47, 'Compression Ratio (%)': 63.78, 'Space Saved (%)': 36.22},
        'RLE + LZW + tANS': {'Compressed Size (KB)': 2.25, 'Compression Ratio (%)': 97.42, 'Space Saved (%)': 2.58},
    },
}

rows = []

for file, algos in new_data.items():
    original_size = algos.get('Original size (KB)', None)
    if original_size is None:
        continue  

    for algo, metrics in algos.items():
        if algo == 'Original size (KB)':
            continue
        
        if metrics is None:
            continue
        
        comp_size = metrics.get('Compressed Size (KB)', None)
        comp_ratio = metrics.get('Compression Ratio (%)', None)
        space_saved = metrics.get('Space Saved (%)', None)

        if comp_size is None:
            continue

        if (comp_ratio is None or space_saved is None) and comp_size is not None:
            comp_ratio = (comp_size / original_size) * 100
            space_saved = 100 - comp_ratio

        rows.append({
            'File': file,
            'Algorithm': algo,
            'Original Size': original_size,
            'Compressed Size': comp_size,
            'Compression Ratio (%)': round(comp_ratio, 2) if comp_ratio is not None else None,
            'Space Saved (%)': round(space_saved, 2) if space_saved is not None else None
        })

df = pd.DataFrame(rows)

plt.figure(figsize=(14,6))
barplot = sns.barplot(data=df, x='File', y='Compressed Size', hue='Algorithm')
plt.title('Original vs Compressed Size (KB) across Algorithms - Text files')
plt.ylabel('Size (KB)')
plt.xticks(rotation=45)

file_positions = {file: pos for pos, file in enumerate(df['File'].unique())}
for file, pos in file_positions.items():
    orig_size = df.loc[df['File'] == file, 'Original Size'].iloc[0]
    plt.hlines(y=orig_size, xmin=pos - 0.4, xmax=pos + 0.4, colors='red', linestyles='--')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('barplot_original_vs_compressed_text.png', dpi=900)
plt.close()

pivot_ratio = df.pivot(index='File', columns='Algorithm', values='Compression Ratio (%)')
pivot_saved = df.pivot(index='File', columns='Algorithm', values='Space Saved (%)')

plt.figure(figsize=(12,8))
sns.heatmap(pivot_ratio, annot=True, fmt=".2f", cmap='coolwarm', cbar_kws={'label': 'Compression Ratio (%)'})
plt.title('Compression Ratio Heatmap across Files and Algorithms - Text files')
plt.tight_layout()
plt.savefig('heatmap_compression_ratio_text.png', dpi=900)
plt.close()

plt.figure(figsize=(12,8))
sns.heatmap(pivot_saved, annot=True, fmt=".2f", cmap='YlGnBu', cbar_kws={'label': 'Space Saved (%)'})
plt.title('Space Saved Heatmap across Files and Algorithms - Text files')
plt.tight_layout()
plt.savefig('heatmap_space_saved_text.png', dpi=900)
plt.close()

df.to_csv('compression_data_text_files.csv', index=False)