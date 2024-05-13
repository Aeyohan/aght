import pathlib
import pandas
from pyfaidx import Fasta

def parse_variant_compat(variant_path: pathlib.Path, info, log_output):
    name = variant_path.name
    gid = None
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

    # Get the variation data
    prev_region = ""
    prev_allele = ""
    variances = {}

    for cid, region, ref, allele in zip(data["Chromosome"], data["Region"], data["Reference"], data["Allele"]):
        if (cid != ch):
            log_output.write(f"[WARN] While processing {str(variant_path.absolute())}: multiple chromosomes detected in"
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

        variances[int(region) -1 ] = (ref, allele)

    return (sid, ch, gid, variances)

def process_variations_compat(args):
    output_root, data, log_output_path = args
    log_output = open(log_output_path, 'a')
    # Create a temp file and copy the contents of
    sid, cid, gid, ranges, variations, record_path = data
    record = Fasta(record_path)[cid]
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
    ext_name = f"{cid}_{sid}_{gid}"
    output_file = output_root / f"{ext_name}.fa"
    with open(output_file, 'w') as f:
        f.write(f">{ext_name}\n")
        temp = ""
        for subset in ranges:
            for i in range(subset.start, subset.stop):
                temp += str(mutable[i])
                if len(temp) % 61 == 60:
                    #60th character, + new lines before it
                    temp += "\n"
        if (temp[-1] != "\n"):
            temp += "\n"
        temp += "\n"
        f.write(temp)
    # done?
    fasta.close()