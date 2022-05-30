# Transfer daily historical AGCD data from Petricor to Gadi
#
# Usage: $ bash transfer_agcd-historical_daily.sh {variable} {nci_username} {nci_password}

variable=$1
nci_username=$2
nci_password=$3

if [ "${variable}" == "precip" ]; then
        vardir="daily-rainfall"
	start_year=1900
elif [ "${variable}" == "tmax" ]; then
        vardir="daily-temperature/maximum-temperature"
	start_year=1910
elif [ "${variable}" == "tmin" ]; then
        vardir="daily-temperature/minimum-temperature"
	start_year=1910
elif [ "${variable}" == "vp-9am" ]; then
        vardir="daily-vapour-pressure/vp-9am"
	start_year=1971
elif [ "${variable}" == "vp-3pm" ]; then
        vardir="daily-vapour-pressure/vp-3pm"
	start_year=1971
fi

for year in $(seq ${start_year} 2018); do 
	echo ${year}
        csirofile=/datasets/work/af-cdp/work/agcd/HISTORICAL/${vardir}/merged/${year}.nc
	ncifile=/g/data/xv83/agcd-csiro/${variable}/daily/${variable}_AGCD-CSIRO_r005_${year}0101-${year}1231_daily.nc
	sshpass -p ${nci_password} scp ${csirofile} ${nci_username}@gadi.nci.org.au:${ncifile}
done
