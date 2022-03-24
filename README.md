# agcd-csiro

This repository contains scripts for creating a replica of CSIRO's commercially licensed version of the AGCD dataset on NCI.

The commercially licensed AGCD dataset is located at `/datasets/work/af-cdp/work/agcd/` on Petrichor.
The replica data is located at `/g/data/xv83/agcd-csiro/` on NCI.

## Data transfer

The data transfer scripts/commands need to be run from Petrichor.

The transfer of the historical data files was done using the transfer script:
```
$ ssh csiro_username@petrichor.hpc.csiro.au
$ git clone https://github.com/AusClimateService/agcd-csiro.git
$ cd agcd-csiro
$ bash transfer_agcd-historical_precip.sh nci_username nci_password
```

The latest data (updated daily) can be transferred using scp. e.g.
```
$ scp /datasets/work/af-cdp/work/agcd/climate/precip.nc nci_username@gadi.nci.org.au:/g/data/xv83/agcd-csiro/precip/precip-total_AGCD-CSIRO_r005_20171111-20220322_daily.nc
```

### Data processing

The latest data has some issues (e.g. duplication of time steps) and
overlaps in time with the historical data.

These issues can be addressed by running the processing script on NCI:

```
$ cd /g/data/xv83/agcd-csiro/replica-code
$ git pull origin main
$ python process_current.py /g/data/xv83/agcd-csiro/precip/precip-total_AGCD-CSIRO_r005_20171111-20220322_daily.nc /g/data/xv83/agcd-csiro/precip/precip-total_AGCD-CSIRO_r005_20190101-20220322_daily.nc --start_date 2019-01-01
$ rm /g/data/xv83/agcd-csiro/precip/precip-total_AGCD-CSIRO_r005_20171111-20220322_daily.nc
```
