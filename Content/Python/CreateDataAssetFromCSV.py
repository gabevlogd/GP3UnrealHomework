import unreal
import pandas as pd
import re


def camel_to_snake(name):
    """Converte CamelCase in snake_case (es. 'HealthPoints' -> 'health_points')."""
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

def create_data_assets_from_csv(csv_file, asset_class, package_path):
    """
    Crea più Data Asset in Unreal Engine, uno per ogni riga valida del CSV.

    :param csv_file: Percorso del file CSV.
    :param asset_class: Classe del Data Asset (es. unreal.MyDataAsset).
    :param package_path: Percorso della cartella degli asset (es. "/Game/DataAssets").
    """
    
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        asset_name = str(row.iloc[0]).strip()  # Primo valore della riga = nome del Data Asset
        asset_full_path = f"{package_path}/{asset_name}"

        if unreal.EditorAssetLibrary.does_asset_exist(asset_full_path):
            asset = unreal.EditorAssetLibrary.load_asset(asset_full_path)
        else:
            # Crea il Data Asset
            factory = unreal.DataAssetFactory()
            asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                asset_name,
                package_path,
                asset_class,
                factory
            )

        

        if not asset:
            print(f"Errore nella creazione del Data Asset: {asset_name}")
            continue

        # Inserisce i dati nei campi del Data Asset
        for col_name, value in row.items():
            if col_name == df.columns[0]:  # Ignora la colonna del nome
                continue
            
            property_name = camel_to_snake(col_name.strip())  # Normalizza il nome
            try:
                asset.set_editor_property(property_name, value)
            except Exception as e:
                print(f"Errore nell'impostare {property_name} per {asset_name}: {e}")

        # Salva l'asset
        unreal.EditorAssetLibrary.save_asset(asset_full_path)
        print(f"✅ Data Asset creato: {asset_full_path}")

# Esempio di utilizzo
if __name__ == "__main__":
    asset_class = unreal.MyDataAsset  # Sostituisci con la tua classe C++
    package_path = "/Game/DataAssets"
    asset_name = "MyDataAssetInstance"
    properties = {
        "Value": 42,
        "Name": "My Example Data"
    }

    #create_data_asset(asset_class, package_path, asset_name, properties)
