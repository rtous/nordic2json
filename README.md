# nordic2json

## Installing the package locally

From the root of the github repo:

	pip install .

## Testing

	util_bigsfile2sfiles --bigsfile_path input/arrival_times.txt --output_path  output/sfiles_nordicformat

	nordic2json \
	--input_path output/sfiles_nordicformat \
	--output_path output/catalog.json
