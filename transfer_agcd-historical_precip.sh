# Transfer historical AGCD precipitation data from Petricor to Gadi
#
# Usage: $ bash transfer_agcd-historical_precip.sh {nci_username} {nci_password}

nci_username=$1
nci_password=$2

for year in $(seq 1900 2018); do 
	echo ${year}
        csirofile=/datasets/work/af-cdp/work/agcd/HISTORICAL/daily-rainfall/merged/${year}.nc
	ncifile=/g/data/xv83/agcd-csiro/precip/precip-total_AGCD-CSIRO_r005_${year}0101-${year}1231_daily.nc
	sshpass -p ${nci_password} scp ${csirofile} ${nci_username}@gadi.nci.org.au:${ncifile}
done
