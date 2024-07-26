import unreal
import os
import tkinter
import re
from tkinter import filedialog


def create_child_blueprint(parent_class_name, package_path, child_class_name):
    print("Creating child blueprint")
    # Get AssetTools instance
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Find the parent Blueprint class
    parent_class = unreal.EditorAssetLibrary.load_blueprint_class(parent_class_name)

    # If parent class is found
    if parent_class:
        # Set up the BlueprintFactory
        factory = unreal.BlueprintFactory()
        factory.set_editor_property('ParentClass', parent_class)

        # Create the child Blueprint class
        new_asset = asset_tools.create_asset(
            asset_name=child_class_name,
            package_path=package_path,
            asset_class=unreal.Blueprint,
            factory=factory
        )

        if new_asset:
            asset = package_path+child_class_name+"."+child_class_name
            print("Created child Blueprint: ", asset)
            return asset    #Path to new BP
    
def set_blueprint_properties(BPpath, check, name, filename) : 
    print("Setting blueprint properties")

    #Get Blueprint Class to Actor Class
    bpgen = unreal.load_object(None, BPpath)
    bpdef = unreal.get_default_object(bpgen)

    #Add a Skeletal Mesh
    SkeletalMesh = unreal.EditorAssetLibrary.load_asset('/Game/Imports/AutoImports/'+ filename + '/' + filename + '.' + filename )
    bpdef.set_editor_property("SkeletalMeshAsset", SkeletalMesh)

    #Add Texture
    Texture = []
    for Skeletalmaterial in SkeletalMesh.materials :
        material = Skeletalmaterial.material_interface.get_base_material()
        TexturePath = str(unreal.MaterialEditingLibrary.get_used_textures(material)[0])
        pattern = r"([^/]+)\.([^']+)"
        match = re.search(pattern, TexturePath.split('/')[-1])
        TextureName = match.group(0)
    
        Texture.append(unreal.EditorAssetLibrary.load_asset('/Game/Imports/AutoImports/'+ filename + '/' + TextureName))

    bpdef.set_editor_property("Textures", Texture)

    #Tag
    bpdef.set_editor_property("Tags", [name])

def set_animations_properties(filename) :
    bpgen = unreal.load_object(None, '/Game/Imports/AutoImports/' + filename + '.' + filename + '_C')
    bpdef = unreal.get_default_object(bpgen)

    animations = []
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path('/Game/Imports/AutoImports/' + filename)
    for asset in assets : 
        if asset.get_class() == unreal.AnimSequence.static_class() :
            asset_path = '/Game/Imports/AutoImports/' + filename + '/' + str(asset.asset_name) + '.' + str(asset.asset_name)
            unreal.AnimationLibrary.set_is_root_motion_lock_forced(unreal.load_asset(asset_path) , True)
            animations.append(unreal.EditorAssetLibrary.load_asset(asset_path))
    bpdef.set_editor_property("AnimationAssets", animations)

def import_fbx(filepath) : 

    filename = os.path.splitext(os.path.basename(filepath))[0]  #get file name without extension

    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', filename)
    task.set_editor_property('destination_path', '/Game/Imports/AutoImports/' + filename)
    task.set_editor_property('filename', filepath)
    task.set_editor_property('save', True)

    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', True)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', True)
    options.import_animations = True

    task.set_editor_property('options', options)

    return task

def get_fbx() : 

    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    filepath = filedialog.askopenfilename(initialdir= "C:/Users/antoi/Documents/Unreal Projects/VRBA/Resources",title="Select FBX",filetypes=(("fbx files","*.fbx"),("all files","*.*")))

    return filepath

def set_datatable(filename, name, check, asset) :
    datatable = unreal.load_object(None, '/Game/MiscAssets/ObjectsDataTable.ObjectsDataTable')
    unreal.PythonDataTableLib.add_row(datatable, filename)
    row_index = len(unreal.PythonDataTableLib.get_row_names(datatable)) - 1
    unreal.PythonDataTableLib.set_property_by_string_at(datatable, row_index, 0, name)
    unreal.PythonDataTableLib.set_property_by_string_at(datatable, row_index, 1, asset)
    unreal.PythonDataTableLib.set_property_by_string_at(datatable, row_index, 2, check)

def button(filepath, check, name) :
    print("BUTTON PRESSED")
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_fbx(filepath)])
    filename = os.path.splitext(os.path.basename(filepath))[0]
    assetPath = create_child_blueprint('/Game/Imports/BP_SqueletteBase', '/Game/Imports/AutoImports/', filename)
    set_blueprint_properties(assetPath + '_C', check, name, filename)
    set_animations_properties(filename)
    set_datatable(filename, name, check, assetPath+'_C')