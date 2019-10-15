# nordic2json

Currently ObsPy parses Nordic file format into its own, quite complete, objets model. So, it's not necessary anymore to develop neither a Nordic format parser nor a objects model.

## Installing the package locally

From the root of the github repo:

	pip install .

## Testing

### Filtering some things from select.out

*NOTE: This will only work if all the input entries are from the same year.*

	grep -e "2019 \|2019-\|BAUV HZ\|BENV HZ\|MAPV HZ\|TACV HZ\|\STAT\|^[[:space:]]*$" carabobo_select.out

### To JSON

	nordic2json \
	--input_path input/select1.out input/select2.out \
	--output_path output/catalog.json

TODO: 
	- If not applying the grep filtering for the stations, what will happen?
	- Discard all this and directly work with ObsPy data model?
	
## Troubleshooting

- Need and end-of-line after the last entry in the Nordic Format filecat 

## Legacy

Joining multiple select.out:

	cat select2.out >> select2.out

Splitting a Nordic Format into many:

	util_bigsfile2sfiles --bigsfile_path input/arrival_times.txt --output_path  output/sfiles_nordicformat

