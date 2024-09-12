#!/bin/bash

InputD='/media/fernando/Expansion/DATASET/TESE/PATIENT-MIBOCAM/patients-videos'
#InputD='/home/fernando/Downloads/dataset/files2/'

OutputD='/home/fernando/Downloads/output'
#OutputD='/home/fernando/Downloads/output-test'

python3 principal.py --input-dir $InputD --output-dir $OutputD  --verbose False

