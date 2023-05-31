import math
from math import pi

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def plot_radar(radar_list, radar_label):
    
    if len(radar_list) != len(radar_label):
        print('Please check the size of distance list and label list')
    else:
        num_label = len(radar_label)
        angles = [x/float(num_label)*(2*pi) for x in range(num_label)]
        angles += angles[:1]
        
        fig = plt.figure(figsize=(8,8))
        fig.set_facecolor('white')
        ax = fig.add_subplot(polar=True)
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        
        # x and y label
        plt.xticks(angles[:-1], radar_label, fontsize=13, weight='bold')
        ax.tick_params(axis='x', which='major', pad=30)
        ax.set_rlabel_position(0)
        plt.yticks([0.2, 0.4, 0.6, 0.8], ['0.2','0.4', '0.6', '0.8'], fontsize=10)
        plt.ylim(0,1)
        
        # data radar
        radar_input = radar_list+radar_list[:1]
        ax.plot(angles, radar_input, color='tab:red', linewidth=2, linestyle='solid')
        ax.fill(angles, radar_input, color='tab:red', alpha=0.5)
        
        for g in ax.yaxis.get_gridlines():
            g.get_path()._interpolation_steps = num_label

        spine = Spine(axes=ax,
                  spine_type='circle',
                  path=Path.unit_regular_polygon(num_label))
        spine.set_transform(Affine2D().scale(.5).translate(.5, .5)+ax.transAxes)
        ax.spines = {'polar':spine}  