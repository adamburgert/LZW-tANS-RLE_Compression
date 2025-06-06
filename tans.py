from collections import Counter
from typing import Dict, List, Tuple

class TANS:
    def __init__(self, FreqTable: Dict[int, int], TableSize=65536):
        if not FreqTable:
            raise ValueError("Empty Freq Table")
        if TableSize & (TableSize - 1) != 0:
            raise ValueError("Table size must be power of two")

        self.TableSize = TableSize
        self.Freq = self.Normalize(FreqTable)
        self.TotalFreq = self.Total_Freq()
        self.SymbolsTable = self.BuildSymbolTable()
        self.Symbol_start = {Sym: start for Sym, start in self.TotalFreq.items()}

    def Normalize(self, FreqTable):
        total_norm = sum(FreqTable.values())
        scale = self.TableSize / total_norm
        Norm = {Sym: max(1, int(Freq * scale)) for Sym, Freq in FreqTable.items()}

        diff = self.TableSize - sum(Norm.values())
        Syms = sorted(Norm, key=lambda s: FreqTable[s], reverse=True)
        i = 0
        while diff != 0:
            Sym = Syms[i % len(Syms)]
            if diff > 0:
                Norm[Sym] += 1
                diff -= 1
            elif Norm[Sym] > 1:
                Norm[Sym] -= 1
                diff += 1
            i += 1
        return Norm

    def Total_Freq(self):
        Total_Freq_Arr = {}
        total = 0
        for Sym in sorted(self.Freq):
            Total_Freq_Arr[Sym] = total
            total += self.Freq[Sym]
        return Total_Freq_Arr

    def BuildSymbolTable(self):
        Table = [None] * self.TableSize
        for Sym in self.Freq:
            start = self.TotalFreq[Sym]
            for i in range(self.Freq[Sym]):
                Table[start + i] = Sym
        return Table

    def Encode(self, data: List[int]) -> Tuple[int, List[int]]:
        state = self.TableSize - 1
        Bits = []

        for Sym in reversed(data):
            Freq = self.Freq[Sym]
            start = self.TotalFreq[Sym]

            x = state
            Bits.append(x % Freq)
            state = start + x // Freq

        Bits.reverse()
        return state, Bits

    def Decode(self, state: int, Bits: List[int], length: int) -> List[int]:
        data = []
        for i in range(length):
            if state < 0 or state >= self.TableSize:
                raise IndexError(f"State {state} out of bounds at Symbol index {i}")

            Sym = self.SymbolsTable[state]
            data.append(Sym)
            Freq = self.Freq[Sym]
            start = self.TotalFreq[Sym]

            r = Bits[i]
            if r >= Freq:
                raise ValueError(f"Bit value {r} >= Freq {Freq} at Symbol index {i}")

            state = Freq * (state - start) + r
        return data

