import os

import mobie
import pandas as pd
from elf.io import open_file
from elf.io.ngff import write_ome_zarr
from pybdv.metadata import _write_xml_metadata, validate_attributes


DS_NAME = 'Covid19-S4-Area2'


def _to_ngff(path, key, out_path, is_seg=False):
    if os.path.exists(out_path):
        return

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


def _write_xml(data_path, name, resolution, shape):
    xml_path = data_path.rstrip('.ome.zarr') + '.xml'
    print(xml_path)
    if os.path.exists(xml_path):
        return xml_path
    attributes = validate_attributes(xml_path, {'channel': {'id': None}}, 0, False)
    _write_xml_metadata(xml_path, data_path,
                        unit='micrometer', resolution=resolution,
                        format_type='ome.zarr', shape=shape,
                        setup_id=0, timepoint=0, setup_name=name,
                        affine=None, attributes=attributes,
                        overwrite=False, overwrite_data=False, enforce_consistency=False)
    return xml_path


def _to_bdv_ome_zarr(in_path, in_key, out_path, name):
    with open_file(in_path, 'r') as f:
        shape = f[in_key].shape
    resolution = (0.008, 0.008, 0.008)
    resolution = [res * 2 ** 3 for res in resolution]
    return _write_xml(out_path, name, resolution, shape)


def convert_to_ngff(file_format):
    sources = {}
    views = {}

    raw_path = '../data/Covid19-S4-Area2/images/local/sbem-6dpf-1-whole-raw.n5'
    raw_key = 'setup0/timepoint0/s3'
    out_path = f'./data/{DS_NAME}/images/{file_format}/raw.ome.zarr'
    _to_ngff(raw_path, raw_key, out_path)
    if file_format == 'bdv.ome.zarr':
        xml_path = _to_bdv_ome_zarr(raw_path, raw_key, out_path, 'raw')
        sources["raw"] = mobie.metadata.get_image_metadata(f"./data/{DS_NAME}", xml_path, file_format)
        views["raw"] = mobie.metadata.get_default_view('image', 'raw', 'sbem')
        views["default"] = views["raw"]
    else:
        assert False

    seg_path = '../data/Covid19-S4-Area2/images/local/s4_area2_segmentation.n5'
    seg_key = 'setup0/timepoint0/s3'
    out_path = f'./data/{DS_NAME}/images/{file_format}/segmentation.ome.zarr'
    _to_ngff(seg_path, seg_key, out_path, is_seg=True)
    if file_format == 'bdv.ome.zarr':
        _to_bdv_ome_zarr(seg_path, seg_key, out_path, 'segmentation')
        sources["segmentation"] = mobie.metadata.get_segmentation_metadata(
            f"./data/{DS_NAME}", xml_path,
            table_location=f"./data/{DS_NAME}/tables/segmentation",
            file_format=file_format
        )
        views["segmentation"] = mobie.metadata.get_default_view(
            'segmentation', 'segmentation', 'sbem-segmentation'
        )
    else:
        assert False

    return sources, views


def create_folders(file_formats):
    mobie.metadata.create_project_metadata('./data', file_formats=file_formats)
    mobie.metadata.create_dataset_structure('./data', DS_NAME, file_formats)


def copy_table():
    in_table = '../data/Covid19-S4-Area2/tables/s4_area2_segmentation/default.csv'
    table_dir = f'./data/{DS_NAME}/tables/segmentation'
    os.makedirs(table_dir, exist_ok=True)
    out_table = os.path.join(table_dir, 'default.tsv')
    table = pd.read_csv(in_table)
    table = table[1:]
    table.to_csv(out_table, sep='\t', index=False)


def create_ngff_example(file_format='bdv.ome.zarr'):
    assert file_format in ('bdv.ome.zarr',)
    # TODO support the version without bdv xml
    # assert file_format in ('bdv.ome.zarr', 'ome.zarr')

    # create_folders([file_format])
    # copy_table()
    sources, views = convert_to_ngff(file_format)
    mobie.metadata.create_dataset_metadata(
        f"./data/{DS_NAME}",
        views=views,
        sources=sources
    )


# TODO
def upload_example():
    pass


if __name__ == '__main__':
    create_ngff_example()
