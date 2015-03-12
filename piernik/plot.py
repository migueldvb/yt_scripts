#!/usr/bin/python2

import yt
from os.path import join
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='data directory',
    default="/home/miguel/project/hydro/runs/piernik/")
args = parser.parse_args()

# Load the dataset.
# ds = yt.load(join(basedir, "roche_tst_0020.h5"))
# Create density slices in all three axes.

for i in glob.glob(join(args.dir, '*.h5')):
    ds = yt.load(i)
    print(ds.field_list)
    print(ds.domain_width)
    p = yt.SlicePlot(ds, "z", "deni")
    p.save()
