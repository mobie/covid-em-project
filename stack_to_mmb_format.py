import argparse
import os

# NOTE: I will refactor this into https://github.com/platybrowser/mmb-python eventually
from mmpb.release_helper import add_version, make_folder_structure
from mmb_utils import export_image_stack, initialize_image_dict, initialize_bookmarks

ROOT = './data'


def stack_to_mmb(input_folder, stack_name, target, max_jobs):
    assert os.path.exists(input_folder), input_folder

    tmp_folder = './tmp_%s' % stack_name

    # create output folder structure
    output_folder = os.path.join(ROOT, stack_name)
    make_folder_structure(output_folder)

    # convert tif stack to bdv.n5 format
    # NOTE: the file name still needs to be in the platy naming scheme.
    # @tischi and me need to update this eventually
    out_path = os.path.join(output_folder, 'images', 'local', 'sbem-6dpf-1-whole-raw.n5')

    # TODO need resolution information
    resolution = [1, 1, 1]
    export_image_stack(input_folder, out_path, tmp_folder, resolution,
                       target=target, max_jobs=max_jobs)

    # initialize the image dict and bookmarks
    xml_path = os.path.splitext(out_path)[0] + '.xml'
    initialize_image_dict(output_folder, xml_path)
    initialize_bookmarks(output_folder)

    # register this stack in versions.json
    add_version(stack_name, ROOT)


# This is the exaple path from Julian (without white-spaces now)
# /g/emcf/common/5792_Sars-Cov-2/exp_070420/FIB-SEM/alignments/20-04-23_S4_area2_Sam/align2_amst/target_cell_inv_clip
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str)
    parser.add_argument('name', type=str)
    parser.add_argument('--target', type=str, default='local')
    parser.add_argument('--max_jobs', type=int, default=16)

    args = parser.parse_args()
    stack_to_mmb(args.input_folder, args.name, args.target, args.max_jobs)
