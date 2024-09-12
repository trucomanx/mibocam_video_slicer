
# python3 principal.py --filename ../../VIDEOS/CP1.2.mp4 --output-dir CP1.2 --threshold 3.5

import os
import sys


INPUT_DIR='patients-videos';
OUTPUT_DIR='slices';
START_COUNT=1;
FORMAT_FILENAME="{VNAME}_{INDEX}.mp4"; ## {VNAME}, {INDEX}, 
VERBOSE=False;

#import torch
#torch.cuda.empty_cache();
#torch.cuda.set_per_process_memory_fraction(0.1)  # limitar a un 10% del uso de memoria de la GPU

################################################################################
# total arguments
for n in range(len(sys.argv)):
    if   sys.argv[n]=='--input-dir':
        INPUT_DIR=sys.argv[n+1];
    elif sys.argv[n]=='--output-dir':
        OUTPUT_DIR=sys.argv[n+1];
    elif sys.argv[n]=='--output-format-filename':
        FORMAT_FILENAME=sys.argv[n+1];
    elif sys.argv[n]=='--start-count':
        START_COUNT=int(sys.argv[n+1]);
    elif sys.argv[n]=='--verbose':
        VERBOSE=(sys.argv[n+1].lower()=='true');
        
################################################################################
from pytictoc import TicToc
t = TicToc()
################################################################################


import json
import lib.lib_json_tool as ljt
import lib.lib_get_files as lgf
import lib.lib_split_srt as lss
if __name__ == "__main__":

    json_file_path='srt_files.json';
    index_file_path = 'index.json'
    
    if os.path.exists(json_file_path):
        couple_files=ljt.load_couples(json_file_path);
    else:
        couple_files=lgf.get_all_couple_dir_file(INPUT_DIR,ext='.srt');
        ljt.save_couples(couple_files,json_file_path);
    
    L=len(couple_files);
    
    tg = TicToc();
    l=0;
    
    if os.path.exists(index_file_path):
        with open(index_file_path, 'r', encoding='utf-8') as index_file:
            l = json.load(index_file)
    
    while l<L:
        reldir   = couple_files[l][0];
        filename = couple_files[l][1];
        srt_path = os.path.join(INPUT_DIR,reldir,filename);
        if os.path.exists(srt_path):
            tg.tic()
            lss.split_video(INPUT_DIR,reldir,filename,OUTPUT_DIR,FORMAT_FILENAME)
            
            tg.toc(filename+' elapsed:');
        l=l+1;
        with open(index_file_path, 'w', encoding='utf-8') as index_file:
            json.dump(l, index_file)




