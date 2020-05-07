import os
import json
import luigi
from cluster_tools.downscaling import DownscalingWorkflow


def export_image_stack(input_folder, out_path, tmp_folder,
                       resolution, pattern='*.tif*',
                       target='local', max_jobs=16):
    task = DownscalingWorkflow

    config_dir = os.path.join(tmp_folder, 'configs')
    os.makedirs(config_dir, exist_ok=True)

    # TODO need to determine a good block shape and good chunks
    block_shape = [32, 2048, 2048]
    chunks = [32, 64, 64]

    configs = DownscalingWorkflow.get_config()
    global_conf = configs['global']
    global_conf.update({'block_shape': block_shape})
    with open(os.path.join(config_dir, 'global.config'), 'w') as f:
        json.dump(global_conf, f)

    conf = configs['copy_volume']
    conf.update({'chunks': chunks})
    with open(os.path.join(config_dir, 'copy_volume.config'), 'w') as f:
        json.dump(conf, f)

    conf = configs['downscaling']
    conf.update({'chunks': chunks})
    with open(os.path.join(config_dir, 'downscaling.config'), 'w') as f:
        json.dump(conf, f)

    # TODO do we sample isotropically? need to double check with the resolution
    scale_factors = [[2, 2, 2]] * 6
    halos = scale_factors
    metadata_format = 'bdv.n5'
    metadata_dict = {'resolution': resolution, 'unit': 'micrometer'}

    t = task(tmp_folder=tmp_folder, config_dir=config_dir,
             target=target, max_jobs=max_jobs,
             input_path=input_folder, input_key=pattern,
             scale_factors=scale_factors, halos=halos,
             metadata_format=metadata_format, metadata_dict=metadata_dict,
             output_path=out_path)
    ret = luigi.build([t], local_scheduler=True)
    assert ret
