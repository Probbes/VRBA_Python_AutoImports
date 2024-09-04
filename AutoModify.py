import unreal

def button(asset, oldname, newname, isdel) :
    print("AUTO MODIFY START")
    assetname = asset.get_name()[:-2]
    if(unreal.EditorAssetLibrary.does_asset_exist('/Game/Imports/AutoImports/'+assetname+'.'+assetname)) :
        bpgen = unreal.load_object(None, '/Game/Imports/AutoImports/' + assetname + '.' + assetname + '_C')
        bpdef = unreal.get_default_object(bpgen)

        animations = []
        for index, anim in enumerate(oldname) :
            if (isdel[index] == True) :
                unreal.EditorAssetLibrary.delete_asset('/Game/Imports/AutoImports/'+assetname+'/'+ oldname[index] + "." + oldname[index])
            else :
                if (newname[index] != oldname[index]) :
                    unreal.EditorAssetLibrary.rename_asset('/Game/Imports/AutoImports/' + assetname + '/' + oldname[index], '/Game/Imports/AutoImports/' + assetname + '/' + newname[index])
                    asset_path = '/Game/Imports/AutoImports/' + assetname + '/' + newname[index] + '.' + newname[index]
                    animations.append(unreal.EditorAssetLibrary.load_asset(asset_path))
                else :
                    asset_path = '/Game/Imports/AutoImports/' + assetname + '/' + oldname[index] + '.' + oldname[index]
                    animations.append(unreal.EditorAssetLibrary.load_asset(asset_path))

        bpdef.set_editor_property("AnimationAssets", animations)