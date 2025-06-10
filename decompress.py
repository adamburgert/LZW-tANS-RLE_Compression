import os
from lzw import LZWDecompressFromBytes, ParallelDecompLZW, LZW_Decompress
from rle import RLE_Decode
import traceback
from io import BytesIO
from tans import TANS


MAGIC_HEADERS_REVERSE = {
    b'LZ__': 'lzw',
    b'rle_': 'rle',
    b'MLZW': 'rle+lzw',
    b'TANS': 'tans',
    b'RTNS': 'rle+tans',
    b'LTNS': 'lzw+tans',
    b'RLTN': 'rle+lzw+tans',
}
def UnpackBits(PackedBits: bytes, length: int) -> list[int]:
    Bits = []
    for b in PackedBits:
        high = (b >> 4) & 0xF
        low = b & 0xF
        Bits.append(high)
        if len(Bits) < length:
            Bits.append(low)
        if len(Bits) >= length:
            break
    return Bits[:length]

def PowerTwo(x: int) -> int:
    return 1 << (x - 1).bit_length()

def ChunkReader(f) -> bytes:
    BytesLength = f.read(4)
    if not BytesLength:
        raise EOFError("No more chunks.")
    if len(BytesLength) < 4:
        raise EOFError("Incomplete chunk length header.")
    length = int.from_bytes(BytesLength, 'big')
    data = f.read(length)
    if len(data) < length:
        raise EOFError("Incomplete chunk data.")
    return data

def TotalChunksReader(f) -> bytes:
    chunks = []
    while True:
        try:
            chunk = ChunkReader(f)
            chunks.append(chunk)
        except EOFError:
            break
    return b''.join(chunks)

def ConvertBytesToCodes(data: bytes, code_size_bytes=2) -> list[int]:
    if len(data) % code_size_bytes != 0:
        raise ValueError("Data length is not multiple of code size")
    return [int.from_bytes(data[i:i+code_size_bytes], 'big') for i in range(0, len(data), code_size_bytes)]

def BytesInts(f, size: int, error_msg: str) -> int:
    data = f.read(size)
    if len(data) < size:
        raise EOFError(error_msg)
    return int.from_bytes(data, 'big')

def TansBitsReader(f):
    BitsLength = BytesInts(f, 4, "Incomplete Bits length")
    Bits = [BytesInts(f, 2, "Incomplete bit value") for _ in range(BitsLength)]
    return Bits

def HandlerTANS(f):
    TableSize = BytesInts(f, 4, "Incomplete TANS table size")
    if TableSize & (TableSize - 1) != 0:
        print(f"!!! Warning: Invalid table size {TableSize}, correcting to next power of two.")
        TableSize = PowerTwo(TableSize)

    FreqTableSize = BytesInts(f, 2, "Incomplete frequency table size")

    FreqTable = {}
    for _ in range(FreqTableSize):
        SymByte = f.read(1)
        if len(SymByte) < 1:
            raise EOFError("Incomplete Freq table Symbol")
        Sym = SymByte[0]
        Freq = BytesInts(f, 4, "Incomplete frequency value")
        FreqTable[Sym] = Freq

    FinalState = BytesInts(f, 4, "Incomplete final state")
    OriginalLength = BytesInts(f, 4, "Incomplete original data length")

    PackedBits_bits = f.read()

    Bits = UnpackBits(PackedBits_bits, OriginalLength)

    try:
        tans = TANS(FreqTable, TableSize=TableSize)
        Decoded = tans.Decode(FinalState, Bits, OriginalLength)
    except Exception as e:
        print(f"!!! Warning: TANS decompression failed: {e}. Skipping this file.")
        return None

    return bytes(Decoded)

def HandlerLZW(f):
    try:
        raw = TotalChunksReader(f)
        if raw:
            codes = ConvertBytesToCodes(raw, 2)
            return ParallelDecompLZW(codes)
    except Exception as e:
        print(f"Chunked ParallelDecompLZW failed: {e}")

    raw = f.read()
    return LZWDecompressFromBytes(raw)

