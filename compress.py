import os
import traceback
import concurrent.futures
from typing import List, Tuple
from collections import Counter
from lzw import LZWParallel, LZW_Compress
from rle import RLE_Encode
from tans import TANS

MAGIC_HEADERS = {
    'lzw': b'LZ__',
    'rle': b'rle_',
    'tans': b'TANS',
    'rle+lzw': b'MLZW',
    'rle+tans': b'RTNS',
    'lzw+tans': b'LTNS',
    'rle+lzw+tans': b'RLTN',
}
 
def PowerTwo(n: int) -> int:
    return 1 << (n - 1).bit_length()

def ChunkedDataWriter(FileOut, data, ChunkSize: int = 1 << 18):
    if isinstance(data, str):
        data = data.Encode('utf-8')
    for i in range(0, len(data), ChunkSize):
        chunk = data[i:i + ChunkSize]
        FileOut.write(len(chunk).to_bytes(4, 'big'))
        FileOut.write(chunk)

def BitPacker(Bits):
    PackedBits = bytearray()
    for i in range(0, len(Bits), 2):
        FirstBits = Bits[i] & 0xF
        SecondBits = Bits[i+1] & 0xF if i+1 < len(Bits) else 0
        PackedBits.append((FirstBits << 4) | SecondBits)
    return bytes(PackedBits)

class TANSCompressionSkipped(Exception):
    pass

def TansEncoded_Data_Writer(FileOut, FreqTable, Bits, FinalState, original_length, TableSize=65536):
    FileOut.write(TableSize.to_bytes(4, 'big'))
    FileOut.write(len(FreqTable).to_bytes(2, 'big'))
    for Sym, Freq in FreqTable.items():
        FileOut.write(bytes([Sym]))
        FileOut.write(Freq.to_bytes(4, 'big'))
    if isinstance(FinalState, list):
        FinalState = FinalState[-1] 
    FileOut.write(FinalState.to_bytes(4, 'big'))
    FileOut.write(original_length.to_bytes(4, 'big'))
    PackedBits = BitPacker(Bits)
    ChunkedDataWriter(FileOut, PackedBits)

def TansEncode(data: bytes):
    FreqTable = dict(Counter(data))
    TotalFreq = sum(FreqTable.values())
    TableSize = PowerTwo(TotalFreq)
    MAX_TableSize = 1 << 20  
    if TableSize > MAX_TableSize or len(FreqTable) < 2:
        raise TANSCompressionSkipped("!!! File not suitable for TANS compression (table size too large or too few Symbols).")

    MaxFreq = max(FreqTable.values())
    if MaxFreq / TotalFreq > 0.95:
        raise TANSCompressionSkipped("!!! Frequency distribution too skewed for TANS compression.")

    try:
        tans = TANS(FreqTable, TableSize=TableSize)
        FinalState, EncodedBits = tans.Encode(data)
    except Exception as e:
        raise TANSCompressionSkipped(f"!!! TANS encoding failed: {e}")
    while isinstance(FinalState, list):
        FinalState = FinalState[-1]

    return FreqTable, EncodedBits, FinalState, TableSize

