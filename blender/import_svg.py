import bpy
import os

# Change to relative working directory
blender_main_dir = os.path.dirname(os.path.realpath(__file__))
path, file = os.path.split(blender_main_dir)
os.chdir(path)

# Import path svg
filename = 'route.svg'
bpy.ops.import_curve.svg(filepath=f"../out/{filename}")
route_collection = bpy.data.collections.get(filename)
collection_items = len(route_collection.objects)

# Delete all edges but the path; hardcoded for now
for curve in route_collection.objects:
    if curve.name != "Curve.948":
        bpy.data.objects.remove(curve, do_unlink=True)
