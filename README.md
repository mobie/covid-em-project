# covid-em

Volume EM data from [Integrative imaging reveals SARS-CoV-2-induced reshaping of subcellular morphologies](https://www.sciencedirect.com/science/article/pii/S193131282030620X).

## Opening the dataset in MoBIE

In order to load one of the data-sets in MoBIE, you need to [install the MoBIE Fiji Plugin](https://github.com/mobie/mobie-viewer-fiji#install), select `Plugins->MoBIE->Open->Open MoBIE Project` and enter https://github.com/mobie/covid-em-project.
To load the data on the EMBL share, use `/g/emcf/common/5792_Sars-Cov-2/covid-em/data` instead.

## Reference

For more details on the MoBIE and the MoBIE data format, visit https://mobie.github.io/.

<!--- This is all outdated
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
-->
