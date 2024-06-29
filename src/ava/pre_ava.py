#!/usr/bin/env python3

# Allele Variance Applicator - preprocessor.
# Remove instances of a string from an input file name

import argparse
import errno
import pathlib

from typing import List, Dict, Set, Tuple

from tqdm import tqdm

try:
    from ava.argparse_helpers import ValidFolder, ValidFile, ValidOutput
except:
    # allow imports when run in place
    from argparse_helpers import ValidFolder, ValidFile, ValidOutput


def main():
    # Load input arguments

    parser = argparse.ArgumentParser("pre_ava", description="ava preprocessor (rename input variant files)")

    parser.add_argument("--input", "-i", type=ValidFolder, help="Folder with all the input .csv and .fasta files",
                        default='.')
    parser.add_argument("--name", "-n", type=str, default=" (Variants, filtered)", help="Name to remove from file names")

    args = parser.parse_args()
    input_path: pathlib.Path = args.input
    name: str = args.name

    # Recursively get any input .csv files and rename instances with name
    input_variances: List[pathlib.Path] = [file for file in input_path.glob("**/*.csv")]

    # Rename each file
    counter = 0
    for file in tqdm(input_variances):
        file: pathlib.Path
        if name in file.name:
            file.rename(str(file.absolute()).replace(name, ""))
            counter += 1

    print(f"Renamed {counter} files")

if __name__ == "__main__":
    main()