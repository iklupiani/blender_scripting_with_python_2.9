import bpy 
import bmesh
from mathutils import Vector
from math import radians
import math

def add_cone_once(context, location = (0, 0, 0), vertices = 8, radius1 = 2.0, depth = 3.0):
    if context.scene.objects.find('Cone') < 0: 
        if context.view_layer.objects.active is not None: 
            bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.mesh.primitive_cone_add(location = location, vertices = vertices, \
        radius1 = radius1, depth = depth) 

def get_object_hard_copy(context, obj):
    context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj_copy = bpy.data.objects.new(name = obj.name + '_copy', object_data = obj.data.copy())
    context.collection.objects.link(obj_copy)
    context.view_layer.update()
    return obj_copy

def get_object_soft_copy(context, obj):
    context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj_copy = bpy.data.objects.new(name = obj.name + '_soft_copy', object_data = obj.data)
    context.collection.objects.link(obj_copy)
    context.view_layer.update()
    return obj_copy

def bmesh_from_existing():
    add_cone_once(bpy.context, (2, 3, 3), 16, 1.5, 5.0)
    cone = bpy.data.objects['Cone']
    cone_copy = get_object_hard_copy(bpy.context, cone) 
    cone_copy.location = cone.location + Vector((0, -6, 0))
    cone_copy_mirror_mod = cone_copy.modifiers.new('mirror_mod', 'MIRROR') 
    cone_copy_mirror_mod.show_in_editmode = True
    cone_copy_mirror_mod.use_clip = True
    cone_copy_mirror_mod.use_axis[0] = False  
    cone_copy_mirror_mod.use_axis[1] = False 
    cone_copy_mirror_mod.use_axis[2] = True   
    cone_copy_subsurf_mod = cone_copy.modifiers.new('subsurf_mod', 'SUBSURF') 
    cone_copy_subsurf_mod.levels = 1
    
    if bpy.context.view_layer.objects.active is not None: 
        bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.view_layer.objects.active = cone_copy
    bpy.ops.object.mode_set(mode = 'EDIT')

    bm = bmesh.from_edit_mesh(cone_copy.data) 
    bmesh.ops.scale(bm, vec = (1, 2, 0.5), verts = bm.verts) 
    bmesh.update_edit_mesh(cone_copy.data) 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
def get_placeholder_mesh_obj_and_bm(context, name, location = Vector((0, 0, 0))):
    mesh_placeholder = bpy.data.meshes.new(name = name)
    obj_placeholder = bpy.data.objects.new(name = name, object_data = mesh_placeholder)
    obj_placeholder.location = location
    context.collection.objects.link(obj_placeholder)
    context.view_layer.objects.active = obj_placeholder
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(mesh_placeholder)
    return bm, obj_placeholder
    
def bmesh_from_scratch():
    bm, obj_scratch = get_placeholder_mesh_obj_and_bm(bpy.context, 'from_scratch', Vector((0, 0, 0)))   
    bm = bmesh.from_edit_mesh(obj_scratch.data)
    bpy.ops.mesh.primitive_monkey_add(location = (0, -5, -5), rotation = (0, 0, 0), size = 2.5)
    bpy.ops.mesh.primitive_monkey_add(location = (0, 0, 0), rotation = (0, 0, radians(45)), size = 2)
    bpy.ops.mesh.primitive_monkey_add(location = (0, 5, 5), rotation = (0, 0, radians(90)), size = 1.5)
    bmesh.update_edit_mesh(obj_scratch.data)
    
def bmesh_as_sketch_pad():     
    add_cone_once(bpy.context, (2, 5, 3), 16, 1.5, 5.0)
    cone = bpy.data.objects['Cone']
    cone_copy_1 = get_object_hard_copy(bpy.context, cone)
    cone_copy_1.location = cone.location + Vector((0, -4, 0))
    cone_copy_2 = get_object_hard_copy(bpy.context, cone)
    cone_copy_2.location = cone.location + Vector((0, -9, 0))    
    
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends = True, segments = 8, radius = 1)
    bm.to_mesh(cone_copy_1.data)
    bm.to_mesh(cone_copy_2.data)
        
def add_circle(bm, radius, num_segments, z):
    verts_added = []
    v_prev = None
    v0 = None    
    for segment in range(num_segments):
        theta = (segment / num_segments) * 2 * math.pi
        v = bm.verts.new(Vector((radius*math.cos(theta), radius*math.sin(theta), z)))
        verts_added.append(v)
        if segment == 0:
            v0 = v
        if v_prev:
            bm.edges.new([v_prev, v])
        if segment == num_segments - 1:
            bm.edges.new([v, v0])
        v_prev = v
    return verts_added
        
def generate_barrel(context, name, radius_end, radius_mid, height, num_segments, \
    center = Vector((0, 0, 0))):
    bm, barrel_obj = get_placeholder_mesh_obj_and_bm(bpy.context, name, center)
    
    bottom_cap_verts = add_circle(bm, radius_end, num_segments, -height/2)
    add_circle(bm, radius_mid, num_segments, 0)
    top_cap_verts = add_circle(bm, radius_end, num_segments, height/2)
    
    bm.faces.new(top_cap_verts)
    bm.faces.new(bottom_cap_verts)
    
    bmesh.ops.bridge_loops(bm, edges = bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces = bm.faces)
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.subdivide(smoothness = 1.1)
    
    bmesh.update_edit_mesh(barrel_obj.data)
    context.view_layer.update()    

# Sample Usage
#add_cone_once(bpy.context)
#get_object_hard_copy(bpy.context, bpy.context.scene.objects['Cone'])
#get_object_soft_copy(bpy.context, bpy.context.scene.objects['Cone'])

#bmesh_from_existing()
#bmesh_from_scratch()
#bmesh_as_sketch_pad()

generate_barrel(bpy.context, 'test_barrel', radius_end = 3, radius_mid = 5, height = 10, num_segments = 16, center = Vector((0, 0, 5)))
generate_barrel(bpy.context, 'test_tall_slim_barrel', radius_end = 1.5, radius_mid = 3, height = 15, num_segments = 16, center = Vector((0, 12, 7.5)))
generate_barrel(bpy.context, 'test_bar_stool', radius_end = 5, radius_mid = 2, height = 7, num_segments = 16, center = Vector((12, 0, 3.5)))