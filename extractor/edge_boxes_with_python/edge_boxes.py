import tempfile
import subprocess
import shlex
import os
import numpy as np
import scipy.io
import cv2
import time

script_dirname = os.path.abspath(os.path.dirname(__file__))

np.set_printoptions(threshold='nan')

def get_windows(image_fnames, cmd='edge_boxes_wrapper'):
    """
    Run MATLAB EdgeBoxes code on the given image filenames to
    generate window proposals.

    Parameters
    ----------
    image_filenames: strings
        Paths to images to run on.
    cmd: string
        edge boxes function to call:
            - 'edge_boxes_wrapper' for effective detection proposals paper configuration.
    """
    # Form the MATLAB script command that processes images and write to
    # temporary results file.
    f, output_filename = tempfile.mkstemp(suffix='.mat')
    os.close(f)
    fnames_cell = '{' + ','.join("'{}'".format(x) for x in image_fnames) + '}'
    command = "{}({}, '{}')".format(cmd, fnames_cell, output_filename)

    #toolboxpath = os.path.abspath('./edge_boxes_with_python/toolbox/')
    toolboxpath = os.path.abspath('./toolbox/')
    pathcommand1 = "addpath(genpath('{}'));".format(toolboxpath)
    pathcommand2 = "savepath;"
    # Execute command in MATLAB.
    path_mc = "matlab -nojvm -r \"{} {} exit\"".format(pathcommand1, pathcommand2)
    os.system(path_mc)
    mc = "matlab -nojvm -r \"try; {}; catch; exit; end; exit\"".format(command)
    pid = subprocess.Popen(
        shlex.split(mc), stdout=open('/dev/null', 'w'), cwd=script_dirname)
    retcode = pid.wait()
    if retcode != 0:
        raise Exception("Matlab script did not exit successfully!")

    # Read the results and undo Matlab's 1-based indexing.
    all_boxes = list(scipy.io.loadmat(output_filename)['all_boxes'][0])
    subtractor = np.array((1, 1, 0, 0, 0))[np.newaxis, :]
    all_boxes = [boxes - subtractor for boxes in all_boxes]

    # Remove temporary file, and return.
    os.remove(output_filename)
    if len(all_boxes) != len(image_fnames):
        raise Exception("Something went wrong computing the windows!")
    
    #print(all_boxes[0])
    return all_boxes

def visualize_boxes(image_file, boxs):
    img = cv2.imread(image_file)
    for box in boxs:
        print(box)
        if box[4] < 0.1:
            continue
        cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (int(255*box[4]), 0, 0), 3)
    
    cv2.imshow('img', img)
    cv2.waitKey(0)

if __name__ == '__main__':
    image_filenames = ['000004.jpg', '001551.jpg']
    boxes = get_windows(image_filenames)
    for image_file, boxs in zip(image_filenames, boxes):
        visualize_boxes(image_file, boxs)
