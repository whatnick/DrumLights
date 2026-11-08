"""Blender turntable of the KiCad GLB export with animated lighting.
Run: blender -b -P render_turntable.py -- <in.glb> <out_prefix> [frames] [still_only]
"""
import sys, math, os
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
glb, out = argv[0], argv[1]
frames = int(argv[2]) if len(argv) > 2 else 120
still = len(argv) > 3

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)

bpy.context.view_layer.update()
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
center, size = (lo + hi) / 2, max((hi - lo).length, 1e-6)
print("bounds", lo, hi, "size", size)

# Pivot empty for rotation about the board centre (KiCad GLB is Y-up -> Z-up after import)
pivot = bpy.data.objects.new("pivot", None)
bpy.context.scene.collection.objects.link(pivot)
pivot.location = center
bpy.context.view_layer.update()
for o in bpy.context.scene.objects:
    if o.parent is None and o is not pivot:
        mw = o.matrix_world.copy()
        o.parent = pivot
        o.matrix_world = mw
pivot.rotation_euler = (0, 0, 0)
pivot.keyframe_insert("rotation_euler", frame=1)
pivot.rotation_euler = (0, 0, math.radians(360))
pivot.keyframe_insert("rotation_euler", frame=frames + 1)
for fc in pivot.animation_data.action.fcurves if hasattr(pivot.animation_data.action, "fcurves") else []:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"

# Ground plane for reflections/shadows
bpy.ops.mesh.primitive_plane_add(size=size * 8, location=(center.x, center.y, lo.z - size * 0.01))
gp = bpy.context.object
gm = bpy.data.materials.new("ground")
gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.025, 1)
gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.35
gp.data.materials.append(gm)

# Camera
cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 60
cam_d.clip_start = size * 0.01
cam_d.clip_end = size * 100
cam = bpy.data.objects.new("cam", cam_d)
bpy.context.scene.collection.objects.link(cam)
cam.location = center + Vector((0, -size * 2.6, size * 2.0))
tr = cam.constraints.new("TRACK_TO")
tr.target = pivot
tr.track_axis, tr.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
bpy.context.scene.camera = cam

# World
w = bpy.data.worlds.new("w")
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.01, 0.01, 0.015, 1)
bg.inputs[1].default_value = 1.0
bpy.context.scene.world = w

# Variable lighting: key/rim area lights cycle colour + intensity; fill pulses
def area(name, loc, energy, color):
    d = bpy.data.lights.new(name, "AREA")
    d.size = size
    d.energy = energy
    d.color = color
    o = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(o)
    o.location = center + Vector(loc) * size
    c = o.constraints.new("TRACK_TO")
    c.target = pivot
    c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    return d

KEY_E = 0.25
key = area("key", (1.2, -1.0, 1.6), KEY_E, (1, 1, 1))
rim = area("rim", (-1.4, 1.2, 0.9), 0.2, (0.2, 0.4, 1))
fill = area("fill", (0.0, -1.6, 0.6), 0.05, (1, 0.7, 0.4))

cols = [(1, 1, 1), (1, 0.15, 0.1), (0.1, 1, 0.2), (0.15, 0.25, 1), (1, 0.8, 0.1), (1, 1, 1)]
for i, c in enumerate(cols):
    f = 1 + round(i * frames / (len(cols) - 1))
    rim.color = c
    rim.keyframe_insert("color", frame=f)
    key.energy = KEY_E * (0.35 if i % 2 else 1.0)
    key.keyframe_insert("energy", frame=f)
    fill.color = cols[(i + 2) % len(cols)]
    fill.keyframe_insert("color", frame=f)

sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.frame_start, sc.frame_end = 1, frames
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.view_settings.view_transform = "Standard"
if still:
    sc.frame_set(1)
    sc.render.filepath = out + "_still.png"
    bpy.ops.render.render(write_still=True)
else:
    sc.render.image_settings.media_type = "VIDEO"
    sc.render.image_settings.file_format = "FFMPEG"
    sc.render.ffmpeg.format = "MPEG4"
    sc.render.ffmpeg.codec = "H264"
    sc.render.fps = 30
    sc.render.filepath = out + "_"
    bpy.ops.render.render(animation=True)

