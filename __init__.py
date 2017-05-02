import bpy
import os

bl_info = {
 "name": "Unity Tools",
 "description": "Tools to batch export fbx files",
 "author": "Don-Duong Quach",
 "blender": (2, 7, 8),
 "version": (1, 1, 0),
 "category": "Unity",
 "location": "",
 "warning": "",
 "wiki_url": "",
 "tracker_url": "",
}

class UnityBatchExportPanel(bpy.types.Panel):
    """ Unity Tools panel on the toolbar tab 'Tools' """
    bl_category = "Unity Tools"
    bl_idname = "LOQ_unity_tools"
    bl_label = "Unity Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):

        layout = self.layout


        # batch export
        col = layout.column(align=True)
        col.prop(context.scene, 'loq_batch_export_path')
        row = col.row(align=True)
        row.operator("loq.batch_export", text="Batch Export", icon='EXPORT')
        col = layout.column(align=True)
        col.prop(context.scene, 'loq_export_name')
        row = col.row(align=True)
        row.operator("loq.single_export", text="Single Export", icon='EXPORT')

        # apply location
        col = layout.column(align=True)
        col.label(text="Location Export")

        col = layout.column(align=True)
        col.prop(context.scene, 'loq_location_export', text="Location Export", expand=True)

        col = layout.column(align=True)
        col.prop(context.scene, "loq_fix_rotation", text="Fix Rotation") 

        col = layout.column(align=True)
        col.prop(context.scene, "loq_export_scale", text="Export Scale") 

class LoqBatchExport(bpy.types.Operator):
    bl_idname = "loq.batch_export"
    bl_label = "Batch Export"

    def execute(self, context):
        print ("execute Loq_batch_export")
        bpy.ops.ed.undo_push() # all changes will be undone below

        if context.scene.loq_batch_export_path == "":
            raise Exception("Export path not set")

        if len(bpy.context.selected_objects) == 0:
            raise Exception("No objects selected for export")

        col = bpy.context.selected_objects

        # convert path to windows friendly notation
        dir = os.path.dirname(bpy.path.abspath(context.scene.loq_batch_export_path))
        # cursor to origin

        for obj in col:
            # select only current object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select = True

            if context.scene.loq_location_export == "A":
                bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
            elif context.scene.loq_location_export == "Z":
                obj.location = (0, 0, 0)

            apply_fix_rotation(obj)

            # set pivot point to cursor location
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # use mesh name for file name
            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(dir, name)
            print("exporting: " + fn)
            # export fbx
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, axis_forward='-Z', axis_up='Y', global_scale=context.scene.loq_export_scale, apply_unit_scale=False )

        bpy.ops.ed.undo() # clean up

        return {'FINISHED'}

class LoqSingleExport(bpy.types.Operator):
    bl_idname = "loq.single_export"
    bl_label = "Single Export"

    def execute(self, context):
        print ("execute Loq_single_export")
        bpy.ops.ed.undo_push() # all changes will be undone below

        if context.scene.loq_batch_export_path == "":
            raise Exception("Export path not set")

        if len(bpy.context.selected_objects) == 0:
            raise Exception("No objects selected for export")

        col = bpy.context.selected_objects

        # convert path to windows friendly notation
        dir = os.path.dirname(bpy.path.abspath(context.scene.loq_batch_export_path))

        for obj in col:
            # select only current object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select = True

            if context.scene.loq_location_export == "A":
                bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
            elif context.scene.loq_location_export == "Z":
                obj.location = (0, 0, 0)

            apply_fix_rotation(obj)

        for obj in col:
            obj.select = True

        if context.scene.loq_export_name == "":
            # use mesh name for file name
            name = bpy.path.clean_name(col[-1].name)
        else:
            name = context.scene.loq_export_name
        fn = os.path.join(dir, name)
        print("exporting: " + fn)
        # export fbx
        bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, axis_forward='-Z', axis_up='Y', global_scale=context.scene.loq_export_scale, apply_unit_scale=False )

        bpy.ops.ed.undo()
        return {'FINISHED'}

def apply_fix_rotation(obj):
    bpy.ops.object.transform_apply(rotation = True)
    bpy.ops.transform.rotate(value = -1.5708, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')
    
    bpy.ops.object.transform_apply(rotation = True)
    bpy.ops.transform.rotate(value = 1.5708, axis = (1, 0, 0), constraint_axis = (True, False, False), constraint_orientation = 'GLOBAL')

    for child in obj.children:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True
        apply_fix_rotation(child)

# registers
def register():
    bpy.types.Scene.loq_batch_export_path = bpy.props.StringProperty (
        name="Path",
        default="",
        description="Define the path where to export",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.loq_export_name = bpy.props.StringProperty (
        name="Single Name",
        default="",
        description="Name of object for single export",
        subtype="FILE_NAME"
    )
    bpy.types.Scene.loq_location_export = bpy.props.EnumProperty(
        name = "Location Export",
        items =(
            ("P", "Pass", "Location is passed through unmodified"),
            ("A", "Apply", "Apply Location to Object's mesh"),
            ("Z", "Zero", "Move object to origin")
        ),
        default="P",
        description="Location Export Option"
        )
    bpy.types.Scene.loq_export_scale = bpy.props.FloatProperty(default=1, min=0.01, description="Scale all data according to current Blender size to match default FBX unit, centimeter.")

    bpy.utils.register_class(UnityBatchExportPanel)
    bpy.utils.register_class(LoqBatchExport)
    bpy.utils.register_class(LoqSingleExport)

def unregister():
    del bpy.types.Scene.loq_batch_export_path
    del bpy.types.Scene.loq_export_name
    del bpy.types.Scene.loq_location_export
    del bpy.types.Scene.loq_export_scale

    bpy.utils.unregister_class(UnityBatchExportPanel)
    bpy.utils.unregister_class(LoqBatchExport)
    bpy.utils.unregister_class(LoqSingleExport)

if __name__ == "__main__":
    register()
