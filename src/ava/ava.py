#!/usr/bin/env python3

# Allele Variance Applicator

import argparse
import errno
from io import TextIOWrapper
from multiprocessing import Pool
import os
import pathlib

import pandas

from typing import List, Dict, Set, Tuple
from pyfaidx import Fasta, FastaRecord, MutableFastaRecord

from tqdm import tqdm
try:
    from ava.argparse_helpers import ValidFolder, ValidFile, ValidOutput
    from ava.metadata_types import Cid, Gid, Sid
    from ava.parallellisation import parse_variant_compat, process_variations_compat
except:
    # allow imports when run in place
    from argparse_helpers import ValidFolder, ValidFile, ValidOutput
    from metadata_types import Cid, Gid, Sid
    from parallellisation import parse_variant_compat, process_variations_compat

def load_sequences(sequence_paths: List[pathlib.Path]) -> Dict[FastaRecord, Fasta]:
    result = {}

    for path in tqdm(sequence_paths, desc="Loading sequence files: "):
        data = Fasta(path.absolute(), one_based_attributes=False)
        for cid in data:
            result[cid.name] = data
    return result

def load_config(cfg_file: pathlib.Path):
    result: Dict[Cid, Dict[Gid, List[range]]] = {}

    cfg = pandas.read_csv(str(cfg_file.absolute()))

    # Get a list of genes in each chromosome
    for cid, gid, region_str in zip(cfg['Chromosome_ID'], cfg['Gene_ID'], cfg['Region']):
        if not cid in result:
            result[cid] = {}
        region_str: str
        regions: List[range] = []
        prefix = "complement("
        suffix = ")"
        if region_str.startswith(prefix):
            region_str = region_str.removeprefix(prefix).removesuffix(suffix)
        prefix = "join("
        if region_str.startswith(prefix):
            region_str = region_str.removeprefix(prefix).removesuffix(")")
        for region in region_str.split(","):
            values = region.split("..")
            regions.append(range(int(values[0]) - 1, int(values[1])))
        result[cid][gid] = regions

    return result

def parse_variant(variant_path: pathlib.Path, info: dict[Cid, Set[Gid]], log_output: TextIOWrapper):
    name = variant_path.name
    gid: Gid | None = None
    data = pandas.read_csv(str(variant_path.absolute()))

    if not len(data):
        log_output.write(f"[WARN] While parsing {str(variant_path.absolute())}: File has no entries. Unable to map "
                         f"variants to a known chromosomes detected in same file. Skipping.\n")
        return None

    # Get the first value
    ch = data["Chromosome"][0]

    # See if there's a gene in this chromosome in the file name
    sid = None
    gid = None
    for gene in info[ch]:
        if gene in name:
            sid = name.removesuffix(variant_path.suffix).removesuffix(gene).removesuffix("_")
            gid = gene
            break

    if sid == None:
        return None

    sid: Sid
    gid: Gid

    # Get the variation data
    prev_region = ""
    prev_allele = ""
    variances: Dict[int, Tuple[str, str]] = {}

    for cid, region, ref, allele in zip(data["Chromosome"], data["Region"], data["Reference"], data["Allele"]):
        if (cid != ch):
            log_output.write(f"[WARN] While parsing {str(variant_path.absolute())}: multiple chromosomes detected in"
                             f" same file. This will cause unexpected behaviour\n")

        # Check for an edge case for two regions with different alleles
        if prev_region == region and allele != ref and prev_allele != ref:
            log_output.write(f"[WARN] Unexpected event. Found an instance in {str(variant_path.absolute())} where "
                             f"neither allele - ({allele} and {prev_allele}) did not match the reference: {ref} at position {region}\n")

        prev_region = region
        prev_allele = allele

        # Skip instances where this was not the variance
        if allele == ref:
            continue

        variances[int(region) - 1] = (ref, allele)

    return (sid, ch, gid, variances)

