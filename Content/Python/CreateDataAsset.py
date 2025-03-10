import unreal

def create_data_asset(asset_class, package_path, asset_name, properties=None):
    """
    Crea un Data Asset in Unreal Engine.
    
    :param asset_class: Classe del Data Asset (es. unreal.MyDataAsset)
    :param package_path: Percorso del pacchetto (es. "/Game/DataAssets")
    :param asset_name: Nome dell'asset (es. "MyDataAssetInstance")
    :param properties: Dizionario di proprietà da impostare sull'asset (opzionale)
    :return: Il Data Asset creato o None se già esiste.
    """
    
    asset_full_path = f"{package_path}/{asset_name}"
    
    # Controlla se l'asset esiste già
    if unreal.EditorAssetLibrary.does_asset_exist(asset_full_path):
        print(f"L'asset '{asset_full_path}' esiste già!")
        return None

    # Crea il Data Asset
    factory = unreal.DataAssetFactory()
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name,
        package_path,
        asset_class,
        factory
    )

    if asset and properties:
        # Imposta le proprietà fornite
        for key, value in properties.items():
            asset.set_editor_property(key, value)

    # Salva l'asset
    unreal.EditorAssetLibrary.save_asset(asset_full_path)
    print(f"Data Asset creato: {asset_full_path}")

    return asset


# Esempio di utilizzo
if __name__ == "__main__":
    asset_class = unreal.MyDataAsset  # Sostituisci con la tua classe C++
    package_path = "/Game/DataAssets"
    asset_name = "MyDataAssetInstance"
    properties = {
        "Value": 42,
        "Name": "My Example Data"
    }

    create_data_asset(asset_class, package_path, asset_name, properties)
