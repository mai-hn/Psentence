import requests, sys, pandas as pd
import xml.etree.ElementTree as ET

def get_sequence_from_API(uniprotkb):
    requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&accession=" + uniprotkb
    r = requests.get(requestURL, headers={ "Accept" : "application/xml"})
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    tree = ET.ElementTree(ET.fromstring(r.content, parser=ET.XMLParser(encoding='utf-8')))
    root = tree.getroot()
    for element in root.iter():
        if element.text is not None and element.tag.split('}')[1]=='sequence':
            # print(element.text)
            return element.text

# get_sequence_from_API(uniprotkb)

data = []
with open('unique_mitab.txt', 'r') as file:
    for idx, line in enumerate(file):
        line = line.strip().split('\t')
        protein1_id = line[0]
        protein2_id = line[1]
        affinity = line[-1].split(':')[1]
        protein1_sequence = get_sequence_from_API(protein1_id.split(':')[1])
        protein2_sequence = get_sequence_from_API(protein2_id.split(':')[1])
        data.append([protein1_sequence, protein2_sequence, affinity])
        print('Completed: ', idx+1)
        result = pd.DataFrame(data, columns=['protein1_sequence', 'protein2_sequence', 'affinity'])
        result.to_csv('output.csv', index=False)