def load_variants(variant_paths: List[pathlib.Path], cfg_file: pathlib.Path, cfg: dict[Cid, Set[Gid]],
                  log_output: TextIOWrapper):
    # Remove cfg file from variant (if present)
    if cfg_file in variant_paths:
        variant_paths.remove(cfg_file)

    result: Dict[Sid, Dict[Cid, Dict[Gid, Dict[int, Tuple[str, str]]]]] = {}

    # Todo use parallel implementation if requested
    for variant in tqdm(variant_paths, desc="Loading variant files: "):
        values: tuple[Sid, Gid, Dict[int, Tuple[str, str]]] | None = parse_variant(variant, cfg, log_output)
        if values is None:
            continue
        sid, cid, gid, ranges = values

        if not sid in result:
            result[sid] = {}

        if not cid in result[sid]:
            result[sid][cid] = {}

        if (gid in result[sid]):
            log_output.write(f"[WARN], variant files for different genes, were for the same gene {gid} from sample {sid}\n")

        result[sid][cid][gid] = ranges

    return result

def process_variations(args: Tuple[pathlib.Path, Tuple[Sid, Cid, Gid, List[range], Dict[int, Tuple[str, str]],
                                                      FastaRecord], TextIOWrapper]):
    output_root, data, log_output = args
    # Create a temp file and copy the contents of
    sid, cid, gid, ranges, variations, record = data
    temp_file = output_root / f"{cid}_{sid}_{gid}_temp.fa"
    with open(temp_file, 'w') as f:
        f.write(f">{record.name}\n")
        for line in record:
            f.write(f"{str(line)}\n")

    # temp file has been created. Open it as a fasta, but make it mutable
    fasta = Fasta(temp_file.absolute(), one_based_attributes=False, mutable=True)
    mutable = fasta[cid]

    failed_modifications = []

    # Apply changes gloablly for this sample
    for index, [current, new] in variations.items():
        if (mutable[index] != current):
            log_output.write(f"[WARN] while processing varations, position {index + 1} was expecting {current}, but "
                             f"found {mutable[index]}. Skipping\n")

        try:
            mutable[index] = new
            continue
        except OSError as e:
            # Fault in pyfaidx with newlines. Can circumvent this by modifying 2 chars, but depends on the location
            if index % 60 == 1 and index > 0:
                # use the character before
                mutable[index - 1 : index + 1] = str(mutable[index - 1]) + new
                continue

            if index % 60 == 0 and index + 1 < len(mutable):
                mutable[index:index + 1] = new + str(mutable[index + 1])
                continue

            # hail mary
            try:
                mutable[index - 1 : index + 1] = str(mutable[index - 1]) + new
                continue
            except:
                pass
            try:

                mutable[index:index + 1] = new + str(mutable[index + 1])
                continue
            except:
                pass

            # rip in peace
            log_output.writable(f"Fatal Error. While processing {sid}_{cid}_{gid} unable to modify {current} to {new} "
                                "at position {index + 1} due to a bug in pyfaidx with single characters but my "
                                "workaround didn't work.\n")

            raise e




    # Same subsections of each file
    # Unclear what to do with ranges here - For now assume to just concatenate everything
    output_file = output_root / f"{cid}_{sid}_{gid}.fa"
    with open(output_file, 'w') as f:
        f.write(f">{record.name}\n")
        temp = ""
        for subset in ranges:
            for i in range(subset.start, subset.stop):
                temp += str(record[i])
                if len(temp) % 61 == 60:
                    #60th character, + new lines before it
                    temp += "\n"
        if (temp[-1] != "\n"):
            temp += "\n"
        temp += "\n"
        f.write(temp)
    # done?
    fasta.close()