def FileCompressor(InputPath: str, OutputPath: str, method: str = 'lzw'):
    try:
        with open(InputPath, 'rb') as f:
            data = f.read()

        if len(data) == 0:
            raise ValueError(f"File {InputPath} is empty and cannot be compressed.")

        with open(OutputPath, 'wb') as FileOut:
            if method == 'lzw':
                codes = list(LZWParallel(data))
                TotalCodeBytes = b''.join(code.to_bytes(2, 'big') for code in codes)
                FileOut.write(MAGIC_HEADERS[method])
                FileOut.write(len(TotalCodeBytes).to_bytes(4, 'big'))
                FileOut.write(TotalCodeBytes)

            elif method == 'rle':
                RleData = RLE_Encode(data)
                FileOut.write(MAGIC_HEADERS[method])
                ChunkedDataWriter(FileOut, RleData)

            elif method == 'rle+lzw':
                RleData = RLE_Encode(data)
                codes = LZW_Compress(RleData)
                TotalCodeBytes = b''.join(code.to_bytes(2, 'big') for code in codes)
                FileOut.write(MAGIC_HEADERS[method])
                ChunkedDataWriter(FileOut, TotalCodeBytes)

            elif method == 'tans':
                FreqTable, EncodedBits, FinalState, TableSize = TansEncode(data)
                FileOut.write(MAGIC_HEADERS[method])
                TansEncoded_Data_Writer(FileOut, FreqTable, EncodedBits, FinalState, len(data), TableSize=TableSize)

            elif method == 'rle+tans':
                RleData = RLE_Encode(data)
                FreqTable, EncodedBits, FinalState, TableSize = TansEncode(RleData)
                FileOut.write(MAGIC_HEADERS[method])
                TansEncoded_Data_Writer(FileOut, FreqTable, EncodedBits, FinalState, len(RleData), TableSize=TableSize)

            elif method == 'lzw+tans':
                lzwCodes = LZW_Compress(data)
                lzwBytes = b''.join(code.to_bytes(2, 'big') for code in lzwCodes)
                FreqTable, EncodedBits, FinalState, TableSize = TansEncode(lzwBytes)
                FileOut.write(MAGIC_HEADERS[method])
                TansEncoded_Data_Writer(FileOut, FreqTable, EncodedBits, FinalState, len(lzwBytes), TableSize=TableSize)

            elif method == 'rle+lzw+tans':
                RleData = RLE_Encode(data)
                lzwCodes = LZW_Compress(RleData)
                lzwBytes = b''.join(code.to_bytes(2, 'big') for code in lzwCodes)
                FreqTable, EncodedBits, FinalState, TableSize = TansEncode(lzwBytes)
                FileOut.write(MAGIC_HEADERS[method])
                TansEncoded_Data_Writer(FileOut, FreqTable, EncodedBits, FinalState, len(lzwBytes), TableSize=TableSize)

            else:
                raise ValueError(f"Unsupported compression method: {method}")

    except TANSCompressionSkipped as e:
        print(f"!!! Skipped TANS compression for {InputPath}: {e}")
        raise

    except Exception as e:
        print(f"X Compression failed for {InputPath} with method {method}: {e}")
        traceback.print_exc()
        raise

def SingleFileProcessor(args):
    File, InputDir, OutputDir, method = args
    InputPath = os.path.join(InputDir, File)
    OutputPath = os.path.join(OutputDir, File)

    try:
        OriginalSize = os.path.getsize(InputPath)
        if OriginalSize == 0:
            return None

        FileCompressor(InputPath, OutputPath, method)
        CompSize = os.path.getsize(OutputPath)

        print(f"Compressed: {File}")
        print(f"Original: {OriginalSize} bytes Compressed: {CompSize} bytes ({CompSize / OriginalSize:.2%})")

        return (File, OriginalSize, CompSize)

    except TANSCompressionSkipped as skip_exc:
        print(f"!!! Skipped TANS compression for {File}: {skip_exc}")
        return None

    except Exception as e:
        print(f"X Compression failed for {File}: {e}")
        traceback.print_exc()
        return None

def ParallelCompressor(InputDir: str, OutputDir: str, method: str = 'lzw') -> Tuple[List[str], List[int], List[int]]:
    os.makedirs(OutputDir, exist_ok=True)

    Files = [f for f in os.listdir(InputDir) if os.path.isfile(os.path.join(InputDir, f))]
    args_list = [(f, InputDir, OutputDir, method) for f in Files]

    FileNames = []
    OriginalSizes = []
    CompSizes = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(SingleFileProcessor, args) for args in args_list]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                fname, orig, comp = result
                FileNames.append(fname)
                OriginalSizes.append(orig)
                CompSizes.append(comp)

    return FileNames, OriginalSizes, CompSizes
