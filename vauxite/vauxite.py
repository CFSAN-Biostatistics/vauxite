"""Main module."""

from frozendict import frozendict

from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import List

class Choice:
    @classmethod
    def choices(cls):
        for member in cls.__members__:
            yield member.lower()

@unique
class Layout(Choice, Enum):
    "Sequencing strategy"

    SINGLE="single" # reads are a single amplicon sequenced from one end
    PAIRED="paired" # reads are a single amplicon sequenced from both ends towards the center
    MATE="mate-pair" # reads are a single amplicon sequenced from the center outwards
    HAIRPIN="hairpin" # reads are a single amplicon sequenced in both orientations with a hairpin center

    @classmethod
    def get_default_layout_flags(cls):
        return frozendict({
            cls.SINGLE:'s',
            cls.PAIRED:'p',
            cls.MATE:'m'
        })

@unique
class Allocation(Choice, Enum):
    "File layout strategy"

    INTERLEAVED="interleaved" # paired reads follow each other in a single file
    ASSOCIATED="associated" # paired reads in separate files, paired by ordinality
    MERGED="merged" # read pairs are merged into single reads in a single file
    DISTRIBUTED="distributed"  # reads are collected in separate files for storage reasons but aren't otherwise ordered

@unique
class Level(Choice, Enum):
    "Degree of assembly"

    READS="reads" # sequence data is unassembled
    CONTIGS="contigs" # sequence data has been partially assembled into contiguous regions
    REPLICONS="replicons" # sequence data has been fully assembled, representing replicating molecules


@dataclass
class FileArrangement:
    layout: Layout
    allocation: Allocation
    level: Level
    name: str
    paths: List[Path]


    def as_arguments(self, 
                     with_ordinal=False, 
                     starting_at=1, 
                     with_layout=False, 
                     layout=Layout.get_default_layout_flags()
                     ):
        "Return a string that represents this dataset according to the CLI of a tool"
        pass

    def as_streams(self):
        "Yield open file handles for the files, uncompressed as necessary"
        pass

    @classmethod
    def sniff(cls, paths, layout_hint=None, allocation_hint=None, level_hint=None):
        "Try to determine the layout from the files given."
        pass

    @classmethod
    def impute_name(cls, paths):
        "Try to impute a sample name from important parts of the path and file"
        pass

    def __post_init__(self):
        "Check for existence of paths when we create the arrangement."
        exists = {path.name:path.exists() for path in self.paths}
        if not all(exists.values()):
            raise ValueError(f"Files not found:{'\t'.join([n for n,v in exists.items() if not v])}")


