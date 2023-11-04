import bpy
import os
from random import randrange
import re

# User Parameters
FRAME_RATE = bpy.context.scene.render.fps

# Parameters
BACKGROUND_HEIGHT = 0.0005
BACKGROUND_THICKNESS = 0.00025
BACKGROUND_STRENGTH = 1
BACKGROUND_LEAD_IN_s = 1
BACKGROUND_COLOR = (0.0478408, 0.288436, 0.447972, 1)

ROUTES_HEIGHT = 0.0005
ROUTES_THICKNESS = 0.000125
ROUTES_STRENGTH_INITIAL = 0
ROUTES_STRENGTH_FINAL = 0
ROUTES_LEAD_IN_s = 0
ROUTES_LEAD_OUT_s = 0

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

def delete_all_materials():
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def import_svg(filename):
    new_filename = str(randrange(9999999)) + filename
    os.system(f"cp ../out/{filename} ../out/tmp/{new_filename}") 
#    os.rename(f"../out/{filename}", f"../out/{new_filename}")
    bpy.ops.import_curve.svg(filepath=f"../out/tmp/{new_filename}")
    os.system(f"rm ../out/tmp/{new_filename}")
    svg_collection = bpy.data.collections.get(new_filename)
    return svg_collection

def import_background_map():
    map_collection = import_svg('map.svg')

    for curve in bpy.data.curves:
        curve.extrude = BACKGROUND_HEIGHT
    object_num = 0  
    for object in map_collection.objects:
        object_num+=1
        modifier = object.modifiers.new(name="test", type='SOLIDIFY')
        modifier.thickness = BACKGROUND_THICKNESS
        modifier.offset = 0
        modifier.use_even_offset
        object.location[2] = -BACKGROUND_HEIGHT
    return map_collection

def import_routes():
    route_collections_sorted = []
    route_collections = {}
    for root, dirs, files in os.walk("../out"):
        for file in files:
            if re.search("out[0-9]+.svg", file):
                svg_collection = import_svg(file)
                route_collections[file.split('.')[0].split('out')[1]] = svg_collection
                route_collections_sorted += [file.split('.')[0].split('out')[1]]
                
    route_collections_sorted.sort(key = int)

    for collection_num in route_collections_sorted:
        collection = route_collections.get(collection_num)
        for curve in bpy.data.curves:
            curve.extrude = ROUTES_HEIGHT
        
        object_num = 0  
        for object in collection.objects:
            object_num+=1
            modifier = object.modifiers.new(name="test", type='SOLIDIFY')
            modifier.thickness = ROUTES_THICKNESS
            modifier.offset = 0
            modifier.use_even_offset
            
def create_background_map_material():
    # Create background map material
    bg_map_material_name = "bg_map_material" #+ str(randrange(9999999))
    bpy.data.materials.new(name=bg_map_material_name)
    bg_map_material = bpy.data.materials.get(bg_map_material_name)
    bg_map_material.use_nodes = True


    for node in bg_map_material.node_tree.nodes:
        node_name = node.name
        bg_map_material.node_tree.nodes.remove(bg_map_material.node_tree.nodes.get(node_name))

    bg_map_material.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    bg_map_material.node_tree.nodes.new(type="ShaderNodeEmission")
    bg_map_material.node_tree.links.new(
        bg_map_material.node_tree.nodes["Emission"].outputs["Emission"],
        bg_map_material.node_tree.nodes["Material Output"].inputs["Surface"],
    )

    bg_map_material.node_tree.nodes["Emission"].inputs["Strength"].default_value = 0
    bg_map_material.node_tree.nodes["Emission"].inputs["Color"].default_value = BACKGROUND_COLOR
    bg_map_material.node_tree.nodes["Emission"].inputs["Strength"].keyframe_insert(data_path='default_value', frame = 0)
    bg_map_material.node_tree.nodes["Emission"].inputs["Strength"].default_value = BACKGROUND_STRENGTH
    bg_map_material.node_tree.nodes["Emission"].inputs["Strength"].keyframe_insert(data_path='default_value', frame = FRAME_RATE*BACKGROUND_LEAD_IN_s)
    return bg_map_material

change_working_dir()
delete_all_collections()
delete_all_materials
map_collection = import_background_map()
import_routes()
bg_map_material = create_background_map_material()

for object in map_collection.objects:
    object.active_material = bg_map_material



#bpy.data.materials["bg_map_material"].node_tree.nodes["Emission"].inputs[0].default_value



#for material in bpy.data.materials:
#    bpy.data.materials.remove(material)

#print(background_map_material)
    
    
    
    # for object in collection.objects:
        
#print(str(route_collections_sorted))
    

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

