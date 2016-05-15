import scripts.fsl_glm as fg
import os, yaml

def run_loc(subdir):
    with open('config.yaml') as f:
        config = yaml.load(f)
        config['fsldir'] = os.getenv('FSLDIR', '/usr/local/fsl')
        config['design'][0]['length'] = config['epi_vols']['loc']

    roi_masks = config['rois']
    loc_design = config['design']
    tr = config['epi_tr']
    proc_dirs = {}
    proc_dirs['ref'] = '/home/rewire/offline_loc/' + subdir
    proc_dirs['rai_img'] = proc_dirs['ref'] + '/rai'
    proc_dirs['rfi_img'] = proc_dirs['ref'] + '/rfi'
    proc_dirs['loc_img'] = proc_dirs['ref'] + '/bold'
    proc_dirs['tstats_img'] = proc_dirs['ref'] + '/tstats'
    proc_dirs['betas_img'] = proc_dirs['ref'] + '/betas'
    proc_dirs['serve_betas'] = proc_dirs['ref']

    fg.run_glm(proc_dirs,
               loc_design,
               tr)

    fg.show_glm(proc_dirs,
                roi_masks)

    fg.extract_betas(proc_dirs,
                     loc_design,
                     roi_masks)
