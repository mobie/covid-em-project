# covid-em

## Set-up

I have set up a conda environment with all necessary dependencies in `software/miniconda`.
You can activate it by running:
```shell
source software/run_conda.sh
conda activate covid-em-dev
```


## Usage

Use the `stack_to_mmb_format.py` script to convert a folder with tiff slices into the MMB format:
```shell
python stack_to_mmb_format.py /path/to/folder/with/tiffs name
```

## Opening the dataset in MMB

In order to load one of the data-sets in the MMB, you need to [use the CustomBrowser option](https://github.com/platybrowser/mmb-fiji#advanced-options).
To load the data on the EMBL share, you need to give `/g/emcf/common/5792_Sars-Cov-2/covid-em/data` both for the `Image Data Location` and `Table Data Location`.
To load the remote version, you need to give the following address: `https://git.embl.de/pape/covid-em/-/raw/master/data` AND store your S3 credentials in the correct way.


## Reference

For more details on the MMB data format, see https://github.com/platybrowser/platybrowser and https://github.com/platybrowser/mmb-python.
