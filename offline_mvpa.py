import scripts.fsl_align as fa
import scripts.fsl_mask as fm
import scripts.fsl_glm as fg
import numpy as np
import os
from mvpa2.suite import *


def preproc_std(base_dir='/belly/20160427-seqlearn-001',
                num_runs=6):
    # define directories
    dirs = define_dirs(base_dir, num_runs)

    # extract brain from rai 
    fm.fs_extract_brain(rai_img=dirs['rai'],
                        subj_id=dirs['fs_subj_id'],
                        subj_dir=dirs['fs_subj'])

    # motion correct middle run, bet middle run
    # then motion correct each run to rfi, then bet each run
    # proc_all_runs(dirs, num_runs)

    # epi_reg or bbregister rfi to rai
    # need field map img? how was this done before, with FSL?

def fs_proc_rois(dirs):
    ########
    # warp atlas into subject space
    ########
    sval = '/belly/staged-sim-nfb-001/ref/early-vis-areas.sym.mgh' # lh.data.sym.mgh (source)
    tval = '/belly/staged-sim-nfb-001/ref/lh.early-vis-areas.mgh' # lh.data.mgh (output)
    cmd = ('mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg'
           + ' --trgsubject ' + dirs['fs_subj_id']
           + ' --trgsurfreg fsaverage_sym.sphere.reg --hemi lh'
           + ' --sval ' + sval
           + ' --tval ' + tval)
    fa.run_bash(cmd)
    # mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg --trgsubject sim-nfb-001 --trgsurfreg fsaverage_sym.sphere.reg --hemi lh --sval /belly/staged-sim-nfb-001/ref/early-vis-areas.sym.mgh --tval /belly/staged-sim-nfb-001/ref/lh.early-vis-areas.mgh
    # mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg --trgsubject sim-nfb-001 --trgsurfreg fsaverage_sym.sphere.reg --hemi lh --sval /Dropbox/img_data/sim-nfb-001/ref/early-vis-eccen.sym.mgh --tval /Dropbox/img_data/sim-nfb-001/ref/lh.early-vis-eccen.mgh
    # mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg --trgsubject sim-nfb-001 --trgsurfreg fsaverage_sym.sphere.reg --hemi lh --sval ~/Dropbox/img_data/ref/early-vis-eccen.sym.mgh --tval ~/Dropbox/img_data/ref/lh.early-vis-eccen.mgh
    sval = '/belly/staged-sim-nfb-001/ref/early-vis-areas.sym.mgh' # rh.data.sym.mgh
    tval = '/belly/staged-sim-nfb-001/ref/rh.early-vis-areas.mgh' # rh.data.mgh
    cmd = ('mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg'
           + ' --trgsubject ' + dirs['fs_subj_id'] + '/xhemi'
           + ' --trgsurfreg fsaverage_sym.sphere.reg --hemi lh'
           + ' --sval ' + sval
           + ' --tval ' + tval)
    fa.run_bash(cmd)

    ##########
    # Freesurfer stuff - needs to get fixed
    ##########
    # mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg --trgsubject sim-nfb-001/xhemi --trgsurfreg fsaverage_sym.sphere.reg --hemi lh --sval /belly/staged-sim-nfb-001/ref/early-vis-areas.sym.mgh --tval /belly/staged-sim-nfb-001/ref/rh.early-vis-areas.mgh
    # mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg --trgsubject sim-nfb-001/xhemi --trgsurfreg fsaverage_sym.sphere.reg --hemi lh --sval ~/Dropbox/img_data/ref/early-vis-eccen.sym.mgh --tval ~/Dropbox/img_data/ref/rh.early-vis-eccen.mgh
    # mri_surf2surf --srcsubject fsaverage_sym --srcsurfreg sphere.reg --trgsubject sim-nfb-001/xhemi --trgsurfreg fsaverage_sym.sphere.reg --hemi lh --sval ~/Dropbox/img_data/ref/early-vis-eccen.sym.mgh --tval ~/Dropbox/img_data/ref/rh.early-vis-eccen.mgh
    # mri_surf2vol --surfval lh.early-vis-eccen.mgh --identity sim-nfb-001 --template rai.nii --hemi lh --o testytest.nii 
    # mri_surf2vol --surfval lh.early-vis-eccen.mgh --identity sim-nfb-001 --template rai.nii --hemi lh --o testytest.nii 
    # mri_surf2vol --surfval lh.early-vis-eccen.mgh --identity sim-nfb-001 --template rai.nii --hemi lh --o testytestytest.mgz 

    # mri_surf2vol --surfval lh.early-vis-eccen.mgh --fillribbon --identity sim-nfb-001 --template $FREESURFER_HOME/subjects/sim-nfb-001/mri/T1.mgz --hemi lh --o lh_vis_eccen.mgz 
    # mri_convert --in_type mgz --out_type nii --out_orientation RAS lh_vis_eccen.mgz lh_vis_eccen.nii.gz
    # # manual height crop here: 32 is arbitrary (figure out?)
    # fslroi lh_vis_eccen.nii.gz lh_vis_eccen_crop.nii.gz 32 192 0 256 -3 256 

    # mri_surf2vol --surfval rh.early-vis-eccen.mgh --fillribbon --identity sim-nfb-001 --template $FREESURFER_HOME/subjects/sim-nfb-001/mri/T1.mgz --hemi rh --o rh_vis_eccen.mgz 
    # mri_convert --in_type mgz --out_type nii --out_orientation RAS rh_vis_eccen.mgz rh_vis_eccen.nii.gz
    # # manual height crop here: 32 is arbitrary (figure out?)
    # fslroi rh_vis_eccen.nii.gz rh_vis_eccen_crop.nii.gz 32 192 0 256 -3 256 

    # mri_convert --in_type mgz --out_type nii --out_orientation RAS testytest.mgz testytest.nii.gz
    # mri_convert --in_type mgz --out_type nii --out_orientation RAS testytestytest.mgz testytestytest.nii.gz
    # fslroi testytest.nii.gz testytestcrop.nii.gz 35 192 0 256 0 256 

    ########
    # combining freesurfer masks
    ########
    lower_thresh = 2 
    upper_thresh = 10
    cmd = ('fslmaths lh_vis_eccen_crop -thr ' + str(lower_thresh)
           + ' -uthr ' + upper_thresh + ' -bin lh_vis_eccen_crop_thr')
    cmd = ('fslmaths rh_vis_eccen_crop -thr ' + str(lower_thresh)
           + ' -uthr ' + upper_thresh + ' -bin rh_vis_eccen_crop_thr')
    cmd = ('fslmaths lh_vis_eccen_crop_thr'
           + ' -add rh_vis_eccen_crop_thr'
           + ' -bin vis_eccen_crop_thr')


