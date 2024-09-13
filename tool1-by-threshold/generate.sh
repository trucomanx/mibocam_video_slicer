#!/bin/bash

InputD='/mnt/8811f502-ae19-4dd8-8371-f1915178f581/Fernando/DATASET/TESE/PATIENT-MIBOCAM/patients-videos'


OutputD='/home/fernando/Downloads/output'


#export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

python3 principal.py    --input-dir $InputD \
                        --output-dir $OutputD \
                        --threshold 30 \
                        --detect-type face \
                        --verbose False

