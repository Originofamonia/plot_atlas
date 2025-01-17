# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:42:26 2020

@author: ning
"""

import os
import numpy as np
from glob import glob
from nilearn import image,plotting
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from nibabel import load as load_mri
import seaborn as sns
sns.set_context('poster')

# create a directory for the atlas
if not os.path.exists('../data'):
    os.mkdir('../data')
data_dir = os.path.join('../data','fmri_rois')
fig_dir = '../figures'
if not os.path.exists(fig_dir):
    os.mkdir(fig_dir)
collect_dir = '/export/home/nmei/nmei/properties_of_unconscious_processing/all_figures'
#dataset = datasets.fetch_atlas_craddock_2012('../data')
roi_names = """fusiform
inferiorparietal
inferiortemporal
lateraloccipital
lingual
middlefrontal
parahippocampal
pericalcarine
precuneus
superiorfrontal
superiorparietal
ventrolateralPFC""".split('\n')

#parsorbitalis
#parstriangularis
#parsopercularis

the_brain = f'{data_dir}/MNI152_T1_2mm_brain.nii.gz'
the_mask = f'{data_dir}/MNI152_T1_2mm_brain_mask_dil.nii.gz'
surf_dir = '../data/freesurfer/surf'
# get the standard ROIs
masks = [item for item in glob(os.path.join(data_dir,'ctx*nii.gz')) if\
         ('standard' not in item) and ('fsl' not in item) and\
             ('BOLD' not in item) and ('-pars' not in item)]
# combining left and right rois for plotting
# this is for validating if I have got the rois correctly


name_map = {
        'fusiform':'Fusiform gyrus',
        'inferiorparietal':'Inferior parietal lobe',
        'inferiortemporal':'Inferior temporal lobe',
        'lateraloccipital':'Lateral occipital cortex',
        'lingual':'Lingual',
        'middlefrontal':'Middle frontal gyrus',
        'parahippocampal':'Parahippocampal gyrus',
        'parahippocampal':'Parahippocampal gyrus',
        'pericalcarine':'Pericalcarine cortex',
        'precuneus':'Precuneus',
        'superiorfrontal':'Superior frontal gyrus',
        'superiorparietal':'Superior parietal gyrus',
        'ventrolateralPFC':'Inferior frontal gyrus',
        }

#plt.close('all')
handles, labels = [],[]
# create a list of colors for the rois
# I prefer to control it this way so that I will know the correspondence
from matplotlib.colors import ListedColormap
# get the colors into a numpy array
color_list = plt.cm.Paired(np.arange(len(roi_names)))
# convert the numpy array of colors to a colormap object for plotting
cmap = ListedColormap(color_list)

# for color checking
reference = dict()
for ii,(color,mask_name) in enumerate(zip(color_list,roi_names)):
    # pick the left and right hemisphere ROIs
    mask = [item for item in masks if (mask_name in item)]
    # rename the ROIs for plotting
    mask_name = name_map[mask_name]
    # put them into the same numpy array
    temp = np.array([load_mri(f).get_data() for f in mask])
    temp = temp.sum(0)
    # just in case of overlapping
    temp[temp > 0] = ii + 1
    if ii == 0: # initialize the combined mask numpy array
        combined_mask = temp
    else: # add the rest of the ROIs to those we already have
        combined_mask += temp
    # in case of overlapping, the overlapped regions belong to the last comer
    combined_mask[combined_mask > ii + 1] = ii + 1
    # for color checking
    reference[ii+1] = mask_name
    # create the legend handles and labels for plotting
    handles.append(Patch(facecolor = color))
    
    labels.append(mask_name)

# bound the mask
# mask_boundary = np.asanyarray(load_mri(the_mask).dataobj)
# combined_mask[mask_boundary == 0] = 0
# create a niftilImage from a numpy array
combined_mask = image.new_img_like(mask[0],combined_mask,)

from nilearn import datasets,surface
radius = 2
fsaverage = datasets.fetch_surf_fsaverage()
fig,axes = plt.subplots(figsize = (2 * 3,2 * 3),
                        nrows = 2,
                        ncols = 2,
                        subplot_kw = {'projection':'3d'},
                        )
ax = axes.flatten()[0]
brain_map_in_surf = surface.vol_to_surf(combined_mask,os.path.join(surf_dir,'lh.pial'),radius = radius,)
plotting.plot_surf_roi(os.path.join(surf_dir,'lh.inflated'),
                       brain_map_in_surf,
                       bg_map = os.path.join(surf_dir,'lh.sulc'),
                       threshold = 1e-16,
                       hemi = 'left',
                       view = 'lateral',
                       axes = ax,
                       figure = fig,
                       title = '',
                       cmap = cmap,
                       colorbar = False,)

# ax = axes.flatten()[1]
# brain_map_in_surf = surface.vol_to_surf(combined_mask,fsaverage.pial_right,radius = radius,)
# plotting.plot_surf_roi(fsaverage.infl_right,
#                        brain_map_in_surf,
#                        bg_map = fsaverage.sulc_right,
#                        threshold = 1e-6,
#                        hemi = 'right',
#                        view = 'lateral',
#                        bg_on_data = False,
#                        axes = ax,
#                        figure = fig,
#                        title = '',
#                        cmap = cmap,
#                        )

# ax = axes.flatten()[2]
# brain_map_in_surf = surface.vol_to_surf(combined_mask,fsaverage.pial_left,radius = radius,)
# plotting.plot_surf_roi(fsaverage.infl_left,
#                        brain_map_in_surf,
#                        bg_map = fsaverage.sulc_left,
#                        threshold = 1e-6,
#                        hemi = 'left',
#                        view = 'medial',
#                        bg_on_data = False,
#                        axes = ax,
#                        figure = fig,
#                        title = '',
#                        cmap = cmap,
#                        )

# ax = axes.flatten()[3]
# brain_map_in_surf = surface.vol_to_surf(combined_mask,fsaverage.pial_right,radius = radius,)
# plotting.plot_surf_roi(fsaverage.infl_right,
#                        brain_map_in_surf,
#                        bg_map = fsaverage.sulc_right,
#                        threshold = 1e-6,
#                        hemi = 'right',
#                        view = 'medial',
#                        bg_on_data = False,
#                        axes = ax,
#                        figure = fig,
#                        title = '',
#                        cmap = cmap,
#                        )







