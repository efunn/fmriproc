import numpy as np
from mvpa2.suite import *

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
