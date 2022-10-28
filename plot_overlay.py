"""
Visualizing a probabilistic atlas: the default mode in the MSDL atlas
=====================================================================

Visualizing a probabilistic atlas requires visualizing the different
maps that compose it.

Here we represent the nodes constituting the default mode network in the
`MSDL atlas
<https://team.inria.fr/parietal/18-2/spatial_patterns/spatial-patterns-in-resting-state/>`_.

The tools that we need to leverage are:

 * :func:`nilearn.image.index_img` to retrieve the various maps composing
   the atlas

 * Adding overlays on an existing brain display, to plot each of these
   maps

Alternatively, :func:`nilearn.plotting.plot_prob_atlas` allows to plot the maps in one step that
with less control over the plot (see below)

"""
############################################################################
# Fetching probabilistic atlas - MSDL atlas
# -----------------------------------------
from nilearn import datasets
from nilearn import plotting, image


def main():
    # atlas_data = datasets.fetch_atlas_msdl()
    # atlas_filename = atlas_data.maps
    # atlas = datasets.fetch_atlas_destrieux_2009() # error 3D, but need 4D
    # atlas_filename = atlas['maps']
    destrieux_atlas = datasets.fetch_atlas_destrieux_2009()
    atlas_data = datasets.fetch_atlas_harvard_oxford('cortl-prob-1mm')
    atlas_filename = atlas_data['maps']
    
    #############################################################################
    # Visualizing a probabilistic atlas with plot_stat_map and add_overlay object
    # ---------------------------------------------------------------------------
    

    # First plot the map for the PCC: index 4 in the atlas
    # display = plotting.plot_stat_map(#destrieux_atlas['maps'],
    #     image.index_img(atlas_filename, 0),
    #     threshold=200,
    #     colorbar=True,
    #     # title="DMN nodes in MSDL atlas"
    #     )

    # # Now add as an overlay the maps for the ACC and the left and right
    # # parietal nodes
    # # Left Precentral Gyrus: 13; Left Frontal Pole: 1; Right Precentral Gyrus: 14;
    # # Left Postcentral Gyrus: 33; Right Temporal Pole: 16
    roi_indices = [13, 1, 14, 33, 16]
    # display.add_overlay(image.index_img(atlas_filename, roi_indices[0]),
    #                     cmap=plotting.cm.black_blue)
    # display.add_overlay(image.index_img(atlas_filename, roi_indices[1]),
    #                     cmap=plotting.cm.black_green)
    # display.add_overlay(image.index_img(atlas_filename, roi_indices[2]),
    #                     cmap=plotting.cm.black_pink)
    # display.add_overlay(image.index_img(atlas_filename, roi_indices[3]),
    #                     cmap=plotting.cm.brown_cyan)
    # display.add_overlay(image.index_img(atlas_filename, roi_indices[4]),
    #                     cmap=plotting.cm.blue_orange)

    # display.savefig(f'outputs/plot_overlay1.png')


    ###############################################################################
    # Visualizing a probabilistic atlas with plot_prob_atlas
    # ======================================================
    #
    # Alternatively, we can create a new 4D-image by selecting the 3rd, 4th, 5th and 6th (zero-based) probabilistic map from atlas
    # via :func:`nilearn.image.index_img` and use :func:`nilearn.plotting.plot_prob_atlas` (added in version 0.2)
    # to plot the selected nodes in one step.
    #
    # Unlike :func:`nilearn.plotting.plot_stat_map` this works with 4D images
    
    # for idx in roi_indices:
    dmn_nodes = image.index_img(atlas_filename, roi_indices)
    # Note that dmn_node is now a 4D image
    print(dmn_nodes.shape)
    ####################################

    display = plotting.plot_prob_atlas(dmn_nodes,
                                    cut_coords=(0, -55, 29),
                                    alpha=1,
                                    # title="DMN nodes in MSDL atlas"
                                    )
    display.savefig(f'outputs/plot_overlay2.png')


if __name__ == '__main__':
    main()
