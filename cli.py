import argparse
import os
import concurrent.futures
from compress import FileCompressor
from decompress import FileDecompressor
from plot import GenCompReport, GenDeCompReport

def SuffixAdder(FileName: str, SUFFIX: str) -> str:
    BASE, Extension = os.path.splitext(FileName)
    return f"{BASE}_{SUFFIX}{Extension}"

def SuffixRemover(FileName: str, SuffixesList: list[str]) -> str:
    BASE, Extension = os.path.splitext(FileName)
    for SUFFIX in SuffixesList:
        PatternLogic = f"_{SUFFIX}"
        if BASE.endswith(PatternLogic):
            return BASE[:-len(PatternLogic)] + Extension
    return FileName

def CompressionProcessor(args):
    File, InputDir, OutputDir, method, SUFFIX = args
    InputPath = os.path.join(InputDir, File)
    OutputPath = os.path.join(OutputDir, File)

    try:
        if os.path.getsize(InputPath) == 0:
            print(f" Skipping empty File: {File}")
            return None

        FileCompressor(InputPath, OutputPath, method)
        CompSize = os.path.getsize(OutputPath)

        NewName = SuffixAdder(File, SUFFIX)
        NewPath = os.path.join(OutputDir, NewName)
        os.rename(OutputPath, NewPath)

        return (NewName, os.path.getsize(InputPath), CompSize)

    except Exception as e:
        print(f"X Compression failed for {File}: {e}")
        return None

def DecompressionProcessor(args):
    File, InputDir, OutputDir, SuffixesList = args
    InputPath = os.path.join(InputDir, File)
    OutputPath = os.path.join(OutputDir, File)

    try:
        result = FileDecompressor(InputPath, OutputPath)
        if result is None:
            err_msg = "TANS compression failed! File not suitable for TANS compression!"
            print(f"!!! Skipping writing output: File {File} is not suitable for TANS decompression.")
            return (File, os.path.getsize(InputPath), 0, False, err_msg)

        if not os.path.exists(OutputPath):
            err_msg = f"Expected decompressed File {OutputPath} not found."
            return (File, os.path.getsize(InputPath), 0, False, err_msg)

        DecompSize = os.path.getsize(OutputPath)
        CleanedName = SuffixRemover(File, SuffixesList)
        FinalPath = os.path.join(OutputDir, CleanedName)
        if OutputPath != FinalPath:
            os.rename(OutputPath, FinalPath)

        return (CleanedName, os.path.getsize(InputPath), DecompSize, True, None)

    except Exception as e:
        OriginalSize = os.path.getsize(InputPath) if os.path.exists(InputPath) else 0
        return (File, OriginalSize, 0, False, str(e))

 
def main():
    Getter = argparse.ArgumentParser(description="Parallel Compression/Decompression Pipeline")
    Getter.add_argument("--compress", action="store_true", help="Run compression pipeline")
    Getter.add_argument("--decompress", action="store_true", help="Run decompression pipeline")
    Getter.add_argument(
        "--method",
        choices=[
            'lzw',
            'rle',
            'rle+lzw',
            'tans',
            'rle+tans',
            'lzw+tans',
            'rle+lzw+tans'
        ],
        default='lzw',
        help="Compression/decompression method"
    )
    args = Getter.parse_args()

    SuffixesList = {
        'lzw': 'lzw_compressed',
        'rle': 'rle_compressed',
        'rle+lzw': 'rle_lzw_compressed',
        'tans': 'tans_compressed',
        'rle+tans': 'rle_tans_compressed',
        'lzw+tans': 'lzw_tans_compressed',
        'rle+lzw+tans': 'rle_lzw_tans_compressed'
    }
    SUFFIX = SuffixesList.get(args.method, 'compressed')

    ReportsDir = 'reports'
    os.makedirs(ReportsDir, exist_ok=True) 

    if args.compress:
        InputDir = 'samples'
        OutputDir = 'compressed'
        os.makedirs(OutputDir, exist_ok=True)

        Files = [f for f in os.listdir(InputDir) if os.path.isfile(os.path.join(InputDir, f))]
        Tasks = [(f, InputDir, OutputDir, args.method, SUFFIX) for f in Files]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(CompressionProcessor, Tasks))

        ValidResults = [r for r in results if r]
        if ValidResults:
            files_, OriginalSizes, CompSizes = zip(*ValidResults)
            GenCompReport(ReportsDir, args.method, files_, OriginalSizes, CompSizes)
            print(f" Compression report saved to: {ReportsDir}")
        else:
            print("No Files were compressed.")

    elif args.decompress:
        InputDir = 'compressed'
        OutputDir = 'decompressed'
        os.makedirs(OutputDir, exist_ok=True)

        Files = [f for f in os.listdir(InputDir) if os.path.isfile(os.path.join(InputDir, f))]
        SuffixesList = list(SuffixesList.values())
        Tasks = [(f, InputDir, OutputDir, SuffixesList) for f in Files]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(DecompressionProcessor, Tasks))

        for File, orig_size, dec_size, success, err in results:
            if success:
                print(f"Decompressed: {File} (Original: {orig_size} bytes, Decompressed: {dec_size} bytes)")
            else:
                print(f"X Failed to decompress: {File} ({err})")

        Success_Res = [r for r in results if r[3]]
        if Success_Res:
            files_, OriginalSizes, dec_sizes, _, _ = zip(*Success_Res)
            GenDeCompReport(ReportsDir, args.method, files_, OriginalSizes, dec_sizes)
            print(f" Decompression report saved to: {ReportsDir}")
        else:
            print("No Files were successfully decompressed.")

    else:
        Getter.print_help()

if __name__ == "__main__":
    main()
