import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



new_data = {
    'apple.jpg': {
        'Original size (KB)': 4470.9,
        'LZW': {'Compressed Size (KB)': 8247.37, 'Compression Ratio (%)': 184.47, 'Space Saved (%)': -84.47},
        'RLE': {'Compressed Size (KB)': 4500.88, 'Compression Ratio (%)': 100.67, 'Space Saved (%)': -0.67},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 8452.52, 'Compression Ratio (%)': 189.06, 'Space Saved (%)': -89.06},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
    },
    'cable.jpg': {
        'Original size (KB)': 4596.13,
        'LZW': {'Compressed Size (KB)': 8422.02, 'Compression Ratio (%)': 183.24, 'Space Saved (%)': -83.24},
        'RLE': {'Compressed Size (KB)': 4632.01, 'Compression Ratio (%)': 100.78, 'Space Saved (%)': -0.78},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 8721.4, 'Compression Ratio (%)': 189.76, 'Space Saved (%)': -89.76},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
    },
    'lemon.webp': {
        'Original size (KB)': 6555.24,
        'LZW': {'Compressed Size (KB)': 12313.36, 'Compression Ratio (%)': 187.84, 'Space Saved (%)': -87.84},
        'RLE': {'Compressed Size (KB)': 6582.78, 'Compression Ratio (%)': 100.42, 'Space Saved (%)': -0.42},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 12409.86, 'Compression Ratio (%)': 189.31, 'Space Saved (%)': -89.31},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
    },
    'shell.pdf': {
        'Original size (KB)': 1818.41,
        'LZW': {'Compressed Size (KB)': 3363.85, 'Compression Ratio (%)': 184.99, 'Space Saved (%)': -84.99},
        'RLE': {'Compressed Size (KB)': 1830.29, 'Compression Ratio (%)': 100.65, 'Space Saved (%)': -0.65},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 3458.29, 'Compression Ratio (%)': 190.18, 'Space Saved (%)': -90.18},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
    },
    'vase.png': {
        'Original size (KB)': 11148.14,
        'LZW': {'Compressed Size (KB)': 20877.84, 'Compression Ratio (%)': 187.28, 'Space Saved (%)': -87.28},
        'RLE': {'Compressed Size (KB)': 11211.92, 'Compression Ratio (%)': 100.57, 'Space Saved (%)': -0.57},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 21036.01, 'Compression Ratio (%)': 188.7, 'Space Saved (%)': -88.7},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
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
        
        comp_size = metrics.get('Compressed Size (KB)', None)
        comp_ratio = metrics.get('Compression Ratio (%)', None)
        space_saved = metrics.get('Space Saved (%)', None)

        if comp_size is not None and (comp_ratio is None or space_saved is None):
            comp_ratio = (comp_size / original_size) * 100
            space_saved = 100 - comp_ratio
        
        if comp_size is not None:
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
sns.barplot(data=df, x='File', y='Compressed Size', hue='Algorithm')
plt.title('Original vs Compressed Size (KB) across Algorithms - Image files')
plt.ylabel('Size (KB)')
plt.xticks(rotation=45)
for i, file in enumerate(df['File'].unique()):
    orig_size = df.loc[df['File'] == file, 'Original Size'].iloc[0]
    plt.axhline(orig_size, color='red', linestyle='--', xmin=i/len(df['File'].unique()), xmax=(i+1)/len(df['File'].unique()))

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('barplot_original_vs_compressed_images.png', dpi=900)
plt.close()

pivot_ratio = df.pivot(index='File', columns='Algorithm', values='Compression Ratio (%)')
pivot_saved = df.pivot(index='File', columns='Algorithm', values='Space Saved (%)')

plt.figure(figsize=(12,8))
sns.heatmap(pivot_ratio, annot=True, fmt=".2f", cmap='coolwarm', cbar_kws={'label': 'Compression Ratio (%)'})
plt.title('Compression Ratio Heatmap across Files and Algorithms - Image files')
plt.tight_layout()
plt.savefig('heatmap_compression_ratio_images.png', dpi=900)
plt.close()

plt.figure(figsize=(12,8))
sns.heatmap(pivot_saved, annot=True, fmt=".2f", cmap='YlGnBu', cbar_kws={'label': 'Space Saved (%)'})
plt.title('Space Saved Heatmap across Files and Algorithms - Image files')
plt.tight_layout()
plt.savefig('heatmap_space_saved_images.png', dpi=900)
plt.close()

df.to_csv('compression_data_images.csv', index=False)