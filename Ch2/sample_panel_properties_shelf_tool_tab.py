# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Define the meta data that will be listed under this add-on's entry in Edit > Preferences... > Add-ons.
bl_info = {
    "name": "Sample UI Panel in the Properties Shelf > Tool tab",
    "author": "Isabel Lupiani",
    "version": (1, 2, 0),
    "blender": (2, 80, 3),
    "location": "Properties Shelf > Tool > Sample Panel",
    "warning": "",
    "description": "This add-on creates a sample UI Panel in the Properties Shelf > Tool tab",
    "wiki_url": "",    
    "category": "Object", # This is the category the add-on will be listed under Edit > Preferences... > Add-ons
}

import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    IntProperty,
    FloatProperty)

def init_scene_vars():
    # This produces a plain text input field for users 
    # to type in a string.
    bpy.types.Scene.sample_text = StringProperty(
        name = "Text",
        description = "Sample text input",
        maxlen=1024, # Max length of the string.
        subtype = "NONE") # Plain text input field.

    # This produces a text input field with a open-file-dialog 
    # button to its right. Users can use the open-file-dialog 
    # to select a file, or type in the path/name of the file 
    # in the text field.
    bpy.types.Scene.sample_filename = StringProperty(
        name = "Filename",
        description = "Sample filename input",
        maxlen = 1024, # Max length of the string.
        subtype = "FILE_PATH", # Can also be DIR_PATH, FILE_NAME, PASSWORD, etc.
        options = {'SKIP_SAVE'})

    # This produces a checkbox followed by the name variable 
    # specified below. When you hover over name, it displays 
    # description. 
    # If default is set to True, the checkbox is by default 
    # checked.
    bpy.types.Scene.sample_checkbox = bpy.props.BoolProperty(
        name = "Checkbox",
        description = "Sample checkbox",
        default = True)

    # This automatically produces a dropdown list showing 
    # 3 options, "Apple", "Pear", and "Banana". 
    # Notice each entry in the items list is a 3-typle:
    # The 1st element is the internal id, 2nd element is 
    # the text shown in the dropdown, and 3rd element is the 
    # text shown in the tooltip when you hover over the 2nd
    # element in the dropdown. So for example, when you 
    # hover over "Apple" in the dropdown, the tooltip 
    # displays "First fruit".
    bpy.types.Scene.sample_enum = bpy.props.EnumProperty(
        name = "Enum",
        items = (('Apple', "Apple", "First fruit"),
                 ('Pear', "Pear", "Second fruit"),
                 ('Banana', "Banana", "Third fruit")),
        description = "Sample enum",
        default = 'Apple')

    # min and max are HARD constraints, preventing users from 
    # sliding the widget outside of this range. Any number typed 
    # in larger than max will be clamped to max, and any number 
    # typed in smaller than min will be clamped to min.
    bpy.types.Scene.sample_int = bpy.props.IntProperty(
        name = "Integer",
        description = "Sample integer input",
        default = 30,
        min = 20,
        max = 40)

    # By specifying the subtype as PERCENTAGE the widget 
    # will automatically show a % sign to let users know 
    # they are entering a percentage. 
    bpy.types.Scene.sample_int_pcrt = bpy.props.IntProperty(
        name = "Percentage",
        description = "Sample integer percentage input",
        default = 50,
        min = 10,
        max = 100,
        subtype = 'PERCENTAGE')

    # Notice that soft_min and soft_max impose soft constraints 
    # on the input range (think of it as a recommended range) and 
    # prevents users from sliding the widget outside of this range. 
    # However, users are still able to manually type in any number
    # regardless of soft_min/soft_max. 
    bpy.types.Scene.sample_float = bpy.props.FloatProperty(
        name = "Float",
        description = "Sample float input",
        default = 0.0,
        soft_min = -5.0,
        soft_max = 5.0)

def del_scene_vars():
    del bpy.types.Scene.sample_text
    del bpy.types.Scene.sample_filename
    del bpy.types.Scene.sample_checkbox
    del bpy.types.Scene.sample_enum
    del bpy.types.Scene.sample_int
    del bpy.types.Scene.sample_int_pcrt
    del bpy.types.Scene.sample_float

class SAMPLE_PT_Shelf(bpy.types.Panel):
    bl_label = "Sample Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Tool'
    """Sample UI panel located in the Properties Shelf > Tool tab."""

    def draw(self, context):
        layout = self.layout
        col0 = layout.column()
        box0 = col0.box()

        # Display the properties.
        r = box0.row(align = True)
        r.prop(context.scene, "sample_text")
        r = box0.row(align = True)
        r.prop(context.scene, "sample_filename")
        r = box0.row(align = True)
        r.prop(context.scene, "sample_checkbox")
        r = box0.row(align = True)
        r.prop(context.scene, "sample_enum")
        r = box0.row(align = True)
        r.prop(context.scene, "sample_int")
        r = box0.row(align = True)
        r.prop(context.scene, "sample_int_pcrt")
        r = box0.row(align = True)
        r.prop(context.scene, "sample_float")

        # Display the user entered values. You should see them change as you 
        # edit the properties above.
        box1 = col0.box()
        box1.label(text = "User Entered Values:", icon = 'TEXT')
        r = box1.row(align = True)
        r.label(text = "Text: " + str(context.scene.sample_text))
        r = box1.row(align = True)
        r.label(text = "Filename: " + str(context.scene.sample_filename))
        r = box1.row(align = True)
        r.label(text = "Checkbox: " + str(context.scene.sample_checkbox))
        r = box1.row(align = True)
        r.label(text = "Enum: " + str(context.scene.sample_enum))
        r = box1.row(align = True)
        r.label(text = "Integer: " + str(context.scene.sample_int))
        r = box1.row(align = True)
        r.label(text = "Percentage: " + str(context.scene.sample_int_pcrt) + "%")
        r = box1.row(align = True)
        r.label(text = "Float: " + str(context.scene.sample_float))

        # Display the names of the current scene objects.
        box2 = col0.box()
        box2.label(text = "Scene Objects:", icon = 'OBJECT_DATA')
        for ob in context.scene.objects:
            r = box2.row(align = True)
            r.label(text = str(ob.name))

classes = [SAMPLE_PT_Shelf]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    init_scene_vars()

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del_scene_vars()

if __name__ == "__main__":
    register()