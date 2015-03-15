#!/usr/bin/python

import yt
from os.path import join
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='data directory',
    default="/home/miguel/project/hydro/runs/piernik/")
parser.add_argument('-f', '--filename', help='HDF5 file', default="")
parser.add_argument('-a', '--axis', type=int, help='axis', default=2)
args = parser.parse_args()

# Load the dataset.
# ds = yt.load(join(basedir, "roche_tst_0020.h5"))
# Create density slices in all three axes.

def plot_h5(filename):
    ds = yt.load(filename)
    print(ds.field_list)
    print(ds.domain_width)
    p = yt.SlicePlot(ds, args.axis, "deni",
            center=ds.arr([0.5, 0.5, 0.5], 'unitary'),
            origin="native")
    p.save()

if args.filename:
    plot_h5(args.filename)
elif args.dir:
    for i in glob.glob(join(args.dir, '*.h5')):
        plot_h5(i)
else:
    print("Provide file name or directory")
