#!/bin/bash

InputD='/media/fernando/DATA/Fernando/DATASET/TESE/PATIENT-MIBOCAM/patients-videos'
#InputD='/home/fernando/Downloads/dataset/files2/'

OutputD='/home/fernando/Downloads/output'
#OutputD='/home/fernando/Downloads/output-test'

#export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
python3 principal.py --input-dir $InputD --output-dir $OutputD --threshold 20 --detect-type face --verbose False

