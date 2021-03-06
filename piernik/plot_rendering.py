#!/usr/bin/python

import yt
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='HDF5 file', default="")
parser.add_argument('--field', help='field variable', default="density",
        choices=('density', 'velocity_x', 'velocity_y',
            'dens', 'denn', 'dend', 'deni', 'vlxi', 'vlyi', 'vlzi'))
parser.add_argument('-l', '--linear', action='store_false',
        dest='log', help='linear scale', default=True)
parser.add_argument('-c', '--colormap', help='colormap', default="jet")
parser.add_argument('-n', '--number', default=10,
        help='Number of Gaussians')
args = parser.parse_args()

ds = yt.load(args.filename)

# Find the bounds in log space of for your field
dd = ds.all_data()
mi, ma = dd.quantities.extrema(args.field)

if args.log:
    mi, ma = np.log10(mi), np.log10(0.4*ma)

# Instantiate the ColorTransferfunction.
tf = yt.ColorTransferFunction((mi, ma))

print(ds)
c = (ds.domain_right_edge + ds.domain_left_edge)/2.0
W = (ds.domain_right_edge - ds.domain_left_edge)[0]
# N = np.array([1024, int(np.arctan(20*np.pi/180)*1024)])
N = 1024

# tf.add_layers(10, 0.01, colormap = 'RdBu_r')
tf.add_layers(args.number, 0.01, colormap = args.colormap)

for t in range(20):
    phi = -t/19.*2*np.pi - np.pi/2.
    x = np.cos(phi)
    y = np.sin(phi)
    L = np.array([x, y, np.tan(20*np.pi/180)])
    cam = ds.camera(c, L, W, N, tf,
        north_vector=[0., 0., 1.],
        fields = [args.field], log_fields = [True])

    im = cam.snapshot('{0}_rendering_{1:02d}.png'.format(args.filename[:-3], t))

# nim = cam.draw_domain(im)
# im = cam.snapshot('{0}_rendering_with_grid.png'.format(args.filename[:-3]))