def HandlerRLE(f):
    raw = TotalChunksReader(f)
    print(f"Raw encoded RLE data size read: {len(raw)}")
    Decoded = RLE_Decode(raw)
    print(f"Decoded data size: {len(Decoded)}")
    return Decoded

def HandlerRLE_then_lzw(f):
    RawLZW = TotalChunksReader(f)
    codes = ConvertBytesToCodes(RawLZW, 2)
    LZW_fin = LZW_Decompress(codes)
    return RLE_Decode(LZW_fin)

def HandlerRLE_ThenTANS(f):
    RawRLE = TotalChunksReader(f)
    RLEDecoded = RLE_Decode(RawRLE)

    f_tans = BytesIO(RLEDecoded)
    try:
        return HandlerTANS(f_tans)
    except Exception as e:
        print(f"!!! Warning: TANS decompression failed after RLE: {e}. "
              "Frequency distribution of the data is too skewed or too unique for TANS to handle. "
              "Skipping this file.")
        return None

def HandlerLZW_ThenTANS(f):
    RawLZW = TotalChunksReader(f)
    codes = ConvertBytesToCodes(RawLZW, 2)
    LZW_fin = LZW_Decompress(codes)

    f_tans = BytesIO(LZW_fin)
    try:
        return HandlerTANS(f_tans)
    except Exception as e:
        print(f"!!! Warning: TANS decompression failed after LZW: {e}. "
              "Skipping this file.")
        return None

def HandlerRLELZWThenTANS(f):
    CompData = TotalChunksReader(f)

    try:
        tans_out = HandlerTANS(BytesIO(CompData))
    except Exception as e:
        print(f"!!! Warning: TANS decompression failed: {e}. "
              "Frequency distribution of the data is too skewed or too unique for TANS to handle."
              "Skipping this file.")
        return None 
    if tans_out is None:
        print("!!! Warning: TANS decompression returned None. Skipping this file.")
        return None

    codes = ConvertBytesToCodes(tans_out, 2)
    LZW_fin = LZW_Decompress(codes)

    RLEDecoded = RLE_Decode(LZW_fin)

    return RLEDecoded

def ValStreamPos(f, expected_pos: int, context: str):
    CurrentPosition = f.tell()
    if CurrentPosition != expected_pos:
        raise ValueError(f"Stream position mismatch in {context}: "
                        f"expected={expected_pos}, got={CurrentPosition}")

def FileDecompressor(InputPath: str, OutputPath: str) -> bool:
    try:
        if not os.path.isfile(InputPath):
            raise FileNotFoundError(f"Input file does not exist: {InputPath}")

        if os.path.getsize(InputPath) < 4:
            raise ValueError(f"File too small to contain a valid magic header: {InputPath}")

        with open(InputPath, 'rb') as f:
            magic = f.read(4)
            if not magic or len(magic) < 4:
                raise ValueError(f"File {InputPath} is empty or truncated (magic header: {magic})")

            method = MAGIC_HEADERS_REVERSE.get(magic)
            if not method:
                raise ValueError(f"Unknown magic header: {magic}")

            handlers = {
                'lzw': lambda: HandlerLZW(f),
                'rle': lambda: HandlerRLE(f),
                'rle+lzw': lambda: HandlerRLE_then_lzw(f),
                'tans': lambda: HandlerTANS(f),
                'rle+tans': lambda: HandlerRLE_ThenTANS(f),
                'lzw+tans': lambda: HandlerLZW_ThenTANS(f),
                'rle+lzw+tans': lambda: HandlerRLELZWThenTANS(f),
            }

            handler = handlers.get(method)
            if not handler:
                raise ValueError(f"Unsupported compression method: {method}")

            data = handler()

            if data is None:
                print(f"!!! Skipping writing output: file {InputPath} is not suitable for {method} decompression.")
                return False  

        with open(OutputPath, 'wb') as f_out:
            f_out.write(data)

        return True  
    except Exception as e:
        print(f"Exception during decompression ({InputPath}): {e}")
        traceback.print_exc()
        return False 
