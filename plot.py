#!/usr/bin/python2

import yt
from os.path import join

# Load the dataset.
basedir = "/home/miguel/mnt/piernik/runs/roche"
ds = yt.load(join(basedir, "roche_tst_0020.h5"))

# Create density slices in all three axes.
print(ds.field_list)
print(ds.domain_width)

for i in range(33):
    ds = yt.load(join(basedir, "roche_tst_00{:02d}.h5".format(i)))
    p = yt.SlicePlot(ds, "z", "denn")
    p.save()
