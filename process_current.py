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
   

def insert_date_dashes(date):
    """Convert YYYYMMDD to YYYY-MM-DD."""

    assert len(date) == 8
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    
    return f'{year}-{month}-{day}'
 

def parse_date_range(filename):
    """Extract dates from filename"""

    date_range = filename.split('_')[3]
    start_date, end_date = date_range.split('-')
    start = insert_date_dashes(start_date)
    end = insert_date_dashes(end_date)

    return start, end


def main(args):
    """Run the command line program."""

    in_ds = xr.open_dataset(args.infile)
    in_ds['lat'].attrs['standard_name'] = 'latitude'
    in_ds['lon'].attrs['standard_name'] = 'longitude'
    try:
        in_ds = in_ds.drop('crs')
    except ValueError:
        pass
    try:
        in_ds[args.var].attrs.pop('grid_mapping')
    except KeyError:
        pass

    for outfile in args.outfiles:
        print(outfile)
        start_time, end_time = parse_date_range(outfile)
        out_ds = in_ds.sel(time=slice(start_time, end_time))
        out_ds = out_ds.compute()
        out_ds = out_ds.drop_duplicates('time')
        duplicate_time_check(out_ds['time'])
        out_ds.attrs['history'] = cmdprov.new_log(
            infile_logs={args.infile: in_ds.attrs['history']})
        out_ds.to_netcdf(outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infile", type=str, help="Input file")
    parser.add_argument("var", type=str, help="Variable")
    parser.add_argument("outfiles", nargs='*', type=str,
                        help="Output file in {var}_AGCD-CSIRO_{grid}_YYYYMMDD-YYYYMMDD_{timescale}.nc")
    args = parser.parse_args()
    main(args)
    
