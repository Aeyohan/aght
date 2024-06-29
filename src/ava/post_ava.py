#!/usr/bin/env python3

# Allele Variance Applicator - prostprocessor
# Why have 1 output file when you can have all the output files

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

    parser = argparse.ArgumentParser("post_ava", description="ava postprocessor (copy and rename output sequence files)")

    parser.add_argument("--input", "-i", type=ValidFolder, help="Folder with all the ava output .fasta/.fa files",
                        default='.')
    parser.add_argument("--output", "-o", type=ValidOutput, required=True, help="Output folder for renamed outputs to go")

    args = parser.parse_args()
    input_path: pathlib.Path = args.input
    output_path: pathlib.Path = args.output
    if not output_path.exists():
        output_path.mkdir()
    log_file_path = output_path / "post_output.log"
    log_count = 0

    with open(log_file_path, 'w') as log:
        # Recursively get any input .fa/.fasta files
        input_files: List[pathlib.Path] = [file for file in input_path.glob("**/*.fa")]
        input_files += [file for file in input_path.glob("**/*.fasta")]

        # process each file
        for file in tqdm(input_files):
            file: pathlib.Path
            # get the ch and g IDs
            name = file.name.removesuffix(".fa").removesuffix(".fasta")
            segments = name.count("_")
            if segments == 4:
                temp_ch_id_1, temp_ch_id_2, temp_s_id_1, temp_s_id_2, g_id = name.split("_")
                ch_id = f"{temp_ch_id_1}_{temp_ch_id_2}"
                s_id = f"{temp_s_id_1}_{temp_s_id_2}"
            elif segments == 3:
                temp_ch_id_1, temp_ch_id_2, s_id, g_id = name.split("_")
                ch_id = f"{temp_ch_id_1}_{temp_ch_id_2}"
                log.write(f"Warning: Potentially malformed name While attempting to rename '{name}'. Assuming "
                          f"Chromosome: {ch_id}, sample: {s_id}, gene: {g_id} \n")
                log_count += 1
            elif segments == 2:
                ch_id, s_id, g_id = name.split("_")
                log.write(f"Warning: Potentially malformed name While attempting to rename '{name}'. Assuming "
                          f"Chromosome: {ch_id}, sample: {s_id}, gene: {g_id} \n")
                log_count += 1
            else:
                log.write(f"Error: Could not determine file name for {name}")
                log_count += 1
                continue

            # determine output subdirectory
            out_subdir = output_path / f"{ch_id}_{g_id}"
            if not out_subdir.exists():
                out_subdir.mkdir()

            # start moving data from the old file to the new one, but be sure to change the file name and sequence name
            out_file = out_subdir / f"{s_id}.fa"
            with open(file, 'r') as file_in:
                with open(out_file, 'w') as file_out:
                    first_line = file_in.readline()
                    if first_line == "":
                        log.write(f"Empty value in {file.name}\n")
                        log_count += 1
                        continue
                    if f">{name}" not in first_line:
                        log.write(f"unexpected data in {file.name}\n")
                        log_count += 1
                    file_out.write(f">{s_id}\n")
                    line = file_in.readline()
                    while line != "":
                        file_out.write(line)
                        line = file_in.readline()

    print(f"Renamed {len(input_files)} files with {log_count} potential issues. {f'See {str(log_file_path)} for more details' if log_count else ''}")

if __name__ == "__main__":
    main()