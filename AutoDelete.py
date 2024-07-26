import unreal

def button(asset) :
    assetname = asset.get_name()[:-2]
    if(unreal.EditorAssetLibrary.does_asset_exist('/Game/Imports/AutoImports/'+assetname+'.'+assetname)) :
        unreal.EditorAssetLibrary.delete_asset('/Game/Imports/AutoImports/'+assetname+'.'+assetname)
        unreal.EditorAssetLibrary.delete_directory('/Game/Imports/AutoImports/'+assetname+'/')
        datatable = unreal.load_object(None, '/Game/MiscAssets/ObjectsDataTable.ObjectsDataTable')
        unreal.PythonDataTableLib.remove_row(datatable, assetname)