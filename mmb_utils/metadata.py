import json
import os


def initialize_image_dict(folder, xml_path):
    assert os.path.exists(xml_path), xml_path

    image_folder = os.path.join(folder, 'images')
    image_dict_path = os.path.join(image_folder, 'images.json')

    raw_name = os.path.splitext(os.path.split(xml_path)[1])[0]
    rel_path = os.path.relpath(xml_path, image_folder)

    image_dict = {
        raw_name: {
            "color": "white",
            "contrastLimits": [0., 255.],
            "storage": {
                "local": rel_path,
                "remote": rel_path.replace("local", "remote")
            },
            "type": "image"
        }
    }

    with open(image_dict_path, 'w') as f:
        json.dump(image_dict, f, indent=2, sort_keys=True)


def initialize_bookmarks(folder):
    bookmark_folder = os.path.join(folder, 'misc', 'bookmarks')
    os.makedirs(bookmark_folder, exist_ok=True)
    bookmark_path = os.path.join(bookmark_folder, 'default.json')

    bkmrk = {
        'layers': {
            'fibsem-raw': {
                'contrastLimits': [0., 255.]
            }
        }
    }

    with open(bookmark_path, 'w') as f:
        json.dump(bkmrk, f, indent=2, sort_keys=True)


def add_dataset(name, root):
    path = os.path.join(root, 'datasets.json')
    with open(path) as f:
        datasets = json.load(f)
    datasets['datasets'].append(name)
    with open(path, 'w') as f:
        json.dump(datasets, f, sort_keys=True, indent=2)
