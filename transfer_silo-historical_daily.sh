# Transfer daily historical SILO data from Petricor to Gadi
#
# Usage: $ bash transfer_silo-historical_daily.sh {variable} {nci_username} {nci_password}

variable=$1
nci_username=$2
nci_password=$3

if [ "${variable}" == "radiation" ]; then
    start_year=1959
fi

for year in $(seq ${start_year} 2023); do 
    echo ${year}
    csirofile=/datasets/work/af-cdp/work/silo/${variable}/${year}.${variable}.nc
    ncifile=/g/data/xv83/agcd-silo/${variable}/daily/${variable}_SILO-CSIRO_r005_${year}0101-${year}1231_daily.nc
    sshpass -p ${nci_password} scp ${csirofile} ${nci_username}@gadi.nci.org.au:${ncifile}
done
