import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def GenCompReport(output_dir, method, file_names, original_sizes, compressed_sizes):
    if not file_names:
        print("No files were compressed, skipping report generation.")
        return

    orig_kb = [s / 1024 for s in original_sizes]
    comp_kb = [s / 1024 for s in compressed_sizes]
    space_saved = [100 * (1 - c / o) for c, o in zip(compressed_sizes, original_sizes)]

    df = pd.DataFrame({
        'File': file_names,
        'Original (KB)': orig_kb,
        'Compressed (KB)': comp_kb,
        'Compression Ratio (%)': [100 * c / o for c, o in zip(compressed_sizes, original_sizes)],
        'Space Saved (%)': space_saved
    }).set_index('File')

    pdf_path = os.path.join(output_dir, f"compression_report_{method}.pdf")
    with PdfPages(pdf_path) as pdf:
        plt.figure(figsize=(12, 6))
        x = range(len(file_names))
        plt.bar(x, orig_kb, width=0.4, label='Original (KB)', align='center')
        plt.bar([i + 0.4 for i in x], comp_kb, width=0.4, label='Compressed (KB)', align='center')
        plt.xticks([i + 0.2 for i in x], file_names, rotation=45, ha='right')
        plt.ylabel("File size (KB)")
        plt.title(f"Compression Size Comparison ({method})")
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(12, max(2, len(file_names)*0.4)))
        plt.axis('off')
        tbl = plt.table(
            cellText=df.round(2).values,
            colLabels=df.columns,
            rowLabels=df.index,
            loc='center',
            cellLoc='center',
            colWidths=[0.25, 0.18, 0.18, 0.2, 0.2]
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1.2, 1.2)
        plt.title(f"Compression Details Table ({method})", pad=20)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(10, max(3, len(file_names)*0.5)))
        heatmap = sns.heatmap(
            df[['Compression Ratio (%)']],
            annot=True,
            fmt=".2f",
            cmap='coolwarm',
            cbar=True,
            linewidths=0.5,
            linecolor='gray'
        )
        heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0, fontsize=9)
        plt.title(f"Compression Ratio Heatmap ({method})", pad=20)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(10, max(3, len(file_names)*0.5)))
        space_saved_heatmap = sns.heatmap(
            df[['Space Saved (%)']],
            annot=True,
            fmt=".2f",
            cmap='Greens',
            cbar=True,
            linewidths=0.5,
            linecolor='gray'
        )
        space_saved_heatmap.set_yticklabels(space_saved_heatmap.get_yticklabels(), rotation=0, fontsize=9)
        plt.title(f"Space Saved Heatmap ({method})", pad=20)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
    print(f"Compression report saved to: {pdf_path}")

def GenDeCompReport(output_dir, method, file_names, original_sizes, decompressed_sizes):
    if not file_names:
        print("No files were decompressed, skipping report generation.")
        return
    orig_kb = [s / 1024 for s in original_sizes]
    decomp_kb = [s / 1024 for s in decompressed_sizes]
    space_saved = [100 * (1 - d / o) for d, o in zip(decompressed_sizes, original_sizes)]

    df = pd.DataFrame({
        'File': file_names,
        'Original (KB)': orig_kb,
        'Decompressed (KB)': decomp_kb,
        'Decompression Ratio (%)': [100 * d / o for d, o in zip(decompressed_sizes, original_sizes)],
        'Space Saved (%)': space_saved
    }).set_index('File')
    pdf_path = os.path.join(output_dir, f"decompression_report_{method}.pdf")
    with PdfPages(pdf_path) as pdf:
        plt.figure(figsize=(12, 6))
        x = range(len(file_names))
        plt.bar(x, orig_kb, width=0.4, label='Original (KB)', align='center')
        plt.bar([i + 0.4 for i in x], decomp_kb, width=0.4, label='Decompressed (KB)', align='center')
        plt.xticks([i + 0.2 for i in x], file_names, rotation=45, ha='right')
        plt.ylabel("File size (KB)")
        plt.title(f"Decompression Size Comparison ({method})")
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()
        plt.figure(figsize=(12, max(2, len(file_names)*0.4)))
        plt.axis('off')
        tbl = plt.table(
            cellText=df.round(2).values,
            colLabels=df.columns,
            rowLabels=df.index,
            loc='center',
            cellLoc='center',
            colWidths=[0.25, 0.18, 0.18, 0.2, 0.2]
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1.2, 1.2)
        plt.title(f"Decompression Details Table ({method})", pad=20)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
        plt.figure(figsize=(10, max(3, len(file_names)*0.5)))
        heatmap = sns.heatmap(
            df[['Decompression Ratio (%)']],
            annot=True,
            fmt=".2f",
            cmap='coolwarm',
            cbar=True,
            linewidths=0.5,
            linecolor='gray'
        )
        heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0, fontsize=9)
        plt.title(f"Decompression Ratio Heatmap ({method})", pad=20)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
        plt.figure(figsize=(10, max(3, len(file_names)*0.5)))
        space_saved_heatmap = sns.heatmap(
            df[['Space Saved (%)']],
            annot=True,
            fmt=".2f",
            cmap='Greens',
            cbar=True,
            linewidths=0.5,
            linecolor='gray'
        )
        space_saved_heatmap.set_yticklabels(space_saved_heatmap.get_yticklabels(), rotation=0, fontsize=9)
        plt.title(f"Space Saved Heatmap ({method})", pad=20)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
    print(f" Decompression report saved to: {pdf_path}")
