import json

def loadJSONfile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_unique_classes(characters):
    classes = set()
    for character in characters:
        classe = character.get("Classe", "").strip()
        if classe:
            classes.add(classe)
    return classes

if __name__ == "__main__":
    data = loadJSONfile("bdd/data/personnages.json")
    characters = data.get("personnages", [])
    
    unique_classes = get_unique_classes(characters)
    
    print("🎓 Classes trouvées dans le fichier JSON :")
    for c in sorted(unique_classes):
        print(f"- {c}")