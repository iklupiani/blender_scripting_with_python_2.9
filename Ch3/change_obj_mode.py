import bpy

if bpy.context.scene.objects.find('Cube') >= 0:
    cube = bpy.context.scene.objects['Cube']
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.view_layer.update()
