#!/usr/bin/python2

import yt
from os.path import join
import argparse
import glob
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='data directory',
    default="/home/miguel/project/hydro/runs/piernik/")
parser.add_argument('-f', '--filename', help='HDF5 file', default="")
parser.add_argument('-a', '--axis', type=int, help='axis', default=2)
parser.add_argument('--field', help='field variable', default="density",
        choices=('density', 'velocity_x', 'velocity_y', 'temperature',
            'specific_energy',
            'dens', 'denn', 'dend', 'deni',
            'vlxi', 'vlyi', 'vlzi', 'vlxn', 'vlyn', 'vlzn',
            'velx', 'vely', 'velz'))
parser.add_argument('-v', '--vel', action='store_true',
        help='annotate velocity', default=False)
parser.add_argument('-p', '--proj', action='store_true',
        help='plot projection', default=False)
parser.add_argument('--vel_norm', action='store_true',
        help='normalize annotate velocity', default=False)
parser.add_argument('--stream', action='store_true',
        help='annotate streamlines', default=False)
parser.add_argument('--vel_factor', type=int,
        help='annotate velocity', default=32)
parser.add_argument('-l', '--linear', action='store_false',
        dest='log', help='linear scale', default=True)
parser.add_argument('-n', '--normal', nargs=3, type=int,
        help='vector normal to cutting plane')
args = parser.parse_args()

# Load the dataset.
# ds = yt.load(join(basedir, "roche_tst_0020.h5"))
# Create density slices in all three axes.

def flip(ds):
    # Flip the x and y axis for 'y' normal axis
    # http://nbviewer.ipython.org/gist/ngoldbaum/0f9ebc92ca7422ded2d5
    ds.coordinates.x_axis['y'] = 0
    ds.coordinates.x_axis[1] = 0
    ds.coordinates.y_axis['y'] = 2
    ds.coordinates.y_axis[1] = 2

def plot_h5(filename):
    ds = yt.load(filename)
    if args.axis==1: flip(ds)

    print(ds.field_list)
    print(ds.domain_width)
    if args.normal:
        L = args.normal
        north_vector = [0,0,1]
        W = (ds.domain_right_edge - ds.domain_left_edge)[0]
        cut = yt.SlicePlot(ds, L, args.field, width=W,
                            axes_unit='au',
                            north_vector=north_vector)
        cut.save()
    else:
        p = yt.SlicePlot(ds, args.axis, args.field,
                axes_unit='au',
#             center=([0.5, 0.5, 0.5], 'unitary'),
                origin="native"
                )
        p.set_log(args.field, args.log)
        if args.vel:
            p.annotate_velocity(factor = args.vel_factor, normalize=args.vel_norm)
        if args.stream:
            p.annotate_streamlines('velocity_x', 'velocity_y')
        p.save()

def plot_projection(filename):
    ds = yt.load(filename)
    print(ds.field_list)
    print(ds.domain_width)

    if args.normal:
        L = args.normal
        north_vector = [0,0,1]
        c = (ds.domain_right_edge + ds.domain_left_edge)/2.0
        print(ds.domain_right_edge - ds.domain_left_edge)
        W = (ds.domain_right_edge - ds.domain_left_edge)[0::2]
        W = (ds.domain_right_edge - ds.domain_left_edge)[0]
        N = 1024
#         prj = yt.OffAxisProjectionPlot(ds, L, args.field,
#                     center=c, width=W, axes_unit='au',
#                     north_vector=north_vector)
#         prj.save()
        ratio = L[2]/np.linalg.norm(L)*0.95
        print(ratio)
        image = yt.off_axis_projection(ds, c, L, W, N, args.field)
        yt.write_image(np.log10(image[N/2-int(ratio*N):N/2+int(ratio*N),:]),
                        "{0}_offaxis_projection.png".format(ds))
    else:
        if args.axis==1: flip(ds)
        prj = yt.ProjectionPlot(ds, args.axis, args.field,
                                    axes_unit='au'
                                    )
        prj.set_log(args.field, args.log)
        prj.save()

if args.proj:
    fplot = plot_projection
else:
    fplot = plot_h5

if args.filename:
    fplot(args.filename)
elif args.dir:
    for i in glob.glob(join(args.dir, '*.h5')):
        fplot(i)
else:
    print("Provide file name or directory")
