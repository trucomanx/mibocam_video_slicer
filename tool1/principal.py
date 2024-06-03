
# python3 principal.py --filename ../../VIDEOS/CP1.2.mp4 --output-dir CP1.2 --threshold 3.5

import os
import sys


INPUT_DIR='patients-videos';
OUTPUT_DIR='slices';
THRESHOLD=2.5;
START_COUNT=1;
FORMAT_FILENAME="{VNAME}/{FRAME}.png"; ## {COUNT}, {FRAME}, {VNAME}
DETECT_TYPE="body";

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

################################################################################
from pytictoc import TicToc
t = TicToc()
################################################################################

import lib.lib_iou as liou


# define the function to compute MSE between two images
import openpifpaf
import numpy as np
from PIL import Image
import OpenPifPafTools.OpenPifPafGetData as oppgd
import math

def calculate_rmse_from_pil_roi(image1, image2):
    # Asegúrate de que las imágenes tengan el mismo tamaño
    if image1.size != image2.size:
        raise ValueError("Las imágenes deben tener el mismo tamaño");

    # Convierte las imágenes en arrays numpy
    arr1 = np.array(image1, dtype=np.float64)
    arr2 = np.array(image2, dtype=np.float64)
    
    # Calcula la diferencia y luego el error cuadrático medio
    mse = np.mean((arr1 - arr2) ** 2)
    
    # Calcula la raíz cuadrada del MSE para obtener el RMSE
    rmse = math.sqrt(mse)
    
    return rmse

def get_rmse_of_people(pil_img1, pil_img2,annotation1,annotation2,detect_type): # predictor, numpy, numpy
    p1=[];
    for annot in annotation1: 
        if detect_type=='body':
            (xi,yi,xo,yo)=oppgd.get_body_bounding_rectangle(annot.data,factor=1.0);
        elif detect_type=='face':
            (xi,yi,xo,yo)=oppgd.get_face_bounding_rectangle(annot.data,factor=1.0);
        else:
            sys.exit('Error in detect_type, should be body or face.');
        xi=int(xi);        yi=int(yi);
        xo=int(xo);        yo=int(yo);
        if xi!=xo and yi!=yo:
            p1.append((xi,yi,xo,yo));
    
    p2=[];
    for annot in annotation2: 
        if detect_type=='body':
            (xi,yi,xo,yo)=oppgd.get_body_bounding_rectangle(annot.data,factor=1.0);
        elif detect_type=='face':
            (xi,yi,xo,yo)=oppgd.get_face_bounding_rectangle(annot.data,factor=1.0);
        else:
            sys.exit('Error in detect_type, should be body or face.');
        xi=int(xi);        yi=int(yi);
        xo=int(xo);        yo=int(yo);
        if xi!=xo and yi!=yo:
            p2.append((xi,yi,xo,yo));
    
    if len(p1)==0 and len(p2)==0:
        return 0;
    if len(p1)==0 or  len(p2)==0:
        return 255;
        
    iou_matrix = liou.create_iou_matrix(p1,p2);
    correspondences, ious = liou.find_correspondences(iou_matrix);
    
    rmse=[];
    for i in range(len(correspondences)):
        j = correspondences[i];
        if j!=None:
            box1 = p1[i];
            box2 = p2[j];
            ubox = liou.calculate_union_box(box1, box2);
            
            roi1 = pil_img1.crop(ubox);
            roi2 = pil_img2.crop(ubox);
            rmse.append(calculate_rmse_from_pil_roi(roi1,roi2));
        else:
            rmse.append(calculate_rmse_from_pil_roi(pil_img1,pil_img2));
    
    return max(rmse);


import lib.lib_save_data as lsd

import cv2

def get_annotation_from_pil(predictor,pil_current_frame,factor=2.0):
    width, height = pil_current_frame.size;
    resized_image = pil_current_frame.resize((int(width/factor), int(height/factor)));

    annotation_current, _, _ = predictor.pil_image(resized_image);
    for annot in annotation_current:
        annot.data[:, 0] *= factor;
        annot.data[:, 1] *= factor;
    return annotation_current;