def main():
    # Load input arguments

    parser = argparse.ArgumentParser("ava", description="Allele Variance Applicator")

    parser.add_argument("--input", "-i", type=ValidFolder, help="Folder with all the input .csv and .fasta files",
                        default='.')
    parser.add_argument("--config", '-c', type=ValidFile, help="Configuration/metadata file with regions of interest",
                        required=True)
    parser.add_argument("--output", "-o", type=ValidOutput, help="Folder for all output files to go. Ensure this is not "
                        "the input folder", required=True)

    args = parser.parse_args()
    input_path: pathlib.Path = args.input
    cfg_path: pathlib.Path = args.config
    output_path: pathlib.Path = args.output
    log_file_path = output_path / "output.log"


    # Recursively get relavant files
    input_sequences: List[pathlib.Path] = [file for file in input_path.glob("**/*.fasta")]
    input_sequences += [file for file in input_path.glob("**/*.fa")]
    input_variances: List[pathlib.Path]  = [file for file in input_path.glob("**/*.csv")]

    if (not len(input_sequences)):
        print("No input files found. Ensure there are .fasta or .fa files in the input folder")
        exit(errno.ENOENT)

    if (not len(input_variances)):
        print("No variance files were found. Ensure there are .csv files in the input folder")
        exit(errno.ENOENT)

    if cfg_path.suffix != ".csv":
        print("Expecting a CSV file for the configuration file")
        exit(errno.EBADF)

    # Check output exists
    if not output_path.exists():
        output_path.mkdir()

    log_file = open(log_file_path, 'w')
    # Load a list of all genes, Chromosomes and Samples
    chromosomes = load_sequences(input_sequences)
    cfg = load_config(cfg_path)
    compact_cfg = {cid: {gid for gid, pos in values.items()} for cid, values in cfg.items()}
    variants = load_variants(input_variances, cfg_path, compact_cfg, log_file)

    # convert every permutation in variants to a big list
    operations: List[Tuple[Sid, Cid, Gid, List[range], Dict[int, Tuple[str, str]]], FastaRecord] = []

    temp_files: Dict[str, FastaRecord] = {}

    print("Performing preprocessing")
    for sid, sid_data in variants.items():
        for cid, cid_data in sid_data.items():
            if cid not in chromosomes:
                log_file.write(f"[WARN] gene {gid} was not found in sequences when trying to process "
                                f"{cid}_{sid}_{gid}.\n")
                continue

            for gid, gid_data in cid_data.items():
                # Get the range data from the

                if cid not in cfg or gid not in cfg[cid]:
                    log_file.write(f"[WARN] output ranges for {cid}_{sid}_{gid} could not be found in the metadata file"
                                   ".\n")
                    continue

                operations.append((sid, cid, gid, cfg[cid][gid], gid_data,
                                   pathlib.Path(chromosomes[cid][cid]._fa.filename)))

    if not len(operations):
        log_file.write(f"Insufficient data. No output files could be created\n")
    log_file.close()

    # Process the variations
    with Pool() as pool:
        args = [(output_path, data, log_file_path) for data in operations]
        # it = pool.map(process_variations_compat, args)
        # for data in tqdm(operations, desc="Preparing output files:"):
            # sid, cid, gid, ranges, variations, record = data
            # process_variations((output_path, args, log_file))
        for _ in tqdm(pool.imap_unordered(process_variations_compat, args), total=len(args)):
            pass
        # for item in tqdm(it, desc="Preparing output files:"):
        #     pass

    # Clean up cache files
    files_to_remove: List[pathlib.Path] = []

    files_to_remove += [file for file in input_path.glob("**/*.fasta.fai")]
    files_to_remove += [file for file in input_path.glob("**/*.fa.fai")]

    files_to_remove += [file for file in output_path.glob("**/*_temp.fa")]
    files_to_remove += [file for file in output_path.glob("**/*_temp.fa.fai")]

    for file in tqdm(files_to_remove, desc="Cleaning up: "):
        file.unlink()

    print(f"Output to {output_path} complete. Check log at {log_file_path} for more details")

if __name__ == "__main__":
    main()