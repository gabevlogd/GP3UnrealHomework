import unreal

def create_blueprint(package_path, asset_name, parent_class, properties=None):
    """
    Crea un Blueprint in Unreal Engine.
    
    :param package_path: Percorso del pacchetto (es. "/Game/Blueprints")
    :param asset_name: Nome dell'asset (es. "MyBlueprint")
    :param parent_class: Classe base del Blueprint (es. unreal.Actor)
    :param properties: Dizionario di proprietà da impostare sul Blueprint (opzionale)
    :return: Il Blueprint creato o None se già esiste.
    """
    
    asset_full_path = f"{package_path}/{asset_name}"
    
    # Controlla se l'asset esiste già
    if unreal.EditorAssetLibrary.does_asset_exist(asset_full_path):
        print(f"L'asset '{asset_full_path}' esiste già!")
        return None

    # Crea il Blueprint
    factory = unreal.BlueprintFactory()
    blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name,
        package_path,
        unreal.Blueprint,
        factory
    )

    # Impostazione della classe base (parent_class)
    if blueprint:
        # La classe parent_class deve essere un oggetto UClass
        blueprint_cdo = blueprint.get_class().get_default_object()
        blueprint_cdo.set_editor_property('parent_class', parent_class)
        blueprint_cdo.set_editor_property

    if properties:
        # Imposta le proprietà del Blueprint
        for key, value in properties.items():
            blueprint.set_editor_property(key, value)

    # Salva l'asset
    unreal.EditorAssetLibrary.save_asset(asset_full_path)
    print(f"Blueprint creato: {asset_full_path}")

    return blueprint