def fsl_proc_rois(dirs):
    ############
    # select crappy ROI masks
    ############
    # set reference ROI names (in Juelich probability maps)
    roi_names = {'v1_l': 'Visual cortex V1 BA17 L',
                 'v1_r': 'Visual cortex V1 BA17 R',
                 'v2_l': 'Visual cortex V2 BA18 L',
                 'v2_r': 'Visual cortex V2 BA18 R'}
    for area,name in roi_names.iteritems():
        fm.select_roi_mask(roi_name=name,
                           out_img=dirs['ref'] + '/' + area + '_std')

    ############
    # crappy fsl alignment of anatomy
    ############
    fa.gen_struct_brain(in_struct=dirs['rai'],
                        out_struct=dirs['rai']+'_brain',
                        extra_params=' -B')
    # generate std to rai
    fa.gen_struct2struct(in_struct=dirs['std'],
                         ref_struct=dirs['rai']+'_brain',
                         in_name='std',
                         ref_name='rai',
                         outdir=dirs['ref'])

    fa.gen_bold2struct(in_bold=dirs['rfi']+'_brain',
                       ref_struct=dirs['rai']+'_brain',
                       in_name='rfi',
                       ref_name='rai',
                       outdir=dirs['ref'])

    fa.add_align(align1=(dirs['ref']+'/rfi2rai.mat'),
                 align2=(dirs['ref']+'/rai2std.mat'),
                 namefirst='rfi',
                 namelast='std',
                 outdir=dirs['ref'])
    # warp rai into rfi space
    fa.apply_align(dirs['rai'],
                   dirs['rai'] + '_rfi',
                   align_mat=(dirs['ref']+'/rai2rfi.mat'),
                   ref_img=dirs['rfi'])

    ############
    # crappy fsl warping rois into functional space
    ############
    for area,name in roi_names.iteritems():
        base_roi = (dirs['ref'] + '/' + area)
        fa.apply_align(base_roi + '_std',
                       base_roi + '_rfi',
                       align_mat=(dirs['ref']+'/std2rfi.mat'),
                       ref_img=dirs['rfi'])
        fm.thresh_bin(base_roi + '_rfi',
                      base_roi,
                      thr=str(20))

    ############
    # crappy fsl add masks together
    ############
    base_roi = (dirs['ref'] + '/')
    fm.add_mask(base_roi + 'v1_l',
                base_roi + 'v1_r',
                base_roi + 'v1')
    fm.add_mask(base_roi + 'v2_l',
                base_roi + 'v2_r',
                base_roi + 'v2')
    fm.add_mask(base_roi + 'v1',
                base_roi + 'v2',
                base_roi + 'v1v2')

    #######
    # janky way to remove fovea
    #######
    
    lower_thresh = 65
    upper_thresh = 80
    for area,name in roi_names.iteritems():
        base_roi = (dirs['ref'] + '/' + area)
        fm.thresh_bin(base_roi + '_rfi',
                      base_roi + '_fov',
                      thr=str(upper_thresh))
        fm.thresh_bin(base_roi + '_rfi',
                      base_roi + '_peri',
                      thr=str(lower_thresh))
    base_roi = (dirs['ref'] + '/')
    fm.add_mask(base_roi + 'v1_l_fov',
                base_roi + 'v1_r_fov',
                base_roi + 'v1_fov')
    fm.add_mask(base_roi + 'v2_l_fov',
                base_roi + 'v2_r_fov',
                base_roi + 'v2_fov')
    fm.add_mask(base_roi + 'v1_fov',
                base_roi + 'v2_fov',
                base_roi + 'v1v2_fov')
    fm.add_mask(base_roi + 'v1_l_peri',
                base_roi + 'v1_r_peri',
                base_roi + 'v1_peri')
    fm.add_mask(base_roi + 'v2_l_peri',
                base_roi + 'v2_r_peri',
                base_roi + 'v2_peri')
    fm.add_mask(base_roi + 'v1_peri',
                base_roi + 'v2_peri',
                base_roi + 'v1v2_peri')
    fm.sub_mask(base_roi + 'v1v2_peri',
                base_roi + 'v1v2_fov',
                base_roi + 'v1v2')

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

