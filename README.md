# nordic2json

## About this repository

*CURRENT STATUS: This repository has been discontinued. The current tools provided by the ObsPy library to parse Nordic files on the one hand, and to manipulate seismic catalogs on the other hand, makes it unnecessary to convert the catalogs into JSON.*

This repository provides tools to convert a file formatted in Nordic into a JSON file with a simplified structure. It is a (deprecated) component of the UPC-UCV project, related to the application of deep neural networks to the automated analysis of seismograms. More specifically, this repository is part of the preprocessing tools, used to generate the datasets to train and test the models. The repository was originally created because of the lack of convenient tools to deal with seismic catalogs in Nordic format, typically obtained from [SEISAN](https://www.geosig.com/files/GS_SEISAN_9_0_1.pdf), the seismic analysis software suite. 

## Functionality



## Prerequisites

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

