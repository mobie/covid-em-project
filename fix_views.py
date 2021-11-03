import json
import os
from subprocess import run

import mobie


def fix_views_ds(ds):
    ds_folder = os.path.join("./data", ds)
    mdata = mobie.metadata.read_dataset_metadata(ds_folder)

    sources = mdata["sources"]
    for name, source in sources.items():
        stype = list(source.keys())[0]
        menu_name = "em" if stype == "image" else "segmentation"
        if ds == "Covid19-S5-mock-Cell1-2" and stype == "segmentation":
            view = mobie.metadata.get_default_view(stype, name, menu_name=menu_name,
                                                   tables=["default.tsv", "color_scheme_fibsem.tsv"],
                                                   colorByColumn="figuresColorScheme",
                                                   lut="argbColumn")
        elif ds == "Covid19-S4-Area2" and stype == "segmentation":
            view = mobie.metadata.get_default_view(stype, name, menu_name=menu_name, tables=["default.tsv"])
        else:
            view = mobie.metadata.get_default_view(stype, name, menu_name=menu_name)
        mobie.metadata.add_view_to_dataset(ds_folder, name, view, overwrite=True)

    if ds == "Covid19-S5-mock-Cell1-2":
        url = "https://raw.githubusercontent.com/mobie/covid-em-project/master/data/Covid19-S5-mock-Cell1-2/misc/bookmarks/bookmarks.json"
    elif ds == "Covid19-S4-Area2":
        url = "https://raw.githubusercontent.com/mobie/covid-em-project/master/data/Covid19-S4-Area2/misc/bookmarks/bookmarks.json"
    else:
        url = None

    if url is not None:
        run(["wget", url, "-O", "bookmarks.json"])
        with open("./bookmarks.json") as f:
            trafos = json.load(f)
        for name, trafo in trafos.items():
            params = [float(tt[1:]) for tt in trafo["normView"]]
            view = {
                "viewerTransform": mobie.metadata.get_viewer_transform(normalized_affine=params),
                "isExclusive": False,
                "uiSelectionGroup": "bookmark"
            }
            mobie.metadata.add_view_to_dataset(ds_folder, name, view, overwrite=True)
        os.remove("./bookmarks.json")


def fix_all_views():
    ds_names = mobie.metadata.get_datasets("./data")
    for ds in ds_names:
        fix_views_ds(ds)


fix_all_views()


# https://github.com/mobie/covid-em-project/blob/master/data/Covid19-S4-Area2/misc/bookmarks/bookmarks.json
# https://github.com/mobie/covid-em-project/blob/master/data/Covid19-S5-mock-Cell1-2/misc/bookmarks/bookmarks.json