def gen_attr(label_dict,base_labels,out_dir,len_block=16,offset=4):
    num_runs = len(base_labels)
    num_blocks = np.shape(base_labels)[1]
    out_labels = np.zeros((num_runs,
                           len_block*num_blocks))
    # out_labels = -1*np.ones((num_runs,
    #                        len_block*num_blocks))
    for run in range(num_runs):
        for block in range(num_blocks):
            begin_idx = block*len_block
            end_idx = begin_idx + len_block
            out_labels[run, begin_idx:end_idx] = base_labels[run,block]
        out_labels[run] = np.roll(out_labels[run], offset)
        with open(out_dir + '/run_' + str(run+1).zfill(3) + '_attr.txt','w') as f:
            for tr in range(len_block*num_blocks):
                chunk = run
                # if tr < (0.5*len_block*num_blocks-1):
                #     chunk = 2*run
                # else:
                #     chunk = 2*run+1
                f.write(label_dict[out_labels[run][tr]]+  ' ' + str(chunk) + '\n')


def preproc_mvpa(base_dir='/belly/staged-sim-nfb-001'):
    out_dir = base_dir + '/ref'
    label_dict = {-1: 'rest',
                  0: '0-0deg',
                  1: '1-22.5deg',
                  2: '2-45deg',
                  3: '3-67.5deg',
                  4: '4-90deg',
                  5: '5-112.5deg',
                  6: '6-135deg',
                  7: '7-157.5deg'}
    base_labels = np.array([[-1,3,5,4,0,6,2,1,7,2,7,1,3,0,5,4,6,-1],
                            [-1,6,7,5,2,1,4,0,3,2,1,5,4,0,6,3,7,-1],
                            [-1,4,0,5,2,1,7,3,6,7,3,5,0,4,6,2,1,-1],
                            [-1,2,5,0,1,7,6,4,3,5,7,6,0,4,1,2,3,-1],
                            [-1,5,0,4,3,6,2,7,1,5,4,3,1,6,0,7,2,-1],
                            [-1,6,7,2,5,4,0,1,3,5,1,6,4,3,7,0,2,-1],
                            [-1,3,0,5,1,7,4,6,2,4,3,1,7,6,2,5,0,-1],
                            [-1,7,1,2,5,3,4,6,0,5,6,3,4,0,1,7,2,-1]])

    bold_img_list = [base_dir + '/bold/run_001_mc_brain.nii.gz',
        base_dir + '/bold/run_002_mc_brain.nii.gz',
        base_dir + '/bold/run_003_mc_brain.nii.gz',
        base_dir + '/bold/run_004_mc_brain.nii.gz',
        base_dir + '/bold/run_005_mc_brain.nii.gz',
        base_dir + '/bold/run_006_mc_brain.nii.gz',
        base_dir + '/bold/run_007_mc_brain.nii.gz',
        base_dir + '/bold/run_008_mc_brain.nii.gz']

    bold_img_list_smooth = [base_dir + '/bold/run_001_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_002_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_003_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_004_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_005_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_006_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_007_mc_brain_smooth.nii.gz',
        base_dir + '/bold/run_008_mc_brain_smooth.nii.gz']
    run_data = []
    run_attrs = []
    gen_attr(label_dict,base_labels,out_dir)
    for run in range(len(bold_img_list)):
        run_attrs.append(SampleAttributes(out_dir + '/run_' + str(run+1).zfill(3) + '_attr.txt'))
        run_data.append(fmri_dataset(bold_img_list[run],
                                    targets=run_attrs[run].targets,
                                    chunks=run_attrs[run].chunks,
                                    mask=out_dir + '/vis_eccen_crop_thr_rfi_bin.nii.gz'))
                                    # mask=out_dir + '/v1v2.nii.gz'))

    ds = vstack((run_data[0],
                 run_data[1],
                 run_data[2],
                 run_data[3],
                 run_data[4],
                 run_data[5],
                 run_data[6],
                 run_data[7]))
    ds.save(out_dir + '/2deg10deg.hdf5',compression=9)
    # ds.save(out_dir + '/v1v2.hdf5',compression=9)

