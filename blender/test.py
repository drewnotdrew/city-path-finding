import bpy

# Create a new curve object
bpy.ops.curve.primitive_bezier_curve_add(radius=2, location=(0, 0, 0))
curve_obj = bpy.context.active_object

# Access the curve data
curve_data = curve_obj.data

# Add a Simple Deform modifier
modifier = curve_obj.modifiers.new(name="Simple Deform", type='SIMPLE_DEFORM')

# Set the modifier properties
modifier.deform_method = 'BEND'
modifier.angle = 1.0  # Set the bend angle

# Apply the modifier (optional)
# Uncomment the next line if you want to apply the modifier
# bpy.ops.object.modifier_apply({"object": curve_obj}, modifier=modifier.name)
