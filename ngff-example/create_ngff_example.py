import os
import subprocess

import mobie
import pandas as pd
from elf.io import open_file
from elf.io.ngff import write_ome_zarr


def _to_ngff(path, key, out_path, is_seg=False):
    with open_file(path, 'r') as f:
        ds = f[key]
        ds.n_threads = 8
        data = ds[:]
    scale = (0.5,) * 3
    if is_seg:
        kwargs = {"scale": scale, "order": 0, "preserve_range": True}
    else:
        kwargs = {"scale": scale, "order": 3, "preserve_range": True, "anti_aliasing_sigma": 1.}
    name = "segmentation" if is_seg else "raw"
    write_ome_zarr(data, out_path, name=name, n_scales=3, kwargs=kwargs)


def convert_to_ngff():
    raw_path = '../data/Covid19-S4-Area2/images/local/sbem-6dpf-1-whole-raw.n5'
    raw_key = 'setup0/timepoint0/s3'
    out_path = './data/S4-Area2/images/raw.ome.zarr'
    _to_ngff(raw_path, raw_key, out_path)

    seg_path = '../data/Covid19-S4-Area2/images/local/s4_area2_segmentation.n5'
    seg_key = 'setup0/timepoint0/s3'
    out_path = './data/S4-Area2/images/segmentation.ome.zarr'
    _to_ngff(seg_path, seg_key, out_path, is_seg=True)


def create_folders():
    os.makedirs('./data/S4-Area2/images', exist_ok=True)
    os.makedirs('./data/S4-Area2/tables/segmentation', exist_ok=True)


def copy_table():
    in_table = '../data/Covid19-S4-Area2/tables/s4_area2_segmentation/default.csv'
    out_table = './data/S4-Area2/tables/segmentation/default.tsv'
    table = pd.read_csv(in_table)
    table = table[1:]
    table.to_csv(out_table, sep='\t', index=False)


def create_metadata():
    pass


def upload():
    pass


def create_ngff_example():
    create_folders()
    convert_to_ngff()
    copy_table()

    create_metadata()
    upload()


if __name__ == '__main__':
    create_ngff_example()
