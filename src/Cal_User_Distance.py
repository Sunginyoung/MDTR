import pandas as pd
import numpy as np

import scipy
from scipy.stats import f
from scipy.spatial.distance import mahalanobis

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import KernelPCA

def mahalanobis_array_dist(input_np, input_cent, input_cov_inv):
    return np.array([mahalanobis(i, input_cent, input_cov_inv) for i in input_np])

def get_pathinfo(pathinfo_dir, pathmatrix_dir):
    
    with open(pathinfo_dir, 'r') as file:
        path_cent = [float(i) for i in file.readline().split('\n')[0].split('\t')[1:]]
        path_infos = [float(line.split('\n')[0].split('\t')[1]) for line in file.readlines()]
    
    path_matrix = pd.read_csv(pathmatrix_dir, sep='\t', header=None)
    
    return path_cent, path_matrix, path_infos

def get_mechinfo(mechinfo_dir):
    
    return pd.read_csv(mechinfo_dir, sep='\t', index_col=0).to_dict('list')

def cal_series_dist(input_filedir, input_ptsdir, mechanism_dict, pathway_dict):
    
    input_exp = pd.read_csv(input_filedir, sep='\t', index_col=0).T
    input_columns = list(input_exp.index)
    pts_exp = pd.read_csv(input_ptsdir, sep='\t', index_col=0).T
    
    mech_dists = {}
    for mech, paths in mechanism_dict.items():
        
        path_dists = []
        for path in paths:
            
            pathgene = pathway_dict[path]

            pathinfo_dir = './src/data/Pathway_Data/%s/%s_Infos.txt'%(path, path)
            pathmatrix_dir = './src/data/Pathway_Data/%s/%s_Covariance_Inverse.txt'%(path, path)
            path_cent, path_matrix, path_infos = get_pathinfo(pathinfo_dir, pathmatrix_dir)
            path_cent_num = len(path_cent)
            
            path_pts = pts_exp[pathgene]
            path_scaler = StandardScaler().fit(path_pts)
            path_kpca = KernelPCA(n_components=path_cent_num, kernel='rbf', gamma=1/len(pathgene), random_state=42).fit(path_scaler.transform(path_pts))
            
            path_input = input_exp[pathgene]
            path_input_kpca = path_kpca.transform(path_scaler.transform(path_input))
            path_input_maha = (mahalanobis_array_dist(path_input_kpca, path_cent, path_matrix) - path_infos[0])/(path_infos[1]-path_infos[0])
            path_input_p = -np.log10(f.sf(path_input_maha, path_infos[2], path_infos[3]))
            path_dists.append(path_input_maha*path_input_p)
        
        mech_dists[mech] = np.sum(path_dists, axis=0)
        
    return input_columns, mech_dists

def cal_series_dist_minmax(input_columns, input_dists, mechanism_infodir):
    
    mech_infos = get_mechinfo(mechanism_infodir)
    
    return pd.DataFrame(
        [(input_dists[key]-value[0])/(value[1]-value[0])  for key, value in mech_infos.items()]
    , index=mech_infos.keys()
    , columns=input_columns)

def cal_user_dist(input_filedir, input_ptsdir, mechanism_infodir, mechanism_pathwaydir, pathway_genedir):
    
    mechanism_dict = {}
    with open(mechanism_pathwaydir, 'r') as file:
        for line in file.readlines():
            lists = line.split('\n')[0].split('\t')
            mechanism_dict[lists[0]] = lists[1:]
    
    pathway_dict = {}
    with open(pathway_genedir, 'r') as file:
        for line in file.readlines():
            lists = line.split('\n')[0].split('\t')
            pathway_dict[lists[0]] = lists[1:]
    
    input_columns, input_dists = cal_series_dist(input_filedir, input_ptsdir, mechanism_dict, pathway_dict)
    
    return cal_series_dist_minmax(input_columns, input_dists, mechanism_infodir)