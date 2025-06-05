from typing import List
import concurrent.futures
from itertools import islice

DEFAULT_MAX_DICT_SIZE = 1 << 16

from typing import List

def LZW_Compress(data: bytes, max_dict_size: int = DEFAULT_MAX_DICT_SIZE) -> List[int]:
    if not data:
        return []

    Dictionary = {bytes([i]): i for i in range(256)}
    CodeNext = 256
    word = b""
    result = []

    for Byte in data:
        NewWord = word + bytes([Byte])
        if NewWord in Dictionary:
            word = NewWord
        else:
            result.append(Dictionary[word])
            if CodeNext < max_dict_size:
                Dictionary[NewWord] = CodeNext
                CodeNext += 1
            word = bytes([Byte])

    if word:
        result.append(Dictionary[word])

    return result


def LZW_Decompress(codes: List[int], max_dict_size: int = DEFAULT_MAX_DICT_SIZE) -> bytes:
    if not codes:
        return b""

    Dictionary = {i: bytes([i]) for i in range(256)}
    CodeNext = 256

    result = bytearray()
    word = Dictionary.get(codes[0])
    if word is None:
        raise ValueError(f"Invalid first LZW code: {codes[0]}")
    result.extend(word)

    for code in codes[1:]:
        if code in Dictionary:
            entry = Dictionary[code]
        elif code == CodeNext:
            entry = word + word[:1]
        else:
            raise ValueError(f"Invalid LZW code: {code}")

        result.extend(entry)

        if CodeNext < max_dict_size:
            Dictionary[CodeNext] = word + entry[:1]
            CodeNext += 1

        word = entry

    return bytes(result)


def BytesToCodesEncoder(codes: List[int]) -> bytes:
    return b''.join(code.to_bytes(2, 'big') for code in codes)


def BytesToCodesDecoder(data: bytes) -> List[int]:
    if len(data) % 2 != 0:
        raise ValueError(f"Expected even number of bytes, got {len(data)}")
    return [int.from_bytes(data[i:i + 2], 'big') for i in range(0, len(data), 2)]


def ChunkCompressor(data: bytes) -> List[int]:
    return LZW_Compress(data)


def ChunkDecompressor(codes: List[int]) -> bytes:
    return LZW_Decompress(codes)


def LZWParallel(data: bytes, chunk_size=64 * 1024, max_workers=None) -> List[int]:
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        CompressedChunks = list(executor.map(ChunkCompressor, chunks))

    result = []
    for c in CompressedChunks:
        result.append(len(c))  
        result.extend(c)

    return result


def ParallelDecompLZW(codes: List[int]) -> bytes:
    iterator = iter(codes)
    chunks = []

    while True:
        try:
            length = next(iterator)
            chunk = list(islice(iterator, length))
            chunks.append(chunk)
        except StopIteration:
            break

    with concurrent.futures.ProcessPoolExecutor() as executor:
        DeCompressedChunks = list(executor.map(ChunkDecompressor, chunks))

    return b"".join(DeCompressedChunks)


def LZWDecompressFromBytes(data: bytes) -> bytes:
    
    if len(data) % 2 != 0:
        raise ValueError("Invalid data length for 16-bit codes")

    codes = [int.from_bytes(data[i:i+2], 'big') for i in range(0, len(data), 2)]

    MaxCode = 4095 
    if any(code > MaxCode for code in codes):
        print("Warning: LZW codes exceed max expected code")

    return LZW_Decompress(codes)

