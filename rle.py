import random
def RLE_Encode(data: bytes) -> bytes:
    Encoded = bytearray()
    i = 0
    n = len(data)
    while i < n:
        RunLength = 1
        while i + RunLength < n and data[i + RunLength] == data[i]:
            RunLength += 1

        if RunLength >= 4:
            val = data[i]
            Rems = RunLength
            while Rems > 0:
                chunk = min(Rems, 255)
                Encoded.append(0)
                Encoded.append(0xFF)
                Encoded.append(val)
                Encoded.append(chunk)
                Rems -= chunk
            i += RunLength
        else:
            for j in range(RunLength):
                Byte = data[i + j]
                if Byte == 0:
                    Encoded.append(0)
                    Encoded.append(0)  
                else:
                    Encoded.append(Byte)
            i += RunLength
    return bytes(Encoded)

def RLE_Decode(data: bytes) -> bytes:
    Decoded = bytearray()
    i = 0
    n = len(data)

    while i < n:
        Byte = data[i]

        if Byte == 0:
            if i + 1 >= n:
                raise ValueError("Truncated escape sequence at end")

            Marker = data[i + 1]
            if Marker == 0:
                Decoded.append(0)
                i += 2
            elif Marker == 0xFF:
                if i + 3 >= n:
                    raise ValueError("Truncated run Marker at end")
                val = data[i + 2]
                RunLen = data[i + 3]
                Decoded.extend([val] * RunLen)
                i += 4
            else:
                Context = data[max(0, i-5):i+10]
                print(f"Invalid escape sequence at pos {i}: 0x00 0x{Marker:02x}, Context bytes: {Context.hex()}")
                raise ValueError(f"Invalid escape sequence: 0x00 0x{Marker:02x}")
        else:
            Decoded.append(Byte)
            i += 1
    return bytes(Decoded)

def Val_RLE_Encoded(data: bytes):
    i = 0
    n = len(data)
    while i < n:
        Byte = data[i]
        if Byte == 0:
            if i + 1 >= n:
                raise ValueError("Incomplete escape or run Marker at EOF during validation")
            NextByte = data[i + 1]
            if NextByte == 0:
                i += 2
            else:
                if i + 2 >= n:
                    raise ValueError("Incomplete run marker during validation")
                i += 3
        else:
            i += 1
    return True

def TestRLERoundTrip():
    for TestNum in range(20):
        size = random.randint(0, 10000)
        data = bytearray(random.getrandbits(8) for _ in range(size))
        Encoded = RLE_Encode(data)
        Decoded = RLE_Decode(Encoded)
        assert Decoded == data, f"Test {TestNum} failed: Decoded data does not match original"
        print(f"Test {TestNum} passed: size {size} bytes, Encoded size {len(Encoded)} bytes")
    print("All tests passed!")
if __name__ == "__main__":
    TestRLERoundTrip()



