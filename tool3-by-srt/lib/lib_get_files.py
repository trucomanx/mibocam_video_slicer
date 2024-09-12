#!/usr/bin/python3 arg1 arg2

import os

def get_all_files(input_dir,ext='.mp4'):
    mp4_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(ext):
                mp4_files.append(os.path.join(root, file))
    return mp4_files


def get_all_couple_dir_file(input_dir,ext='.mp4'):
    couple_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(ext):
                filepath=os.path.join(root, file);
                directory = os.path.dirname(filepath)
                filename = os.path.basename(filepath)
                relpath=os.path.relpath(os.path.abspath(directory), input_dir)
                couple_files.append((relpath,filename))
    return couple_files

