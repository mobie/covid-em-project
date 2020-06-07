import argparse
import os

from mobie import add_segmentation
from stack_to_mmb_format import add_xml_for_s3

ROOT = './data'
DEFAULT_CHUNKS = (64, 64, 64)


def add_seg_to_dataset(input_path, dataset_name, segmentation_name,
                       resolution, chunks, target, max_jobs):

    # TODO what's the input key
    input_key = ''
    scale_factors = 6 * [[2, 2, 2]]

    add_segmentation(input_path, input_key,
                     ROOT, dataset_name, segmentation_name,
                     resolution, scale_factors, chunks,
                     target=target, max_jobs=max_jobs,
                     add_default_table=True)

    # convert tif stack to bdv.n5 format
    dataset_folder = os.path.join(ROOT, dataset_name)
    out_path = os.path.join(dataset_folder, 'images', 'local', f'{segmentation_name}.n5')
    xml_path = os.path.splitext(out_path)[0] + '.xml'
    add_xml_for_s3(xml_path, out_path)
    print("You also need to add the files in", dataset_folder, "to git")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str)
    parser.add_argument('dataset_name', type=str)
    parser.add_argument('segmentation_name', type=str)
    parser.add_argument('--resolution', type=float, nargs=3, default=None)
    parser.add_argument('--chunks', type=int, nargs=3, default=DEFAULT_CHUNKS)
    parser.add_argument('--target', type=str, default='local')
    parser.add_argument('--max_jobs', type=int, default=16)

    args = parser.parse_args()
    add_seg_to_dataset(args.input_path, args.dataset_name, args.segmentation_name,
                       args.resolution, args.chunks, args.target, args.max_jobs)
