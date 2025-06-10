import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
new_data = {
    'mixkit-birds-chirping-near-the-river-2473.wav': {
        'Original size (KB)': 23290.82,
        'LZW': {'Compressed Size (KB)': 32751.94, 'Compression Ratio (%)': 140.62, 'Space Saved (%)': -40.62},
        'RLE': {'Compressed Size (KB)': 26342.19, 'Compression Ratio (%)': 113.1, 'Space Saved (%)': -13.1},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 38212.32, 'Compression Ratio (%)': 164.07, 'Space Saved (%)': -64.07},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
    },
    'mixkit-river-surroundings-in-the-jungle-2451.wav': {
        'Original size (KB)': 15541.19,
        'LZW': {'Compressed Size (KB)': 23363.35, 'Compression Ratio (%)': 150.33, 'Space Saved (%)': -50.33},
        'RLE': {'Compressed Size (KB)': 16687.1, 'Compression Ratio (%)': 107.37, 'Space Saved (%)': -7.37},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 27001.73, 'Compression Ratio (%)': 173.74, 'Space Saved (%)': -73.74},
        'RLE + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
    },
    'rmixkit-sea-waves-with-birds-loop-1185.wav': {
        'Original size (KB)': 6553.28,
        'LZW': {'Compressed Size (KB)': 9181.9, 'Compression Ratio (%)': 140.11, 'Space Saved (%)': -40.11},
        'RLE': {'Compressed Size (KB)': 6747.7, 'Compression Ratio (%)': 102.97, 'Space Saved (%)': -2.97},
        'tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'LZW + tANS': {'Compressed Size (KB)': None, 'Compression Ratio (%)': None, 'Space Saved (%)': None},
        'RLE + LZW': {'Compressed Size (KB)': 9169.18, 'Compression Ratio (%)': 139.92, 'Space Saved (%)': -39.92},
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
plt.title('Original vs Compressed Size (KB) across Algorithms - Sound files')
plt.ylabel('Size (KB)')
plt.xticks(rotation=45)

file_positions = {file: pos for pos, file in enumerate(df['File'].unique())}
for file, pos in file_positions.items():
    orig_size = df.loc[df['File'] == file, 'Original Size'].iloc[0]
    plt.hlines(y=orig_size, xmin=pos - 0.4, xmax=pos + 0.4, colors='red', linestyles='--')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('barplot_original_vs_compressed_soundfiles.png',dpi=900)
plt.close()

pivot_ratio = df.pivot(index='File', columns='Algorithm', values='Compression Ratio (%)')
pivot_saved = df.pivot(index='File', columns='Algorithm', values='Space Saved (%)')

plt.figure(figsize=(12,8))
sns.heatmap(pivot_ratio, annot=True, fmt=".2f", cmap='coolwarm', cbar_kws={'label': 'Compression Ratio (%)'})
plt.title('Compression Ratio Heatmap across Files and Algorithms, Sound files')
plt.tight_layout()
plt.savefig('heatmap_compression_ratio_soundfiles.png',dpi=900)
plt.close()

plt.figure(figsize=(12,8))
sns.heatmap(pivot_saved, annot=True, fmt=".2f", cmap='YlGnBu', cbar_kws={'label': 'Space Saved (%)'})
plt.title('Space Saved Heatmap across Files and Algorithms, Sound files')
plt.tight_layout()
plt.savefig('heatmap_space_saved_soundfiles.png',dpi=900)
plt.close()

df.to_csv('compression_data_soundfiles.csv', index=False)
