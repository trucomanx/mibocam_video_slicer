#!/usr/bin/python3 

################################################################################

import numpy as np
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



################################################################################
# define the function to compute MSE between two images

import OpenPifPafTools.OpenPifPafGetData as oppgd
import lib.lib_iou as liou

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
        
    iou_matrix = liou.create_iou_matrix(p1,p2); # p1 in rows, p2 in columns
    # len(p1)==len(correspondences)==len(ious) # 
    correspondences, ious = liou.find_correspondences(iou_matrix,min_iou=0.05);
    
    #print(iou_matrix, correspondences, ious ) 
    
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
            #print('passei por aqui')
            rmse.append(calculate_rmse_from_pil_roi(pil_img1,pil_img2));
            #pil_img1.save('e1.png')
            #pil_img2.save('e2.png')
    
    return max(rmse);

################################################################################

def get_annotation_from_pil(predictor,pil_current_frame,factor=2.0):
    width, height = pil_current_frame.size;
    resized_image = pil_current_frame.resize((int(width/factor), int(height/factor)));

    annotation_current, _, _ = predictor.pil_image(resized_image);
    for annot in annotation_current:
        annot.data[:, 0] *= factor;
        annot.data[:, 1] *= factor;
    return annotation_current;
