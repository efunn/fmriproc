import scripts.fsl_glm as fg
import os, yaml
from tqdm import *
import numpy as np

def proc_all_runs(ref_dir='/belly/staged-sim-nfb-001', num_runs=8):
    with open('offline_glm_config.yaml') as f:
        config = yaml.load(f)
        config['design'][0]['length'] = config['num_vols']
    for run in tqdm(range(num_runs)):
        proc_run(ref_dir, run, config)

def proc_run(base_dir, run_num, config):
    # - need to make these specific per run
    #   e.g. (loc_design, tstats, loc_img, betas)
    run_str = str(run_num+1).zfill(3)
    proc_dirs = {}
    proc_dirs['ref'] = base_dir + '/ref'
    proc_dirs['rai_img'] = proc_dirs['ref'] + '/rai'
    proc_dirs['rfi_img'] = proc_dirs['ref'] + '/rfi'
    proc_dirs['loc_img'] = (base_dir + '/bold/run_'
                            + run_str + '_mc_brain_smooth')
    proc_dirs['tstats_img'] = proc_dirs['ref'] + '/tstats_run_' + run_str
    proc_dirs['betas_img'] = proc_dirs['ref'] + '/betas_run_' + run_str

    #   use convert_design_to_run to turn loc_design into expected format
    # - need to make loc_design go run-by-run
    # - run_glm right now cannot take an arbitrary # of regressors
    loc_design = convert_design_to_run(config['design'], run_num)
    tr = config['tr']
    fg.run_glm(proc_dirs,
               loc_design,
               tr)


def convert_design_to_run(all_runs_design, run_num):
    run_design_subset = all_runs_design[run_num]
    single_run_design = []
    for label in np.unique(run_design_subset['labels']):
        single_run_design.append({})
        single_run_design[-1]['onsets'] = run_design_subset['onsets']
        single_run_design[-1]['label'] = str(label)
        single_run_design[-1]['durations'] = run_design_subset['durations']
        single_run_design[-1]['heights'] = 1*(
            np.equal(run_design_subset['labels'],label))
    single_run_design[0]['length'] = all_runs_design[0]['length']
    return single_run_design
