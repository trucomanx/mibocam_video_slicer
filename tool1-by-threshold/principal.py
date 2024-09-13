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
from tqdm import tqdm
from pytictoc import TicToc

import lib.lib_save_data as lsd
import lib.lib_json_tool as ljt
import lib.lib_get_files as lgf

from func_extras import save_images
from func_extras import get_unprocessed_list


if __name__ == "__main__":

    # Arquivo com uma lista de elementos, cada elemento 'e uma lista de dois string
    json_all_files_path = os.path.join(OUTPUT_DIR,'all_couples_files.json');
    json_processed_path = 'processed_couples_files.json';
    
    all_couple_files=lgf.get_all_couple_dir_file(INPUT_DIR,ext='.mp4');
    ljt.save_couples(all_couple_files,json_all_files_path);
    
    processed_couple_files=[];
    if os.path.exists(json_processed_path):
        with open(json_processed_path, 'r', encoding='utf-8') as index_file:
            processed_couple_files = json.load(index_file) 
    
    print("            Number of files:",len(all_couple_files))
    print("  Number of processed files:",len(processed_couple_files))
    couple_files=get_unprocessed_list(all_couple_files,processed_couple_files);
    L=len(couple_files);
    print("Number of unprocessed files:",L)
    
    tg = TicToc();
    l=0;
    
    for l in tqdm(range(L)):
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
            processed_couple_files.append(couple_files[l]);
        else:
            print("")
            print("File not found:",mp4_path);
            print("")
        
        ljt.save_couples(processed_couple_files,json_processed_path);


