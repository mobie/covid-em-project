# covid-em

## Set-up

TODO set up local env with all necessary dependencies to run the scripts.


## Usage

Use the `stack_to_mmb_format.py` script to convert a folder with tiff slices into the MMB format:
```shell
python stack_to_mmb_format.py /path/to/folder/with/tiffs name
```


## Reference

For more details on the MMB data format, see https://github.com/platybrowser/platybrowser and https://github.com/platybrowser/mmb-python.
In order to load a data-set in the MMB, you need to [use the CustomBrowser option](https://github.com/platybrowser/mmb-fiji#advanced-options).
