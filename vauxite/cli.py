"""Console script for vauxite."""
import sys
import click

from vauxite.vauxite import *
from vauxite.ipfs import pull_from_ipfs
from vauxite.packages import run_on_package


# parameter-group aliases for our most common data types


def alias_illumina(ctx):
    ctx.params['layout'] = Layout.PAIRED
    ctx.params['allocation'] = Allocation.ASSOCIATED
    ctx.params['level'] = Level.READS

def alias_grasp(ctx):
    ctx.params['layout'] = Layout.PAIRED
    ctx.params['allocation'] = Allocation.INTERLEAVED
    ctx.params['level'] = Level.READS

def alias_nanopore(ctx):
    ctx.params['layout'] = Layout.HAIRPIN
    ctx.params['allocation'] = Allocation.DISTRIBUTED
    ctx.params['level'] = Level.READS

def alias_fasta(ctx):
    ctx.params['layout'] = Layout.SINGLE
    ctx.params['allocation'] = Allocation.MERGED
    ctx.params['level'] = Level.CONTIGS


def alias_callback(ctx, param, value):
    "Click callback function to set bundle of flags if an alias flag is used."
    return {'illumina':alias_illumina,
            'grasp':alias_grasp,
            'nanopore':alias_nanopore,
            'fasta':alias_fasta}.get(value, lambda c: None)

def alias(flag, flag_value, help):
    return click.option(flag, '_', flag_value=flag_value, help=help, callback=alias_callback, expose_value=False)


@click.group()
def main():
    "Vauxite is a tool for managing and running in-silico typing schemes on sequencing data."
    pass

@main.command()
@click.argument('package')
@click.argument('files', nargs=-1)
@click.option('-p', '--paired', 'layout', flag_value=Layout.PAIRED)
@click.option('-s', '--single', 'layout', flag_value=Layout.SINGLE)
@click.option('--layout', 'layout', type=click.Choice(list(Layout.choices()), case_sensitive=False))
@click.option('--arrangement', 'allocation', type=click.Choice(list(Allocation.choices()), case_sensitive=False))
@click.option('--fasta', 'level', flag_value=Level.CONTIGS)
@click.option('--assembly-level', 'level', type=click.Choice(list(Level.choices()), case_sensitive=False))
@click.option('-n', '--name', 'name')
@alias('--illumina', 'illumina', 'paired-end short-read sequencing in associated files')
@alias('--grasp', 'grasp', 'paired-end short-read sequencing in interlaced single file')
@alias('--nanopore', 'nanopore', 'hairpin long-read sequencing in distributed files')
@alias('--fasta', 'fasta', 'contig assembly in single file')
def run(package, files, layout=None, allocation=None, level=None, name=None):
    "Run the specified package on a series of files. Describe the format and layout of sequencing in the file using options."
    pack_path = pull(package)
    if not any(layout, allocation, level):
        data = FileArrangement.sniff(files, layout_hint=layout, allocation_hint=allocation, level_hint=level, name_hint=name)
    else:
        if not name:
            name = FileArrangement.impute_name(files)
        data = FileArrangement(layout, allocation, level, name [Path(fi) for fi in files])
    run_on_package(pack_path, data)
    

@main.command(name='list')
def _list():
    "List the available typing packages."
    pass

@main.command()
@click.argument('package')
def pull(package):
    "Pull a typing package to local storage."
    return pull_from_ipfs(package)

@main.command()
@click.argument('package_path')
@click.argument('package')
def push(package_path, package):
    "Push a typing package into the IPFS network."
    return push_to_ipfs(package_path, name=package)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
