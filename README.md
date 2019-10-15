# nordic2json

## Installing the package locally

From the root of the github repo:

	pip install .

## Testing

### Joining multiple select.ou

	cat select2.out >> select2.out

### Filtering some things from select.out

*NOTE: This will only work if all the input entries are from the same year.*

	grep -e "2019 \|2019-\|BAUV HZ\|BENV HZ\|MAPV HZ\|TACV HZ\|\STAT\|^[[:space:]]*$" carabobo_select.out

### Splitting select.out into many single-event files


	util_bigsfile2sfiles --bigsfile_path input/arrival_times.txt --output_path  output/sfiles_nordicformat

### To JSON


	nordic2json \
	--input_path output/sfiles_nordicformat \
	--output_path output/catalog.json

	nordic2json \
	--input_path input/1_carabobo_select.out \
	--output_path output/catalog.json

PROBLEMA: linia amb el waveform/tracedate file
	
## Troubleshooting

- Need and end-of-line after the last entry in the Nordic Format filecat 
