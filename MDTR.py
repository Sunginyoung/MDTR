import argparse
import os

import src.Cal_User_Distance as Cal_User_Distance
import src.Vis_Radar_Chart as Vis_Radar_Chart
import matplotlib.pyplot as plt

def run_MDTRuler(input_dir, output_dir, save_rader=0):

    ptsexp_dir = './src/data/Potential_Toxic_Expression.txt'
    mechinfo_dir = './src/data/Mechanism_Infos.txt'
    mechpath_dir = './src/data/Mechanism_Pathway_List.txt'
    mechpathgene_dir = './src/data/Mechanism_Pathway_Gene_List.txt'
    
    input_dist = Cal_User_Distance.cal_user_dist(input_dir, ptsexp_dir, mechinfo_dir, mechpath_dir, mechpathgene_dir)
    input_dist.to_csv(output_dir+'/MTDR_result.txt', sep='\t')
    
    if save_rader!=0:
        mechanisms=list(input_dist.index)
        columns=list(input_dist.columns)
        for column in columns:
            Vis_Radar_Chart.plot_radar(list(input_dist[column]), mechanisms)
            plt.savefig(output_dir+'/%s.png'%column, bbox_inches='tight')
            
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('expr', type=open, help='File path of gene expression data. Tab-delimited file format (.txt) is recommended for input data. It is also recommended to use Z-normalized files.')    
    parser.add_argument('outdir', help = 'Directory to save a result file')
    parser.add_argument('--r', type=int, default=0, help = '(1/0) Whether to save the radar chart for the measured results (default=0)')
    
    args = parser.parse_args()
    
    input_dir = args.expr
    output_dir = args.outdir
    radar_chart = args.r
    
    run_MDTRuler(input_dir = input_dir, output_dir = output_dir, save_rader = radar_chart)
    
if __name__ == "__main__":
    main()