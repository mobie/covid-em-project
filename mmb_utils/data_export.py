import os
import json
import luigi
from cluster_tools.downscaling import DownscalingWorkflow


def export_image_stack(input_folder, out_path, tmp_folder,
                       resolution, pattern='*.tif*',
                       target='local', max_jobs=32):
    task = DownscalingWorkflow

    config_dir = os.path.join(tmp_folder, 'configs')
    os.makedirs(config_dir, exist_ok=True)

    # TODO need to determine a good block shape and good chunks
    block_shape = []
    configs = DownscalingWorkflow.get_config()
    global_conf = configs['global']
    global_conf.update({'block_shape': block_shape})
    with open(os.path.join(config_dir, 'global.config'), 'w') as f:
        json.dump(global_conf, f)

    t = task(tmp_folder=tmp_folder, config_dir=config_dir,
             target=target, max_jobs=max_jobs)
    ret = luigi.build([t], local_scheduler=True)
    assert ret
