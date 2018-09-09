# import required libraries
import matplotlib.pyplot as plt
from math import pi

# define functions

def spider(skills, categories):
    my_dpi=96
    plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)

    n_plots = len(skills)

    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set2", n_plots)

    # number of variable
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    for i, row in enumerate(skills):
        # Initialise the spider plot
        ax = plt.subplot(n_plots + 1 // 2, min(2, n_plots), i + 1, polar=True)

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=7)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([1,2,3,4], ["1","2","3","4"], color="grey", size=7)
        plt.ylim(0,5)

        # Ind1
        values=[row[cat] for cat in categories]
        values += values[:1]
        ax.plot(angles, values, color=my_palette(i), linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=my_palette(i), alpha=0.4)

        # Add a title
        plt.title(row['Title'], size=10, color=my_palette(i), y=1.1)

plt.tight_layout()
