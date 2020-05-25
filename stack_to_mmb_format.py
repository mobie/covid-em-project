import argparse
import os

# NOTE: I will refactor this into https://github.com/platybrowser/mmb-python eventually
from mmpb.release_helper import add_version, make_folder_structure
from mmpb.files.xml_utils import write_s3_xml
from mmb_utils import export_image_stack, initialize_image_dict, initialize_bookmarks

ROOT = './data'
DEFAULT_CHUNKS = (64, 64, 64)


def add_xml_for_s3(xml_path, data_path):
    bucket_name = 'covid-fib-sem'
    xml_out_path = xml_path.replace('local', 'remote')

    path_in_bucket = os.path.relpath(data_path, start=ROOT)
    write_s3_xml(xml_path, xml_out_path, path_in_bucket,
                 bucket_name=bucket_name)

    print("In order to add the data to the EMBL S3, please run the following command:")
    full_s3_path = f'embl/{bucket_name}/{path_in_bucket}'
    mc_command = f"mc cp -r {os.path.relpath(data_path)}/ {full_s3_path}/"
    print(mc_command)


# FIXME if this is called multiple times, it will replicate fields in the xml
def stack_to_mmb(input_folder, dataset_name, resolution, chunks, target, max_jobs, time_limit):
    assert os.path.exists(input_folder), input_folder

    # @Martin, this is small, no reason to put it on scratch (where I don't have write permissions)
    tmp_folder = 'tmp_%s' % dataset_name

    # create output folder structure
    output_folder = os.path.join(ROOT, dataset_name)
    make_folder_structure(output_folder)

    # convert tif stack to bdv.n5 format
    # NOTE: the file name still needs to be in the platy naming scheme.
    # @Tischi and me need to update this eventually
    out_path = os.path.join(output_folder, 'images', 'local', 'sbem-6dpf-1-whole-raw.n5')

    # TODO we should also compute a foreground/background mask
    # @julian, we could just use what you are doing to invert the bg values
    # then we could also do the inversion on the fly here

    export_image_stack(input_folder, out_path, tmp_folder,
                       resolution, chunks,
                       target=target, max_jobs=max_jobs,
                       time_limit=time_limit)

    xml_path = os.path.splitext(out_path)[0] + '.xml'
    add_xml_for_s3(xml_path, out_path)

    # initialize the image dict and bookmarks
    initialize_image_dict(output_folder, xml_path)
    initialize_bookmarks(output_folder)

    # register this stack in versions.json
    add_version(dataset_name, ROOT)
    print("You also need to add the files in", output_folder, "to git")


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
    parser.add_argument('--chunks', type=int, nargs=3, default=DEFAULT_CHUNKS)
    parser.add_argument('--target', type=str, default='local')
    parser.add_argument('--max_jobs', type=int, default=16)
    parser.add_argument('--time_limit', type=int, default=60, help="Time limit in minutes")

    args = parser.parse_args()
    resolution = get_resolution(args.resolution, args.name)
    print("Resolution:", resolution)
    stack_to_mmb(args.input_folder, args.name, resolution, args.chunks,
                 args.target, args.max_jobs, args.time_limit)
