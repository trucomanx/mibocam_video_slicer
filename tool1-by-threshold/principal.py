#/usr/bin/python3

import os
import sys


INPUT_DIR='patients-videos';
OUTPUT_DIR='slices';
THRESHOLD=2.5;
START_COUNT=1;
FORMAT_FILENAME="{VNAME}_{FRAME}.png"; ## {COUNT}, {FRAME}, {VNAME}
DETECT_TYPE="body";
VERBOSE=False;
MAX_SIZE=300;

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
    elif sys.argv[n]=='--threshold':
        THRESHOLD=float(sys.argv[n+1]);
    elif sys.argv[n]=='--start-count':
        START_COUNT=int(sys.argv[n+1]);
    elif sys.argv[n]=='--detect-type':
        DETECT_TYPE=sys.argv[n+1];
    elif sys.argv[n]=='--verbose':
        VERBOSE=(sys.argv[n+1].lower()=='true');
        
################################################################################





import json
from pytictoc import TicToc

import lib.lib_save_data as lsd
import lib.lib_json_tool as ljt
import lib.lib_get_files as lgf

from func_extras import save_images


if __name__ == "__main__":

    # Arquivo com uma lista de elementos, cada elemento 'e uma lista de dois string
    json_file_path=os.path.join(OUTPUT_DIR,'couple_files.json');
    index_file_path = 'index.json';
    
    if os.path.exists(json_file_path):
        couple_files=ljt.load_couples(json_file_path);
    else:
        couple_files=lgf.get_all_couple_dir_file(INPUT_DIR,ext='.mp4');
        ljt.save_couples(couple_files,json_file_path);
    
    ## couple_files : [ ["patient5/camera1","filename.mp4"], ..., [...] ]
    L=len(couple_files);
    print('L',L)
    
    tg = TicToc();
    l=0;
    
    if os.path.exists(index_file_path):
        with open(index_file_path, 'r', encoding='utf-8') as index_file:
            l = json.load(index_file)
    
    while l<L:
        reldir   = couple_files[l][0];
        filename = couple_files[l][1];
        mp4_path = os.path.join(INPUT_DIR,reldir,filename);
        if os.path.exists(mp4_path):
            tg.tic()
            save_images(input_filename=mp4_path,
                        output_dir=os.path.join(OUTPUT_DIR,reldir),
                        threshold=THRESHOLD, 
                        format_filename=FORMAT_FILENAME,
                        my_pil_func=lsd.func_default_save2,
                        start_count=START_COUNT,
                        verbose=VERBOSE,
                        detect_type=DETECT_TYPE,
                        max_size=MAX_SIZE);
            tg.toc(filename+' elapsed:');
        l=l+1;
        with open(index_file_path, 'w', encoding='utf-8') as index_file:
            json.dump(l, index_file)

