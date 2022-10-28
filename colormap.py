"""
try cmap
https://betterprogramming.pub/how-to-use-colormaps-with-matplotlib-to-create-colorful-plots-in-python-969b5a892f0c
set c/color a number, cmap: pick a cmap, done.
"""

import pandas as pd
import matplotlib.pyplot as plt

def main():
    #import data and create dataframe
    wine_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data' 
    wine_column_headers = ['Alcohol','Malic acid','Ash','Alcalinity of ash',  
                        'Magnesium','Total phenols','Flavanoids',
                        'Nonflavanoid phenols','Proanthocyanins','Color intensity', 
                        'Hue','OD280/OD315 of diluted wines' ,'Proline']
    wine_df = pd.read_csv(wine_url, names = wine_column_headers)

    #figure
    fig, ax1 = plt.subplots()
    fig.set_size_inches(13, 10)

    #labels
    ax1.set_xlabel('Alcohol')
    ax1.set_ylabel('Color Intensity')
    ax1.set_title('Relationship Between Color Intensity and Alcohol Content in Wines')

    #c sequence
    c = wine_df['Color intensity']

    #plot(x, y, s: marker size, c: color)
    plt.scatter(wine_df['Alcohol'], wine_df['Color intensity'] , c=c, 
                cmap = 'RdPu', s = wine_df['Proline']*.5, alpha =0.5)
    cbar = plt.colorbar()
    cbar.set_label('Color Intensity')
    fig.savefig(f'outputs/cmap.png')


if __name__ == '__main__':
    main()
