# LZW-tANS-RLE_Compression
This project was created for the course "Data Compression Methods"
Written by Adam Burgert

cli.py CLI for user interaction.
•python cli.py –compress –method tans
•python cli.py –decompress –method tans
•Usage:
o  cli.py [-h] [–compress] [–decompress] [–method lzw,rle,rle+lzw, tans,
rle+tans, lzw+tans, rle+lzw+tans]
Files:
•
compress.py
o Compression python file utilizing LZW, RLE, tANS based compression
•decompress.py
•rle.py
•lzw.py
•tans.py
• plot.py
o Generates pdf reports of compression and decompression results
visualizations Table, File, original size,
ocompressed size, compression ratio (%), space saved (%)
