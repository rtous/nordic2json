# nordic2json

## About this repository

*CURRENT STATUS: This repository has been discontinued. The current tools provided by the ObsPy library to parse Nordic files on the one hand, and to manipulate seismic catalogs on the other hand, makes it unnecessary to convert the catalogs into JSON.*

This repository provides tools to convert a file formatted in Nordic into a JSON file with a simplified structure. It is a (deprecated) component of the UPC-UCV project, related to the application of deep neural networks to the automated analysis of seismograms. More specifically, this repository is part of the preprocessing tools, used to generate the datasets to train and test the models. The repository was originally created because of the lack of convenient tools to deal with seismic catalogs in Nordic format, typically obtained from [SEISAN](https://www.geosig.com/files/GS_SEISAN_9_0_1.pdf), the seismic analysis software suite. 

## Functionality

The repository is designed to provide a command line tool (nordic2json). With simply running "pip install ." from the root of the repository the command "nordic2json" will be available. This is accomplished through the [Command Line Scripts(https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html) functionality of the python native packaging consisting on:

- Place the python package within a directory of the repo root directory (including the __init__.py file).
- Include a setup.py file at the root of the repo specifying the scripts. 
- Place the python scripts within a bin directory of the repo root directory. They should include the "#!/usr/bin/env python" header.

## Prerequisites

The repository has been created with Python 3.7 and has not been tested with previous versions.

It is convenient to activate a python virtual environment before installing the package:

	python3 -m venv VirtualEnvs/myVirtualEnv
	source VirtualEnvs/myVirtualEnv/bin/activate


## Installation

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

