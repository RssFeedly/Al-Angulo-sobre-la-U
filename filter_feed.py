import urllib.request
import xml.etree.ElementTree as ET

SOURCE_URL = "https://www.youtube.com/feeds/videos.xml?playlist_id=PLh6wTRX09wXc3bRz7WeNP4QbYbEl2rHgn"
KEYWORD = "UNIVERSITARIO"
OUTPUT_FILE = "filtered_feed.xml"

# Registrar espacios de nombres (namespaces) que usa YouTube para mantener la validez del XML
namespaces = {
    'atom': 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'media': 'http://search.yahoo.com/mrss/'
}

for prefix, uri in namespaces.items():
    ET.register_namespace('' if prefix == 'atom' else prefix, uri)

def filter_feed():
    # 1. Descargar el XML original de YouTube
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    xml_data = response.read()

    # 2. Parsear el documento XML
    root = ET.fromstring(xml_data)

    # 3. Filtrar las entradas (<entry>)
    for entry in root.findall('atom:entry', namespaces):
        title_elem = entry.find('atom:title', namespaces)
        
        # Si la entrada no tiene título o no contiene la palabra clave, la eliminamos
        if title_elem is None or KEYWORD.lower() not in title_elem.text.lower():
            root.remove(entry)

    # 4. Guardar el nuevo XML filtrado
    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding='utf-8', xml_declaration=True)
    print(f"Feed filtrado generado con éxito en '{OUTPUT_FILE}'")

if __name__ == "__main__":
    filter_feed()
