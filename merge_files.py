"""Merge files and remove duplicate times."""

import pdb
import argparse
from datetime import date

import xarray as xr
import cmdline_provenance as cmdprov


def check_ntimes():
    """Make sure there are no duplicate times"""
    
    f_date = date(2014, 7, 2)
    l_date = date(2014, 7, 11)
    delta = l_date - f_date
    print(delta.days)


def main(args):
    """Run the command line program."""

    ds = xr.open_mfdataset(args.infiles, concat_dim='time')
    pdb.set_trace()
    ds = ds.drop_duplicates('time')
    ds.attrs['history'] = cmdprov.new_log()
    #ds = ds.chunk({'time': args.chunk_size})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infiles", type=str, nargs='*', help="Input netCDF files")
    parser.add_argument("outfile", type=str, help="Output file name (must end in .zarr.zip)")
    #parser.add_argument("--chunk_size", type=int, default=50,
    #                    help="Size of time axis chunks for writing output file")
    args = parser.parse_args()
    main(args)
    