def preproc_mvpa_glm(base_dir='/belly/staged-sim-nfb-001'):
    out_dir = base_dir + '/ref'
    bold_img_list = [base_dir + '/ref/betas_run_001.nii.gz',
        base_dir + '/ref/betas_run_002.nii.gz',
        base_dir + '/ref/betas_run_003.nii.gz',
        base_dir + '/ref/betas_run_004.nii.gz',
        base_dir + '/ref/betas_run_005.nii.gz',
        base_dir + '/ref/betas_run_006.nii.gz',
        base_dir + '/ref/betas_run_007.nii.gz',
        base_dir + '/ref/betas_run_008.nii.gz']
    run_labels = [0,1,2,3,4,5,6,7,-1,-1]
    label_dict = {-1: 'rest',
                  0: '0-0deg',
                  1: '1-22.5deg',
                  2: '2-45deg',
                  3: '3-67.5deg',
                  4: '4-90deg',
                  5: '5-112.5deg',
                  6: '6-135deg',
                  7: '7-157.5deg'}
    base_labels = np.array([run_labels,
                            run_labels,
                            run_labels,
                            run_labels,
                            run_labels,
                            run_labels,
                            run_labels,
                            run_labels])
    run_data = []
    run_attrs = []
    gen_attr(label_dict,base_labels,out_dir,len_block=1,offset=0)
    for run in range(len(bold_img_list)):
        run_attrs.append(SampleAttributes(out_dir + '/run_' + str(run+1).zfill(3) + '_attr.txt'))
        run_data.append(fmri_dataset(bold_img_list[run],
                                    targets=run_attrs[run].targets,
                                    chunks=run_attrs[run].chunks,
                                    mask=out_dir + '/vis_eccen_crop_thr_rfi_bin.nii.gz'))
                                    # mask=out_dir + '/v1v2.nii.gz'))

    ds = vstack((run_data[0],
                 run_data[1],
                 run_data[2],
                 run_data[3],
                 run_data[4],
                 run_data[5],
                 run_data[6],
                 run_data[7]))
    ds.save(out_dir + '/glm_2deg10deg.hdf5',compression=9)
