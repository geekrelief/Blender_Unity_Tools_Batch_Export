# Blender Unity Tools Batch Exporter

Blender's normal FBX export results in a mesh with the incorrect orientation when loaded into Unity.
This addon fixes the rotation issue with exported FBX files without you having to 
manually rotate the objects in either Blender or Unity.

## Installing
Download the repo as a .zip file.

Install the addon as a .zip file using Blender's "Install From File" option.

A Unity Tools panel will appear in the ToolShelf.

## Function
Select objects in your scene and click on Batch Export to export each object separately.
The exported object's name will be the same as in the Outline.

Single Export can be used to export one or more objects grouped as one object.  The Single Name field is used to name the exported object for Single Export.  If left empty, the name of first object selected is used.

The Location Export radio option can be set to pass through the location to the exported object (Pass), apply the location to the mesh (Apply), or move the object to the origin (Zero).

Export Scale let's you adjust the scale of all the meshes.

## Shortcuts
* Single Export press Ctrl + E 
* Batch Export is Ctrl + Shift + E

You can modify the shortcuts in the Input Panel listed under 
3D View -> 3D View (Global) -> "Single FBX Export For Unity"
and "Batch FBX Export for Unity"
