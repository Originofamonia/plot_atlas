"""
plot brain regions
"""

import os
import numpy as np
from glob import glob
from collections import defaultdict
import pandas as pd
import pickle
from nilearn import image,plotting, datasets
from nilearn.surface import vol_to_surf
from nilearn.datasets import fetch_surf_fsaverage
from nilearn.plotting.cm import _cmap_d
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from nibabel import load as load_mri
import seaborn as sns
sns.set_context('poster')
from typing import List


def create_mesh(mask_list:List,stat_mesh:str,radius:int = 2,kind:str = 'line',) -> np.ndarray:
    """
    Parameters
    ----------
    mask_list : List
        DESCRIPTION.
    stat_mesh : str
        DESCRIPTION.
    radius : int, optional
        DESCRIPTION. The default is 2.
    kind : str, optional
        DESCRIPTION. The default is 'line'.

    Returns
    -------
    side_mesh : np.ndarray
        DESCRIPTION.

    """
    side = np.vstack([np.array(vol_to_surf(item,
                                           stat_mesh,
                                           radius = radius,
                                           kind = 'line',) > 0.,
                               dtype = int) for item in mask_list])
    idx_side = {ii:np.unique(item) for ii,item in enumerate(side.T * np.arange(1,len(mask_list)+1,).reshape(1,-1))}
    side_mesh = np.zeros(side.shape[1])
    for key,val in idx_side.items():
        side_mesh[key] = val[1] if val.shape[0] > 1 else val[0]
    return side_mesh

def rename_roi_names():
    cwd = os.getcwd()
    roi_speed_file = os.path.join('/', *cwd.split('/')[:-1], 'adni_project/output/subtype_roi_speed.pickle')
    roi_speed = None
    with open(roi_speed_file, 'rb') as f:
        while True:
            try:
                roi_speed = pickle.load(f)
            except EOFError:
                break
    roi_dict_file = os.path.join('/', *cwd.split('/')[:-1], 'adni_project/data/TADPOLE_D1_D2_Dict.csv')
    roi_dict_df = pd.read_csv(roi_dict_file)
    renamed_roi_speed = defaultdict(list)
    for k, v in roi_speed.items():
        # print(k, v)
        real_name = roi_dict_df[roi_dict_df['FLDNAME'] == k]['TEXT'].values[0]
        renamed_roi_speed[real_name] = v
    
    return renamed_roi_speed


def main():
    # renamed_roi_speed = rename_roi_names()

    atlas_data = datasets.fetch_atlas_harvard_oxford('cortl-prob-1mm')
    atlas_filename = atlas_data['maps']
    # roi_indices = [13, 1, 14, 33, 16]  # old, left/right wrong
    roi_indices = [14, 2, 13, 34, 15]  # shifted
    roi_speeds = np.array([[0.5710243, 0.48483637, 0.4158381], [0.5344531, 0.48818338, 0.4871025],
    [0.55191654, 0.41920632, 0.36598548], [0.4785908, 0.42470285, 0.39548638], 
    [0.51027787, 0.49033287, 0.4860968]])
    roi_names = ['Left Precentral Gyrus','Left Frontal Pole','Right Precentral Gyrus',
    'Left Postcentral Gyrus','Right Temporal Pole']
    colormap = _cmap_d['bwr_r']
    # x=left-, right+; y=front+, rear-; z=up+, down-.
    cut_coords = [(-40, 11, -29),(-38, 0, -7),(10, -17, 40),(-25, -55, 45),(38, 10, -25)]
    for i, roi in enumerate(roi_names):
        fig,ax = plt.subplots(figsize = (6*2,5*2),
                            nrows = 3,
                            ncols = 1,
                            )
        dmn_nodes = image.index_img(atlas_filename, [roi_indices[i]])
        # coords = plotting.find_probabilistic_atlas_cut_coords(atlas_filename)
        coords = cut_coords[i]
        plotting.plot_prob_atlas(dmn_nodes,
                                cut_coords=coords,  # (0, -55, 29),
                                alpha=roi_speeds[i][0]/max(roi_speeds[i]),
                                axes = ax[0],
                                figure = fig,
                                # cmap=colormap,
                                title=f"{roi}, Subtype 1",
                                black_bg=False,
                                )
        plotting.plot_prob_atlas(dmn_nodes,
                                cut_coords=coords,
                                alpha=roi_speeds[i][1]/max(roi_speeds[i]),
                                axes = ax[1],
                                figure = fig,
                                # cmap=colormap,
                                title='Subtype 2',
                                black_bg=False,
                                )
        plotting.plot_prob_atlas(dmn_nodes,
                                cut_coords=coords,
                                alpha=roi_speeds[i][2],
                                axes = ax[2],
                                figure = fig,
                                # cmap=colormap,
                                title='Subtype 3',
                                black_bg=False,
                                )

        # plotting.plot_surf_roi(fsaverage.infl_left,
        #                     parcellation['map_left'],
        #                     hemi = 'left',
        #                     bg_map = fsaverage.sulc_left,
        #                     cmap = cmap,
        #                     axes = ax[0][0],
        #                     figure = fig,
        #                     )
        # fig.legend(handles,
        #         labels,
        #         bbox_to_anchor=(0, .6),
        #         loc = "center right",
        #         borderaxespad = 1,
        #         frameon = False,
        #         )
        
        fig.savefig(f'outputs/overlay{i}.png',
                    # dpi = 300,
                    bbox_inches = 'tight')


if __name__ == "__main__":
    main()
