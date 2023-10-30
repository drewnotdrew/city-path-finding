import bpy
import os
from random import randrange

# Change to relative working directory
def change_working_dir():
    blender_main_dir = os.path.dirname(os.path.realpath(__file__))
    path, file = os.path.split(blender_main_dir)
    os.chdir(path) 

# Print to console for debugging
def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

# Delete all collections in current file
def delete_all_collections():
    for collection in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(collection)
        
def delete_all():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

def import_svg(filename):
    new_filename = str(randrange(9999999)) + filename
    os.system(f"cp ../out/{filename} ../out/tmp/{new_filename}") 
#    os.rename(f"../out/{filename}", f"../out/{new_filename}")
    bpy.ops.import_curve.svg(filepath=f"../out/tmp/{new_filename}")
    svg_collection = bpy.data.collections.get(new_filename)
    return svg_collection

def import_background_map():
    map_collection = import_svg('map.svg')
    for object in map_collection.objects:
       curve_name = object.name
       print(curve_name)
       print(object.type)

    for curve in bpy.data.curves:
        curve.extrude = 0.0005
    object_num = 0  
    for object in map_collection.objects:
        object_num+=1
        print(object_num)
        modifier = object.modifiers.new(name="test", type='SOLIDIFY')
        modifier.thickness = 0.0005
        modifier.offset = 0
        modifier.use_even_offset
        object.location[2] = -0.0005

change_working_dir()
delete_all_collections()
import_background_map()
# Import background map

#    object.modifiers.new(name=f"solidify{object_num}", type='SOLIDIFY')
#    bpy.data.objects[object.name].modifiers["solidify{object_num}"].thickness = 0.0069
    # object.modifiers[f"solidify{object_num}"].thickness = 0.0005
    # bpy.context.object.modifiers[f"solidify{object_num}"].thickness = 0.0005
        # bpy.data.objects["Curve.73874"].modifiers["test"].thickness

# bpy.data.objects[0].modifiers

# for curve in bpy.data.curves:
#     curve.extrude = 0.0005

#     bpy.types.CurveModifier.object = curve
    # print(curve.name)
    # curve.extrude=0.0005
 #   bpy.context.curves

# for curve in bpy.data.curves:
#     curve.modifiers["Solidify"].thickness = 0.0005
#     bpy.context.curve.

#     curve.dat
#     curve.object.modifier_add
#     bpy.data.objects["Curve.40823"].modifiers["Solidify"].offset
#    print(curve.users_collection)
#bpy.data.curves["Curve.33186"].extrude
#bpy.data.curves["Curve.33186"].name
# for i in range(0,len(map_collection.objects)):
#     curve_name = bpy.data.objects[0].name
#     bpy.data.curves[curve_name].extrude
#     print(curve_name)
# #    print(bpy.data.objects[0].name)


#bpy.data.objects["Curve.37927"].modifiers["Solidify"].name

#print(len(map_collection.objects))



## Delete all edges but the path; hardcoded for now
#for curve in route_collection.objects:
#    if curve.name != "Curve.948":
#        bpy.data.objects.remove(curve, do_unlink=True)

