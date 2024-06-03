#!/bin/bash

InputD='/media/fernando/Expansion/DATASET/TESE/PATIENT-MIBOCAM/patients-videos'
#InputD='/home/fernando/Downloads/dataset/'
OutputD='/home/fernando/Downloads/output'

#export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
python3 principal.py --input-dir $InputD --output-dir $OutputD --threshold 18 --detect-type face 

