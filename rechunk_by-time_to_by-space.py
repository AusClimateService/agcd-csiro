"""Take dataset chunked along time axis and rechunk along spatial axes."""

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


def main(args):
    """Run the command line program."""

    ds = xr.open_mfdataset(args.infiles)
    ds = ds.chunk({'time': 365})
    assert not os.path.isdir(args.time_chunked_collection), \
        f"You need to delete existing zarr collection: {args.time_chunked_collection}"
    ds.attrs['history'] = cmdprov.new_log(
        infile_logs={args.infiles[0]: ds.attrs['history']}
    )
    for var in ds.variables:
        ds[var].encoding = {}
    logging.info('Writing the time chunked collection...')
    ds.to_zarr(args.time_chunked_collection)

    source_group = zarr.open(args.time_chunked_collection)
    source_array = source_group[args.var]
    target_chunks_dict = {'time': len(ds['time']), 'lat': 10, 'lon': 10}
    #target_chunks_dict = {
    #    args.var: {'time': len(ds['time']), 'lat': 10, 'lon': 10},
    #    'time': None,
    #    'lon': None,
    #    'lat': None,
    #    'time_bnds': None,
    #    'lon_bnds': None,
    #    'lat_bnds': None,
    #}
    max_mem = '1GB'
    array_plan = rechunk(
        source_array,
        target_chunks_dict,
        max_mem,
        args.space_chunked_collection,
        temp_store=args.temp_collection
    )
    logging.info('Writing the space chunked collection...')
    array_plan.execute()

    clean_up_command = f'rm -r {args.temp_collection}'
    logging.info(clean_up_command)
    os.system(clean_up_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infiles", type=str, nargs='*', help="Input files")
    parser.add_argument("var", type=str, help="Variable")
    parser.add_argument("time_chunked_collection", type=str, help="Path to time chunked zarr collection")
    parser.add_argument("space_chunked_collection", type=str, help="Path to space chunked zarr collection")
    parser.add_argument("temp_collection", type=str, help="Temporary zarr collection")
    args = parser.parse_args()
    main(args)
    
