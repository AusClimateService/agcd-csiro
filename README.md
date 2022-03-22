# agcd-csiro

This repository contains scripts for creating a replica of CSIRO's commercially licensed version of the AGCD dataset on NCI.

The commercially licensed AGCD dataset is located at `/datasets/work/af-cdp/work/agcd/` on Petrichor.
The replica data is located at `/g/data/xv83/agcd-csiro/` on NCI.

The scripts need to be run from Petrichor, e.g.
```
$ ssh csiro_username@petrichor.hpc.csiro.au
$ git clone https://github.com/AusClimateService/agcd-csiro.git
$ cd agcd-csiro
```

### Precipitation

The historical precipitation data (1900-2016) can be replicated by running the following on Petrichor:
```
$ module load cdo
$ bash transfer_agcd-historical_precip.sh {csiro_username} {nci_username} {nci_password}
```

To replicate the very latest AGCD data (2017-now, updated daily), run the following on Petrichor:
```
$ scp /datasets/work/af-cdp/work/agcd/climate/precip.nc nci_username@gadi.nci.org.au:/g/data/xv83/agcd-csiro/precip-total_AGCD-CSIRO_r005_2017-2022_daily.nc
```
