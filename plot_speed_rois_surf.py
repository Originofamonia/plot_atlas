#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot selected ROIs on surf
TODO: 5个ROI画在一个脑图里面 然后边界画出来 然后不同 subtype 用不同的cmap
"""
import numpy as np
from nilearn import datasets,plotting,surface,input_data
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

def main():
    data = datasets.fetch_atlas_harvard_oxford("cort-maxprob-thr0-1mm")
    fsaverage = datasets.fetch_surf_fsaverage()
    mask = datasets.load_mni152_brain_mask()
    masker = input_data.NiftiMasker(mask_img = mask).fit()
    maps = data['maps']
    names = np.array(data['labels'])
    left_roi_names = ['Left Precentral Gyrus','Left Frontal Pole',
    'Left Postcentral Gyrus',]
    right_roi_names = ['Right Precentral Gyrus','Right Temporal Pole']

    name_map = {
            'Left Precentral Gyrus':'Precentral Gyrus',
            'Left Frontal Pole':'Frontal Pole',
            'Right Precentral Gyrus': 'Precentral Gyrus',
            'Left Postcentral Gyrus':'Postcentral Gyrus',
            'Right Temporal Pole':'Temporal Pole',
            }
    radius = 1
    roi_speeds = np.array([[0.5710243, 0.48483637, 0.4158381], [0.5344531, 0.48818338, 0.4871025],
    [0.55191654, 0.41920632, 0.36598548], [0.4785908, 0.42470285, 0.39548638], 
    [0.51027787, 0.49033287, 0.4860968]])

    # create a list of colors for the rois
    # I prefer to control it this way so that I will know the correspondence
    from matplotlib.colors import ListedColormap
    # get the colors into a numpy array
    left_color_list = plt.cm.Paired(np.arange(len(left_roi_names)))
    right_color_list = plt.cm.Paired(np.arange(len(left_roi_names), len(left_roi_names)+len(right_roi_names)))
    # convert the numpy array of colors to a colormap object for plotting
    left_cmap = ListedColormap(left_color_list)
    right_cmap = ListedColormap(right_color_list)

    map_data = masker.transform(maps)
    left_new_map = np.zeros(map_data.shape)  # make 2 of this for left/right
    right_new_map = np.zeros(map_data.shape)
    reference = dict()
    handles, labels = [],[]
    left_labels, right_labels = [], []
    left_idx, right_idx = [], []
    # left
    for ii,((roi_native,roi_harvard),color,mask_name) in enumerate(zip(
                            name_map.items(),
                            left_color_list,
                            left_roi_names)):
        print(roi_native,mask_name)
        # for color checking
        reference[ii+1] = mask_name
        # create the legend handles and labels for plotting
        handles.append(Patch(facecolor = color))
        left_label = "Left " + name_map[mask_name]
        labels.append(left_label)
        left_labels.append(left_label)
        # for item in roi_harvard:
        idx, = np.where(names == roi_harvard)
        idx_brain = np.where(map_data[0] == idx[0])
        left_idx.append(idx[0])
        left_new_map[0,idx_brain] = ii + 1
        # next try put plot_surf_roi in this for loop
    left_temp = masker.inverse_transform(left_new_map)
    
    # right
    for ii,((roi_native,roi_harvard),color,mask_name) in enumerate(zip(
                                name_map.items(),
                                right_color_list,
                                right_roi_names)):
        print(roi_native,mask_name)
        # for color checking
        reference[ii+1+len(left_roi_names)] = mask_name
        # create the legend handles and labels for plotting
        handles.append(Patch(facecolor = color))
        right_label = "Right " +name_map[mask_name]
        labels.append(right_label)
        right_labels.append(right_label)
        # for item in roi_harvard:
        idx, = np.where(names == roi_harvard)
        idx_brain = np.where(map_data[0] == idx[0])
        right_idx.append(idx[0])
        right_new_map[0,idx_brain] = ii + 1
        # next try put plot_surf_roi in this for loop
    right_temp = masker.inverse_transform(right_new_map)

    # draw left
    fig,axes = plt.subplots(figsize = (9,6),
                            nrows = 3,
                            ncols = 2,
                            subplot_kw = {'projection':'3d'},
                            )
    left_roi = surface.vol_to_surf(left_temp,fsaverage.pial_left,radius=radius)
    right_roi = surface.vol_to_surf(right_temp,fsaverage.pial_right,radius=radius)
    # ax = axes[0][0]
    for i in range(3):
        if i < 2:
            left_color = roi_speeds[[0, 1, 3], i] / roi_speeds[[0, 1, 3], 0]
            right_color = roi_speeds[[2, 4], i] / roi_speeds[[2, 4], 0]
        else:
            left_color = roi_speeds[[0, 1, 3], i]
            right_color = roi_speeds[[2, 4], i]

        left_display = plotting.plot_surf_roi(fsaverage.infl_left,
                            left_roi,
                            bg_map = fsaverage.sulc_left,
                            view = 'lateral',
                            axes = axes[i][0],
                            figure = fig,
                            c=np.mean(left_color),
                            alpha=np.mean(left_color),
                            cmap = left_cmap,
                            colorbar = False,
                            title=f'Subtype {i+1}')
        # draw right
        # ax = axes[0][1]
        right_display = plotting.plot_surf_roi(fsaverage.infl_right,
                            right_roi,
                            bg_map = fsaverage.sulc_right,
                            view = 'medial',
                            axes = axes[i][1],
                            figure = fig,
                            title = '',
                            c=np.mean(right_color),
                            alpha=np.mean(right_color),
                            cmap = right_cmap,
                            colorbar = False,)
    
    fig.legend(handles,labels,
            # loc = 'center right',
            # bbox_to_anchor = (1.5,0.5),
            )

    fig.savefig(f'outputs/roi_surf.png', bbox_inches = 'tight')


if __name__ == '__main__':
    main()
