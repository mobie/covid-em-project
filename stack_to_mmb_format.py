import argparse
import os

from mobie import initialize_dataset
from mobie.xml_utils import copy_xml_as_n5_s3

ROOT = './data'
DEFAULT_CHUNKS = (64, 64, 64)


def add_xml_for_s3(xml_path, data_path):
    bucket_name = 'covid-fib-sem'
    xml_out_path = xml_path.replace('local', 'remote')
    path_in_bucket = os.path.relpath(data_path, start=ROOT)
    copy_xml_as_n5_s3(xml_path, xml_out_path,
                      service_endpoint='https://s3.embl.de',
                      bucket_name=bucket_name,
                      path_in_bucket=path_in_bucket,
                      authentication='Protected')

    print("In order to add the data to the EMBL S3, please run the following command:")
    full_s3_path = f'embl/{bucket_name}/{path_in_bucket}'
    mc_command = f"mc cp -r {os.path.relpath(data_path)}/ {full_s3_path}/"
    print(mc_command)


# FIXME if this is called multiple times, it will replicate fields in the xml
def stack_to_mmb(input_folder, dataset_name, resolution, chunks,
                 target, max_jobs, time_limit, is_default):
    assert os.path.exists(input_folder), input_folder

    # TODO need to make these settable if we want to add anisotropic data
    raw_name = 'fibsem-raw'
    scale_factors = 6 * [[2, 2, 2]]

    initialize_dataset(input_folder, '*.tif', ROOT,
                       dataset_name, raw_name,
                       resolution, chunks, scale_factors,
                       is_default=is_default, target=target,
                       max_jobs=max_jobs, time_limit=time_limit)

    dataset_folder = os.path.join(ROOT, dataset_name)
    out_path = os.path.join(dataset_folder, 'images', 'local', f'{raw_name}.n5')
    xml_path = os.path.splitext(out_path)[0] + '.xml'
    add_xml_for_s3(xml_path, out_path)
    print("You also need to add the files in", dataset_folder, "to git")


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
    parser.add_argument('--resolution', type=float, nargs=3, default=None)
    parser.add_argument('--chunks', type=int, nargs=3, default=DEFAULT_CHUNKS)
    parser.add_argument('--target', type=str, default='local')
    parser.add_argument('--max_jobs', type=int, default=16)
    parser.add_argument('--time_limit', type=int, default=60, help="Time limit in minutes")
    parser.add_argument('--is_default', type=int, default=0)

    args = parser.parse_args()
    resolution = get_resolution(args.resolution, args.name)
    print("Resolution:", resolution)
    stack_to_mmb(args.input_folder, args.name, resolution, args.chunks,
                 args.target, args.max_jobs, args.time_limit, bool(args.is_default))
