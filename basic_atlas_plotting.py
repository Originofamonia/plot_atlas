"""
https://nilearn.github.io/stable/auto_examples/01_plotting/plot_atlas.html#sphx-glr-auto-examples-01-plotting-plot-atlas-py
https://nilearn.github.io/dev/auto_examples/01_plotting/plot_3d_map_to_surface_projection.html
"""
import os
from nilearn import datasets, plotting,surface
from nibabel import load
import numpy as np


def main():
    # Get a statistical map
    motor_images = datasets.fetch_neurovault_motor_task()
    stat_img = motor_images.images[0]
    # Get a cortical mesh
    fsaverage = datasets.fetch_surf_fsaverage()
    # Sample the 3D data around each node of the mesh
    texture = surface.vol_to_surf(stat_img, fsaverage.pial_right)
    destrieux_atlas = datasets.fetch_atlas_surf_destrieux()
    parcellation = destrieux_atlas['map_right']
    # destrieux_atlas = datasets.fetch_atlas_destrieux_2009()
    # parcellation = destrieux_atlas['maps']

    # these are the regions we want to outline
    regions_dict = {b'G_postcentral': 'Postcentral gyrus',
                    b'G_precentral': 'Precentral gyrus'}

    # get indices in atlas for these labels
    regions_indices = [np.where(np.array(destrieux_atlas['labels']) == region)[0][0]
                    for region in regions_dict]

    labels = list(regions_dict.values())

    display = plotting.plot_surf_stat_map(fsaverage.infl_right, texture, hemi='right',
                                     title='Surface right hemisphere',
                                     colorbar=False, threshold=10.,
                                     bg_map=fsaverage.sulc_right)

    plotting.plot_surf_contours(fsaverage.infl_right, parcellation, labels=labels,
                                levels=regions_indices, figure=display, legend=True,
                                colors=['g', 'k'])
    # roi_map = [item]
    plotting.plot_surf_roi(fsaverage.infl_right, parcellation, figure=display, 
                           legend=True, colors=['g', 'k'])

    display.figure.savefig(f'outputs/roi_outlines.png')


def read_tadpole_rois():
    """
    get a list of our significant ROIs
    """
    file = os.getcwd()


if __name__ == '__main__':
    main()
