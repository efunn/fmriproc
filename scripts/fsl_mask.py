import os
import subprocess, shlex
import fsl_align as fa

default_fsldir = '/usr/local/fsl'
FSLDIR = os.getenv('FSLDIR', default_fsldir)

def run_bash(cmd):
    cmd_line = shlex.split(cmd)
    subprocess.call(cmd_line)


def select_roi_mask(roi_name='Primary motor cortex BA4p L',
                    atlas='Juelich',
                    atlas_spec = '-prob-1mm',
                    out_img = '/path/to/out.nii.gz'):
    atlas_dir = FSLDIR + '/data/atlases/' + atlas + '.xml'
    atlas_img = (FSLDIR + '/data/atlases/' + atlas
                 + '/' + atlas + atlas_spec + '.nii.gz')
    cmd = (os.getcwd() + '/scripts/process/select_roi_mask.sh -r \"'
           + roi_name + '\" -a '
           + atlas_dir + ' -i ' + atlas_img + ' -o ' + out_img)
    run_bash(cmd)


def thresh(in_img,
           out_img,
           thr='0.5'):
    cmd = ('fslmaths ' + in_img + ' -thr ' + thr
           + ' ' + out_img)
    run_bash(cmd)


def thresh_bin(in_img,
               out_img,
               thr='0.5'):
    cmd = ('fslmaths ' + in_img + ' -thr ' + thr 
           + ' -bin ' + out_img)
    run_bash(cmd)


def add_mask(in_mask_1,
             in_mask_2,
             out_mask):
    cmd = ('fslmaths ' + in_mask_1 + ' -add '
           + in_mask_2 + ' -bin ' + out_mask)
    run_bash(cmd)

def sub_mask(in_mask_1,
             in_mask_2,
             out_mask):
    cmd = ('fslmaths ' + in_mask_1 + ' -sub '
           + in_mask_2 + ' -bin ' + out_mask)
    run_bash(cmd)


def extract_roi(in_img,
                out_txt,
                in_mask):
    cmd = (os.getcwd() + '/scripts/process/extract_roi.sh -i ' + in_img
           + ' -o ' + out_txt
           + ' -m ' + in_mask)
    run_bash(cmd)

def fs_extract_brain(rai_img,
                     subj_id,
                     subj_dir):
    # need to add -all (or other directives here?)
    fs_cmd = ('recon-all -i ' + rai_img
              + '.nii -subjid ' + subj_id
              + ' -sd ' + subj_dir)
    run_bash(fs_cmd)

def gen_all_masks(dirs, roi_names):
    # set reference ROI names (in Juelich probability maps)
    for area,name in roi_names.iteritems():
        select_roi_mask(roi_name=name,
                        out_img=dirs['ref'] + '/' + area + '_std')

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

    thresh = 20
    for area,name in roi_names.iteritems():
        base_roi = (dirs['ref'] + '/' + area)
        fa.apply_align(base_roi + '_std',
                       base_roi + '_rfi',
                       align_mat=(dirs['ref']+'/std2rfi.mat'),
                       ref_img=dirs['rfi'])
        fm.thresh_bin(base_roi + '_rfi',
                      base_roi,
                      thr=thresh)

    # add logic to 
    # base_roi = (dirs['ref'] + '/')
    # fm.add_mask(base_roi + 'v1_l',
    #             base_roi + 'v1_r',
    #             base_roi + 'v1')
    
    # base_roi = (dirs['ref'] + '/')
    # fm.add_mask(base_roi + 'v1_l_fov',
    #             base_roi + 'v1_r_fov',
    #             base_roi + 'v1_fov')

def proc_rois(dirs):
    # set reference ROI names (in Juelich probability maps)
    roi_names = {'v1_l': 'Visual cortex V1 BA17 L',
                 'v1_r': 'Visual cortex V1 BA17 R',
                 'v2_l': 'Visual cortex V2 BA18 L',
                 'v2_r': 'Visual cortex V2 BA18 R'}
    for area,name in roi_names.iteritems():
        select_roi_mask(roi_name=name,
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

    thresh = 20
    for area,name in roi_names.iteritems():
        base_roi = (dirs['ref'] + '/' + area)
        fa.apply_align(base_roi + '_std',
                       base_roi + '_rfi',
                       align_mat=(dirs['ref']+'/std2rfi.mat'),
                       ref_img=dirs['rfi'])
        fm.thresh_bin(base_roi + '_rfi',
                      base_roi,
                      thr=thresh)

    base_roi = (dirs['ref'] + '/')
    fm.add_mask(base_roi + 'v1_l',
                base_roi + 'v1_r',
                base_roi + 'v1')
    
    base_roi = (dirs['ref'] + '/')
    fm.add_mask(base_roi + 'v1_l_fov',
                base_roi + 'v1_r_fov',
                base_roi + 'v1_fov')
