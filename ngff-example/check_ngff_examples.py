import argparse
import os
from glob import glob

import napari
import zarr


# should open pyramid view instead
def check_example(ff):
    if ff.startswith('flat'):
        store = zarr.storage.DirectoryStore(ff)
    else:
        store = zarr.storage.NestedDirectoryStore(ff)

    with zarr.open(store, mode='r') as f:
        data = f['s0'][:]

    with napari.gui_qt():
        v = napari.Viewer()
        v.title = ff
        v.add_image(data)


def main(folder):
    files = glob(os.path.join(folder, "*.ome.zarr"))
    for ff in files:
        check_example(ff)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument_group('folder')
    args = parser.parse_args()
    main(args.folder)
