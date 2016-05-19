import os
import subprocess, shlex

def run_bash(cmd):
    cmd_line = shlex.split(cmd)
    subprocess.call(cmd_line)

def extract_brain(rai_img,
                  subj_id,
                  subj_dir):
    # need to add -all (or other directives here?)
    fs_cmd = ('recon-all -i ' + rai_img
              + '.nii -subjid ' + subj_id
              + ' -sd ' + subj_dir)
    run_bash(fs_cmd)

def proc_rois(dirs):
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
    run_bash(cmd)
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
    run_bash(cmd)

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
    