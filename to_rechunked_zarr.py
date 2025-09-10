"""Take a dataset and produce two zarr collections chunked along the temporal and spatial axis respectively."""

import os
import argparse
import logging

import xarray as xr
from rechunker import rechunk
import dask.diagnostics
import zarr
import cmdline_provenance as cmdprov


dask.diagnostics.ProgressBar().register()
logging.basicConfig(level=logging.INFO)


def define_target_chunks(ds, var):
    """Create a target chunks dictionary."""

    if 'latitude' in ds[var].dims:
        chunks = {'time': len(ds['time']), 'latitude': 10, 'longitude': 10}
    else:
        chunks = {'time': len(ds['time']), 'lat': 10, 'lon': 10}
    target_chunks_dict = {var: chunks}
    variables = list(ds.keys())
    variables.remove(var)
    coords = list(ds.coords.keys())
    for name in coords + variables:
        target_chunks_dict[name] = None

    return target_chunks_dict


def main(args):
    """Run the command line program."""

    ds = xr.open_mfdataset(args.infiles)
    ds = ds.chunk({'time': 365})
    if not os.path.isdir(args.temporal_chunked_collection):
        ds.attrs['history'] = cmdprov.new_log(
            infile_logs={args.infiles[0]: ds.attrs['history']}
        )
        for var in ds.variables:
            ds[var].encoding = {}
        logging.info('Writing the temporal chunked collection...')
        ds.to_zarr(args.temporal_chunked_collection)
        zarr.consolidate_metadata(args.temporal_chunked_collection)

    source_group = zarr.open(args.temporal_chunked_collection)
    target_chunks_dict = define_target_chunks(ds, args.var)
    max_mem = '1GB'
    group_plan = rechunk(
        source_group,
        target_chunks_dict,
        max_mem,
        args.spatial_chunked_collection,
        temp_store=args.temp_collection
    )
    logging.info('Writing the spatial chunked collection...')
    group_plan.execute()
    zarr.consolidate_metadata(args.spatial_chunked_collection)

    clean_up_command = f'rm -r {args.temp_collection}'
    logging.info(clean_up_command)
    os.system(clean_up_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infiles", type=str, nargs='*', help="Input files")
    parser.add_argument("var", type=str, help="Variable")
    parser.add_argument("temporal_chunked_collection", type=str, help="Path to temporal chunked zarr collection")
    parser.add_argument("spatial_chunked_collection", type=str, help="Path to spatial chunked zarr collection")
    parser.add_argument("temp_collection", type=str, help="Temporary zarr collection")
    args = parser.parse_args()
    main(args)
    
