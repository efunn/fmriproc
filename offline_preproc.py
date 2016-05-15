import scripts.fsl_align as fa
import scripts.fsl_mask as fm
import scripts.fsl_glm as fg
import scripts.freesurfer_preproc as fp
import numpy as np
import os

def preproc_std(base_dir='/belly/20160427-seqlearn-001',
                num_runs=6):
    # define directories
    dirs = define_dirs(base_dir, num_runs)

    # extract brain from rai 
    fp.fs_extract_brain(rai_img=dirs['rai'],
                        subj_id=dirs['fs_subj_id'],
                        subj_dir=dirs['fs_subj'])

    # motion correct middle run, bet middle run
    # then motion correct each run to rfi, then bet each run
    proc_all_runs(dirs, num_runs)

    # epi_reg or bbregister rfi to rai
    # need field map img? how was this done before, with FSL?

def gen_masks_seqlearn(base_dir='/belly/20160427-seqlearn-001'):
    dirs = define_dirs(base_dir, 6)
    roi_names = {'m1a_l': 'Primary motor cortex BA4a L',
                 'm1a_r': 'Primary motor cortex BA4a R',
                 'm1p_l': 'Primary motor cortex BA4p L',
                 'm1p_r': 'Primary motor cortex BA4p R',
                 'pmd_l': 'Premotor cortex BA6 L',
                 'pmd_r': 'Premotor cortex BA6 R'}
    fm.gen_all_masks(dirs, roi_names)

def define_dirs(base_dir, num_runs):
    dirs = {'ref': base_dir + '/ref',
            'rfi': base_dir + '/ref/rfi',
            'rai': base_dir + '/ref/rai',
            'bold': base_dir + '/bold',
            'fs': base_dir + '/ref/fs',
            'fsl': os.getenv('FSLDIR', '/usr/local/fsl'),
            'fs_home': os.getenv('FREESURFER_HOME'),
            'fs_subj': os.getenv('SUBJECTS_DIR'),
            'fs_subj_id': base_dir.rsplit('/')[-1],
            'run': []}
    dirs['std'] = dirs['fsl'] + '/data/standard/MNI152_T1_1mm_brain'
    for i in range(num_runs):
        dirs['run'].append(dirs['bold'] + '/run_' + str(i+1).zfill(3))
    return dirs

def proc_mid_run(dirs, num_runs):
    mid_run = int((num_runs-1)/2)
    run_base = dirs['run'][mid_run]
    fa.gen_bold_mc(run_base,
                   run_base + '_mc',
                   ref_bold='none')
    fa.gen_bold_mean(run_base + '_mc',
                     dirs['rfi'])
    fa.gen_bold_4d_brain(run_base + '_mc',
                         run_base + '_mc_brain')
    fa.gen_bold_mean(run_base + '_mc_brain',
                     dirs['rfi']+'_brain')

def proc_all_runs(dirs, num_runs):
    proc_mid_run(dirs, num_runs)
    mid_run = int((num_runs-1)/2)
    for run in range(num_runs):
        if run != mid_run:
            run_base = dirs['run'][run]
            fa.gen_bold_mc(run_base,
                           run_base + '_mc',
                           ref_bold=dirs['rfi'])
            fa.gen_bold_4d_brain(run_base + '_mc',
                                 run_base + '_mc_brain')

def smooth_all_runs(dirs, num_runs, fwhm=5):
    for run in range(num_runs):
        run_base = dirs['run'][run]
        fa.smooth_bold(run_base + '_mc_brain',
                       run_base + '_mc_brain_smooth',
                       fwhm)