def save_images(input_filename,
                output_dir,
                threshold, 
                format_filename="count_{COUNT}.png",
                my_pil_func=lsd.func_default_save,
                start_count=1,
                verbose=False,
                detect_type='body'):
    
    #predictor
    predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')#'shufflenetv2k16' 'mobilenetv2'
    
    nombre_archivo, extension = os.path.splitext(os.path.basename(input_filename));
    
    ## Make directory
    os.makedirs(output_dir,exist_ok=True);
    
    vidcap = cv2.VideoCapture(input_filename);

    # Verificar si el archivo de video se abrió correctamente
    if not vidcap.isOpened():
        sys.exit("Error opening th file: "+input_filename);
    
    # Obtener el número de frames del video
    tot_num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print('opened file:',input_filename);
    print('num frames:',tot_num_frames);
    print('start count:',start_count);
    count = start_count;
    first_success=True;
    num_frame=1;
    while vidcap.isOpened():
        success,image = vidcap.read()
        if success:
            t.tic()
            new_filename = str(format_filename);
            new_filename = new_filename.replace("{COUNT}", str(count))
            new_filename = new_filename.replace("{FRAME}", str(num_frame))
            new_filename = new_filename.replace("{VNAME}", nombre_archivo)
            
            
            if first_success:
                old_frame=cv2.cvtColor(image, cv2.COLOR_BGR2RGB);
                pil_old_frame = Image.fromarray(old_frame);
                annotation_old    , _, _ = predictor.pil_image(pil_old_frame);
                if my_pil_func(output_dir,new_filename, pil_old_frame,annotation_old):
                    print('count:',count,'frame:',num_frame,new_filename);
                    first_success=False;
                    count += 1;
            else:
                current_frame=cv2.cvtColor(image, cv2.COLOR_BGR2RGB); ## to numpy
                pil_current_frame = Image.fromarray(current_frame);
                
                #annotation_current, _, _ = predictor.pil_image(pil_current_frame);
                annotation_current=get_annotation_from_pil(predictor,pil_current_frame,factor=2.0);
                
                rmse=get_rmse_of_people(pil_current_frame, 
                                        pil_old_frame,
                                        annotation_current,
                                        annotation_old,
                                        detect_type); 
                #print(rmse,threshold);
                if rmse>threshold:
                    if my_pil_func(output_dir,new_filename, pil_current_frame,annotation_current):
                        pil_old_frame=pil_current_frame.copy();
                        annotation_old = annotation_current.copy();
                        print('count:',count,'frame:',num_frame,'rmse: %6.2f'%rmse,new_filename);
                        count += 1;
                else:
                    if verbose:
                        t.toc('count:'+str(count-1)+' frame:'+str(num_frame)+' pass')
            
            num_frame +=1;
        elif num_frame>=tot_num_frames:
            break;
        else:
            sys.exit('Error reading the file',input_filename);
    print('last count:',count);

    vidcap.release();
    cv2.destroyAllWindows();

import json
import lib.lib_json_tool as ljt
import lib.lib_get_files as lgf
if __name__ == "__main__":

    json_file_path='couple_files.json';
    index_file_path = 'index.json'
    
    if os.path.exists(json_file_path):
        couple_files=ljt.load_couples(json_file_path);
    else:
        couple_files=lgf.get_all_couple_dir_file(INPUT_DIR,ext='.mp4');
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
        tg.tic()
        save_images(input_filename=os.path.join(INPUT_DIR,reldir,filename),
                    output_dir=os.path.join(OUTPUT_DIR,reldir),
                    threshold=THRESHOLD, 
                    format_filename=FORMAT_FILENAME,
                    my_pil_func=lsd.func_default_save2,
                    start_count=START_COUNT,
                    verbose=False,
                    detect_type=DETECT_TYPE);
        tg.toc(filename+' elapsed:');
        l=l+1;
        with open(index_file_path, 'w', encoding='utf-8') as index_file:
            json.dump(l, index_file)
