"""Process AGCD current data file."""

import argparse

import numpy as np
import xarray as xr
import cmdline_provenance as cmdprov


def duplicate_time_check(time_da):
    """Check the number of days spanned by a time array.

    Args:
       time_da (xarray DataArray) : Array of numpy datetime64 objects
    """

    length_of_time = time_da.values[-1] - time_da.values[0]    
    expected_ndays = np.timedelta64(length_of_time, 'D').astype(int) + 1
    actual_ndays = len(time_da)
    assert expected_ndays == actual_ndays, "There are duplicate times"
    

def main(args):
    """Run the command line program."""

    ds = xr.open_dataset(args.infile)
    if args.start_date:
        ds = ds.sel(time=slice(args.start_date, None))
    ds = ds.compute()
    ds = ds.drop_duplicates('time')
    #ds = ds.sel(time=~ds.get_index('time').duplicated())
    duplicate_time_check(ds['time'])
    ds.attrs['history'] = cmdprov.new_log(
        infile_logs={args.infile: ds.attrs['history']})
    ds.to_netcdf(args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infile", type=str, help="Input file")
    parser.add_argument("outfile", type=str, help="Output file")
    parser.add_argument("--start_date", type=str, default=None, help="Start date for outfile in YYYY-MM-DD format")
    args = parser.parse_args()
    main(args)
    
