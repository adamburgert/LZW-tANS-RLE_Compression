import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

data = {
    'sample1.data': {
        'LZW': 11.0, 'RLE': 15.33, 'tANS': np.nan, 'LZW + tANS': 2.65,
        'RLE + LZW': 0.5, 'RLE + tANS': 7.7, 'RLE + LZW + tANS': 1.48
    },
    'sample1b.data': {
        'LZW': 11.01, 'RLE': 15.33, 'tANS': np.nan, 'LZW + tANS': 2.65,
        'RLE + LZW': 0.5, 'RLE + tANS': 7.71, 'RLE + LZW + tANS': 1.48
    },
    'sample2.data': {
        'LZW': 181.8, 'RLE': 980.4, 'tANS': 489.56, 'LZW + tANS': 64.18,
        'RLE + LZW': 133.25, 'RLE + tANS': 491.46, 'RLE + LZW + tANS': 67.89
    },
    'sample3.data': {
        'LZW': 199.78, 'RLE': 1251.23, 'tANS': 488.32, 'LZW + tANS': 93.63,
        'RLE + LZW': 234.34, 'RLE + tANS': np.nan , 'RLE + LZW + tANS': 118.44
    },
    'sample4.data': {
        'LZW': 88.25, 'RLE': 383.25, 'tANS': 488.32, 'LZW + tANS': 37.41,
        'RLE + LZW': 78.09, 'RLE + tANS': 191.9, 'RLE + LZW + tANS': 40.31
    },
    'sample5.data': {
        'LZW': 1852.15, 'RLE': 980.45, 'tANS': 489.56, 'LZW + tANS': np.nan,
        'RLE + LZW': 1848.98, 'RLE + tANS': 491.49, 'RLE + LZW + tANS': np.nan
    },
    'sample5b.data': {
        'LZW': 45.12, 'RLE': 15.91, 'tANS': 489.56, 'LZW + tANS': np.nan,
        'RLE + LZW': 10.81, 'RLE + tANS': 9.22, 'RLE + LZW + tANS': 6.67
    },
    'sample6.data': {
        'LZW': 1634.08, 'RLE': 980.49, 'tANS': 489.56, 'LZW + tANS': np.nan,
        'RLE + LZW': 1786.91, 'RLE + tANS': 491.51, 'RLE + LZW + tANS': np.nan
    },
    'sample7.data': {
        'LZW': 1708.25, 'RLE': 994.75, 'tANS': 489.56, 'LZW + tANS': np.nan,
        'RLE + LZW': 1763.4, 'RLE + tANS': 498.64, 'RLE + LZW + tANS': np.nan
    }
}

original_size = 976.56

rows = []
for file, algos in data.items():
    for algo, comp_size in algos.items():
        if comp_size is not None:
            comp_ratio = (comp_size / original_size) * 100
            space_saved = 100 - comp_ratio
            rows.append({
                'File': file,
                'Algorithm': algo,
                'Original Size': original_size,
                'Compressed Size': comp_size,
                'Compression Ratio (%)': round(comp_ratio, 2),
                'Space Saved (%)': round(space_saved, 2)
            })
df = pd.DataFrame(rows)

plt.figure(figsize=(14,6))
sns.barplot(data=df, x='File', y='Compressed Size', hue='Algorithm')
plt.axhline(original_size, color='red', linestyle='--', label='Original Size')
plt.title('Binary files:Original vs Compressed Size (KB) LZW, RLE,tANS, LZW+tANS, RLE+LZW, RLE+tANS, RLE+LZW+tANS')
plt.ylabel('Size (KB)')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('barplot_original_vs_compressed.png' ,dpi=900)
plt.close()

pivot_ratio = df.pivot(index='File', columns='Algorithm', values='Compression Ratio (%)')
pivot_saved = df.pivot(index='File', columns='Algorithm', values='Space Saved (%)')

plt.figure(figsize=(12,8))
sns.heatmap(pivot_ratio, annot=True, fmt=".2f", cmap='coolwarm', cbar_kws={'label': 'Compression Ratio (%)'})
plt.title('Binary files: Compression Ratio Heatmap LZW, RLE,tANS, LZW+tANS, RLE+LZW, RLE+tANS, RLE+LZW+tANS ')
plt.tight_layout()
plt.savefig('heatmap_compression_ratio.png',dpi=900)
plt.close()

plt.figure(figsize=(12,8))
sns.heatmap(pivot_saved, annot=True, fmt=".2f", cmap='YlGnBu', cbar_kws={'label': 'Space Saved (%)'})
plt.title(' Binary files: Space Saved Heatmap LZW, RLE,tANS, LZW+tANS, RLE+LZW, RLE+tANS, RLE+LZW+tANS')
plt.tight_layout()
plt.savefig('heatmap_space_saved.png' ,dpi=900)
plt.close()

df.to_csv('compression_data.csv', index=False)