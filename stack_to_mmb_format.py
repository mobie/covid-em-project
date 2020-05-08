import argparse
import os

# NOTE: I will refactor this into https://github.com/platybrowser/mmb-python eventually
from mmpb.release_helper import add_version, make_folder_structure
from mmb_utils import export_image_stack, initialize_image_dict, initialize_bookmarks

ROOT = './data'


def stack_to_mmb(input_folder, dataset_name, resolution, target, max_jobs):
    assert os.path.exists(input_folder), input_folder

    tmp_folder = './tmp_%s' % dataset_name

    # create output folder structure
    output_folder = os.path.join(ROOT, dataset_name)
    make_folder_structure(output_folder)

    # convert tif stack to bdv.n5 format
    # NOTE: the file name still needs to be in the platy naming scheme.
    # @tischi and me need to update this eventually
    out_path = os.path.join(output_folder, 'images', 'local', 'sbem-6dpf-1-whole-raw.n5')

    export_image_stack(input_folder, out_path, tmp_folder, resolution,
                       target=target, max_jobs=max_jobs)

    # initialize the image dict and bookmarks
    xml_path = os.path.splitext(out_path)[0] + '.xml'
    initialize_image_dict(output_folder, xml_path)
    initialize_bookmarks(output_folder)

    # TODO we should also compute a foreground/background mask right away like so:
    # - threshold the data at background value (0?) on suitable downsampled level
    # - compute connected components and keep only the largest background component

    # register this stack in versions.json
    add_version(dataset_name, ROOT)


# infer resolution if it was set to None
def get_resolution(resolution, name):
    if resolution is None:
        # TODO we need the exact 5nm identifier in the filename
        # if '' in name:
        #     resolution = [0.005, 0.005, 0.005]
        # else:
        #     resolution = [0.008, 0.008, 0.008]
        resolution = [0.008, 0.008, 0.008]
    return resolution


# This is the exaple path from Julian (without white-spaces now)
# /g/emcf/common/5792_Sars-Cov-2/exp_070420/FIB-SEM/alignments/20-04-23_S4_area2_Sam/align2_amst/target_cell_inv_clip
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str)
    parser.add_argument('name', type=str)
    parser.add_argument('--resolution', type=int, nargs=3, default=None)
    parser.add_argument('--target', type=str, default='local')
    parser.add_argument('--max_jobs', type=int, default=16)

    args = parser.parse_args()
    resolution = get_resolution(args.resolution, args.name)
    print("Resolution:", resolution)
    stack_to_mmb(args.input_folder, args.name, resolution, args.target, args.max_jobs)
