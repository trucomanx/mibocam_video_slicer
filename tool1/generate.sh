#!/bin/bash

InputD='/media/fernando/Expansion/DATASET/TESE/PATIENT-MIBOCAM/patients-videos'
OutputD='/media/fernando/Expansion/output'

#export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
python3 principal.py --input-dir $InputD --output-dir $OutputD --threshold 12 

