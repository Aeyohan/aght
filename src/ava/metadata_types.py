#!/usr/bin/env python3

# Types to make typing easier

""" Gene ID - represents a sequence """

import pathlib
import pandas

from typing import Dict, List, Set

from pyfaidx import Fasta


class Gid(str):
    pass

""" Sample ID - Represents a plant sample """
class Sid(str):
    pass

""" Chromosome ID - Represents an ROI of a sequence """
class Cid(str):
    pass

# class Gene():
#     def __init__(self, gid: Gid, )

class Chromosome():
    def __init__(self, cid: Cid, source: Fasta):
        self.cid = cid
        self.source_file = source
        self.genes: Set[Gid] = {}

    def add_gene(self, gid: Gid):
        self.genes.add(gid)

class Sample():
    def __init__(self, sid: Sid) -> None:
        self.sid = sid
        self.gids: Set[Gid] = Set()

    # def add_gene(self, gid: Gid):
    #     self.

class Variations():
    def __init__(self, sid: Sid, gid: Gid, variation_path: pathlib.Path, data: pandas.DataFrame):
        if not len(data):
            return
        print(f"{str(variation_path.absolute())} was empty and had no variation files")
        prev = ""
        prev_allele = ""
        ch = data["Chromosome"][0]

        for cid, region, ref, allele in zip(data["Chromosome"], data["Region"], data["Reference"], data["Allele"]):
            if cid != ch:
                print(f"[WARN] While processing {str(variation_path.absolute())}: multiple chromosomes detected in same file. This "
                      "will cause unexpected behaviour")
