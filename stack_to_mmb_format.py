import argparse
import os

# NOTE: I will refactor this into https://github.com/platybrowser/mmb-python eventually
from mmb_utils import export_image_stack


# TODO expose target and max-jobs
def stack_to_mmb(input_folder, target='local', max_jobs=32):
    assert os.path.exists(input_folder)
    stack_name = os.path.split(input_folder)[1]
    stack_name = stack_name.replace(' ', '_')  # no spaces in names ...

    # TODO
    # create output folder structure
    output_folder = os.path.join('./data', stack_name)

    # convert tif stack to bdv.n5 format
    # NOTE: the file name still needs to be in the platy naming scheme.
    # @tischi and me need to update this eventually
    out_path = os.path.join(output_folder, 'images', 'local', 'sbem-6dpf-1-whole-raw.n5')
    # TODO need resolution information
    export_image_stack(input_folder, out_path, target=target, max_jobs=max_jobs)

    # TODO
    # register this stack in versions.json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str)
    args = parser.parse_args()
    stack_to_mmb(args.input_folder)
