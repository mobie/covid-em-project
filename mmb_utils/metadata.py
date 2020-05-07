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
            "Color": "White",
            "MaxValue": 255,
            "MinValue": 0,
            "Storage": {
                "local": rel_path
            },
            "Type": "Image"
        }
    }

    with open(image_dict_path, 'w') as f:
        json.dump(image_dict, f, indent=2, sort_keys=True)


def initialize_bookmarks(folder):
    bookmark_path = os.path.join(folder, 'misc', 'bookmarks.json')
    with open(bookmark_path, 'w') as f:
        json.dump({}, f)
