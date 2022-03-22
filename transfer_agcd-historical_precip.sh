# Transfer historical AGCD precipitation data from Petricor to Gadi
#
# Usage: $ bash transfer_agcd-historical_precip.sh {csiro_username} {nci_username} {nci_password}

csiro_username=$1
nci_username=$2
nci_password=$3

tempdir=/scratch2/${csiro_username}/temp
mkdir -p ${tempdir}
rm -f ${tempdir}/*.nc
for year in $(seq 1900 2016); do 
	echo ${year}
	outfile=${tempdir}/precip-total_AGCD-CSIRO_r005_${year}_daily.nc
	for infile in /datasets/work/af-cdp/work/agcd/HISTORICAL/daily-rainfall/${year}/*.nc; do
		tempfile=`echo ${infile} | rev | cut -d '/' -f 1 | rev`
		cdo selname,precip ${infile} ${tempdir}/${tempfile}
	done
	command="cdo -O -f nc4 mergetime ${tempdir}/*.nc ${outfile}"
	echo ${command}
	${command}
	sshpass -p ${nci_password} scp ${outfile} ${nci_username}@gadi.nci.org.au:/g/data/xv83/agcd-csiro/precip/
	rm -f ${tempdir}/*.nc
done
