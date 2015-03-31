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

# Do you want the log of the field?
use_log = True

# Find the bounds in log space of for your field
dd = ds.all_data()
mi, ma = dd.quantities.extrema(args.field)

if use_log:
    mi, ma = np.log10(mi), np.log10(ma)

# Instantiate the ColorTransferfunction.
tf = yt.ColorTransferFunction((mi, ma))

print(ds)
c = (ds.domain_right_edge + ds.domain_left_edge)/2.0
L = np.array([1.0, 1.0, 1.0])
W = ds.domain_right_edge - ds.domain_left_edge
N = 1024

tf.add_layers(10, 0.01, colormap = 'spectral')
cam = ds.camera(c, L, W, N, tf, fields = [args.field], log_fields = [True])

im = cam.snapshot('test_rendering.png')
