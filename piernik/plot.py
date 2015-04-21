#!/usr/bin/python2

import yt
from os.path import join
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='data directory',
    default="/home/miguel/project/hydro/runs/piernik/")
parser.add_argument('-f', '--filename', help='HDF5 file', default="")
parser.add_argument('-a', '--axis', type=int, help='axis', default=2)
parser.add_argument('--field', help='field variable', default="density",
        choices=('density', 'velocity_x', 'velocity_y',
            'dens', 'denn', 'dend', 'deni',
            'vlxi', 'vlyi', 'vlzi', 'vlxn', 'vlyn', 'vlzn',
            'velx', 'vely', 'velz'))
parser.add_argument('-v', '--vel', action='store_true',
        help='annotate velocity', default=False)
parser.add_argument('--vel_norm', action='store_true',
        help='normalize annotate velocity', default=False)
parser.add_argument('--vel_factor', type=int,
        help='annotate velocity', default=32)
parser.add_argument('-l', '--linear', action='store_false',
        dest='log', help='linear scale', default=True)
args = parser.parse_args()

# Load the dataset.
# ds = yt.load(join(basedir, "roche_tst_0020.h5"))
# Create density slices in all three axes.

def plot_h5(filename):
    ds = yt.load(filename)
    if args.axis==1:
        # Flip the x and y axis for 'y' normal axis
        # http://nbviewer.ipython.org/gist/ngoldbaum/0f9ebc92ca7422ded2d5
        ds.coordinates.x_axis['y'] = 0
        ds.coordinates.x_axis[1] = 0
        ds.coordinates.y_axis['y'] = 2
        ds.coordinates.y_axis[1] = 2

    print(ds.field_list)
    print(ds.domain_width)
    p = yt.SlicePlot(ds, args.axis, args.field,
            axes_unit='au',
#             center=([0.5, 0.5, 0.5], 'unitary'),
            origin="native")
    p.set_log(args.field, args.log)
    if args.vel:
        p.annotate_velocity(factor = args.vel_factor, normalize=args.vel_norm)
    p.save()

if args.filename:
    plot_h5(args.filename)
elif args.dir:
    for i in glob.glob(join(args.dir, '*.h5')):
        plot_h5(i)
else:
    print("Provide file name or directory")
