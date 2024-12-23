# agcd-csiro

This repository contains scripts for creating a replica of CSIRO's commercially licensed version of the AGCD dataset on NCI.

The commercially licensed AGCD dataset is located at `/datasets/work/af-cdp/work/agcd/` on CSIRO's high performance computing cluster called Petrichor.
(The full catalogue for the Digiscape Climate Data Portal is [here](https://data-cbr.it.csiro.au/thredds/catalog/catch_all/Digiscape_Climate_Data_Portal/catalog.html).)

The AGCD data that CSIRO purchases comes from the Bureau of Meteorology (BoM) FTP server feed.
Any retrospective adjustments made to the AGCD dataset by the BoM have not been picked up in CSIRO's version since 2018.
It is not clear what the relationship is between the FTP data available for purchase from the BoM
and the research-only snapshots of the AGCD dataset that the BoM makes available on NCI
(see https://dx.doi.org/10.25914/6009600304b02).
Basic analysis performed by CSIRO scientists indicates that there are minor but not major
differences between the purchased FTP data and the research-only snapshots on NCI.
As far as we are aware there is no formal citation for the FTP data.
This [BoM catalogue page](http://www.bom.gov.au/metadata/catalogue/19115/ANZCW0503900567) lists a broken DOI
and refers to a CC-BY-NC licence (i.e. non-commercial, which is technically not what CSIRO has purchased).

The replica data is located at `/g/data/xv83/agcd-csiro/` on NCI.

## Daily data

### Data transfer

The data transfer scripts/commands need to be run from Petrichor.

The transfer of the daily historical data files was done using the transfer script:
```
$ ssh csiro_username@petrichor.hpc.csiro.au
$ git clone https://github.com/AusClimateService/agcd-csiro.git
$ cd agcd-csiro
$ bash transfer_agcd-historical_daily.sh {variable} {nci_username} {nci_password}
```

The latest daily data (updated daily) can be transferred using scp. e.g.
```
$ scp /datasets/work/af-cdp/work/agcd/climate/tmax.nc nci_username@gadi.nci.org.au:/g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20180209-20220402_daily.nc
```

### Data processing

The latest data has some issues (e.g. duplication of time steps) and
overlaps in time with the historical data.

These issues can be addressed by running the processing script on NCI:

```
$ cd /g/data/xv83/agcd-csiro/replica-code
$ git pull origin main
$ python process_current.py /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20180209-20220402_daily.nc tmax /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20190101-20191231_daily.nc /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20200101-20201231_daily.nc /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20210101-20211231_daily.nc /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20220101-20220402_daily.nc
$ rm /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_20180209-20220402_daily.nc
```

### Rechunking

```
$ python to_rechunked_zarr.py /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_*_daily.nc tmax /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_19100101-20220402_daily_time-chunked.zarr /g/data/xv83/agcd-csiro/tmax/daily/tmax_AGCD-CSIRO_r005_19100101-20220402_daily_space-chunked.zarr /g/data/xv83/agcd-csiro/tmax/daily/temporary.zarr
```

## Monthly data

There's no historical data included in the commercially licensed AGCD dataset.
A research-only copy of the monthly historical data (up to mid-2020) is available on NCI in project zv2
(`/g/data/zv2/agcd/v2/precip/total/r005/01month`).

The latest monthly data (from 2020 or late 2019 onwards) is available as part of the commercial dataset
for precipitation, tmax and tmin (there's no monthly vapour pressure data).

### Data transfer

The data transfer commands need to be run from Petrichor:
```
scp /datasets/work/af-cdp/work/agcd/tmax/data/IDCKZX1A90_tmax_mean_r005_*.nc nci_username@gadi.nci.org.au:/g/data/xv83/agcd-csiro/tmax/monthly
scp /datasets/work/af-cdp/work/agcd/tmin/data/IDCKZN1A90_tmin_mean_r005_*.nc nci_username@gadi.nci.org.au:/g/data/xv83/agcd-csiro/tmin/monthly
scp /datasets/work/af-cdp/work/agcd/precip/data/IDCK2R1AT0_precip_total_r005_*.nc nci_username@gadi.nci.org.au:/g/data/xv83/agcd-csiro/precip/monthly
```

For the precipitation data it looks like `IDCK2R1AT0` is v2 and `IDCKZR1AT0` is v1,
although when comparing against the data in zv2 the values aren't exactly the same.
(See `precip_comparison.ipynb` for details.)

### Data processing

The files then simply need to be merged using cdo. For example:
```
cdo mergetime /g/data/xv83/agcd-csiro/tmax/monthly/IDCKZX1A90_tmax_mean_r005_2021*.nc /g/data/xv83/agcd-csiro/tmax/monthly/agcd_v1_tmax_mean_r005_monthly_2021.nc
```

