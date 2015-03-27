#!/usr/bin/python

import yt
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='HDF5 file', default="")
parser.add_argument('--field', help='field variable', default="density",
        choices=('density', 'velocity_x', 'velocity_y',
            'dens', 'denn', 'dend', 'deni', 'vlxi', 'vlyi', 'vlzi'))
args = parser.parse_args()

ds = yt.load(args.filename)

c = (ds.domain_right_edge + ds.domain_left_edge)/2.0
L = np.array([1.0, 1.0, 1.0])
W = ds.quan(0.3, 'unitary')
N = 256

cam = ds.camera(c, L, W, N, tf, fields = [args.field], log_fields = [True])

im = cam.snapshot('test_rendering.png')
