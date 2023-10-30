import bpy
import os

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

# Change to relative working directory
def change_working_dir():
    blender_main_dir = os.path.dirname(os.path.realpath(__file__))
    path, file = os.path.split(blender_main_dir)
    os.chdir(path) 