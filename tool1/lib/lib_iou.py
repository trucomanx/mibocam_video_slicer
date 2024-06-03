#!/usr/bin/python3 arg1 arg2

def calculate_union_box(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1;
    x2_min, y2_min, x2_max, y2_max = box2;
    
    # Calcula las coordenadas de la intersección
    xi1 = min(x1_min, x2_min);
    yi1 = min(y1_min, y2_min);
    xi2 = max(x1_max, x2_max);
    yi2 = max(y1_max, y2_max);
    
    return (xi1,yi1,xi2,yi2);
    
def calculate_iou(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1;
    x2_min, y2_min, x2_max, y2_max = box2;
    
    # Calcula las coordenadas de la intersección
    xi1 = max(x1_min, x2_min)
    yi1 = max(y1_min, y2_min)
    xi2 = min(x1_max, x2_max)
    yi2 = min(y1_max, y2_max)
    
    # Calcula el área de la intersección
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    
    # Calcula el área de ambas bounding boxes
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    
    # Calcula el área de la unión
    union_area = box1_area + box2_area - inter_area
    
    # Calcula el IoU
    iou = inter_area / union_area if union_area != 0 else 0
    return iou;


def create_iou_matrix(boxes1, boxes2):
    '''
    boxes1 in rows, boxes2 in columns
    '''
    iou_matrix = []
    for box1 in boxes1:
        row = []
        for box2 in boxes2:
            iou = calculate_iou(box1, box2)
            row.append(iou)
        iou_matrix.append(row)
    return iou_matrix

def find_correspondences(iou_matrix,min_iou=0.05):
    correspondences = [];
    ious = [];
    for i, row in enumerate(iou_matrix):
        max_iou = max(row)
        if max_iou>min_iou:
            j = row.index(max_iou);
        else:
            j = None;
        correspondences.append(j);
        ious.append(max_iou);
    return correspondences, ious;
