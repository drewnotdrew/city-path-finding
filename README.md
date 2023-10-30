# City Path Finding

## Getting Started

This project primarly uses OSMnx, which is easiest to install through a conda environment. Instructions [here](https://osmnx.readthedocs.io/en/stable/installation.html).

## Requirements

- Anaconda
- OSMnx

## Layout

`animslower.gif` is the video of the Dijkstra's (red) and A* (green) on the same map, attempting to find the bottom right corner. A* is using a heuristic that is the geographic distance between two nodes. `anim.gif` is the same but 5x faster. `test.py` generates the frames for these animations, using OSMnx and a custom-modified NetworkX. `makevid.py` turns these frames into a GIF. `blender/` is our attempt at doing this in Blender. `examples/` is example OSMnx code we copied for quick reference. `out/` is where the output from `test.py` is put, but we didn't save all these frames becaues there's too many.
