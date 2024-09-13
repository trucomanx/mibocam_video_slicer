#!/usr/bin/python3

import os
import cv2
import openpifpaf
import lib.lib_save_data as lsd
from PIL import Image
from pytictoc import TicToc

from func_people import get_annotation_from_pil
from func_people import get_rmse_of_people


Td = TicToc()

def save_images(input_filename,
                output_dir,
                threshold, 
                format_filename="count_{COUNT}.png",
                my_pil_func=lsd.func_default_save,
                start_count=1,
                verbose=False,
                detect_type='body',
                max_size=None):
    
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
            Td.tic()
            new_filename = str(format_filename);
            new_filename = new_filename.replace("{COUNT}", str(count))
            new_filename = new_filename.replace("{FRAME}", str(num_frame))
            new_filename = new_filename.replace("{VNAME}", nombre_archivo)
            
            
            if first_success:
                old_frame=cv2.cvtColor(image, cv2.COLOR_BGR2RGB);
                pil_old_frame = Image.fromarray(old_frame);
                annotation_old    , _, _ = predictor.pil_image(pil_old_frame);
                if my_pil_func(output_dir,new_filename, pil_old_frame,annotation_old,resize=max_size):
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
                    if my_pil_func(output_dir,new_filename, pil_current_frame,annotation_current,resize=max_size):
                        pil_old_frame=pil_current_frame.copy();
                        annotation_old = annotation_current.copy();
                        print('count:',count,'frame:',num_frame,'rmse: %6.2f'%rmse,new_filename);
                        count += 1;
                else:
                    if verbose:
                        Td.toc('count:'+str(count-1)+' frame:'+str(num_frame)+' pass')
            
            num_frame +=1;
        elif num_frame>=tot_num_frames:
            break;
        else:
            sys.exit('Error reading the file',input_filename);
    print('last count:',count);

    vidcap.release();
    cv2.destroyAllWindows();
