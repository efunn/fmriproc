#################
# working mvpa here
#################
from mvpa2.suite import *
basedir = '/belly/staged-sim-nfb-001/ref'
ds = h5load(basedir + '/2deg10deg.hdf5')
ds = h5load(basedir + '/glm_2deg10deg.hdf5')
# ds = h5load(basedir + '/v1v2.hdf5')

poly_detrend(ds, polyord=1, chunks_attr='chunks')
zscore(ds, chunks_attr='chunks')
ds = ds[ds.sa.targets != 'rest']
averager = mean_group_sample(['targets', 'chunks'])
ds_avg = ds.get_mapped(averager)

clf = LinearCSVMC()
cvte = CrossValidation(clf, NFoldPartitioner(),
                       errorfx=lambda p, t: np.mean(p == t),
                       enable_ca=['stats']) 
cv_results = cvte(ds)
print cvte.ca.stats.as_string(description=True)

clf_avg = LinearCSVMC()
cvte_avg = CrossValidation(clf_avg, NFoldPartitioner(),
                       errorfx=lambda p, t: np.mean(p == t),
                       enable_ca=['stats']) 
cv_results = cvte_avg(ds_avg)
print cvte_avg.ca.stats.as_string(description=True)

clf_lda = LDA()
cvte_lda = CrossValidation(clf_lda, NFoldPartitioner(),
                       errorfx=lambda p, t: np.mean(p == t),
                       enable_ca=['stats']) 
cv_results = cvte_lda(ds)
print cvte_lda.ca.stats.as_string(description=True)
