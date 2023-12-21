import requests, sys, pandas as pd
import xml.etree.ElementTree as ET

def get_sequence_from_API(uniprotkb):
    requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&accession=" + uniprotkb
    try:
        r = requests.get(requestURL, headers={ "Accept" : "application/xml"})
    except requests.exceptions.RequestException as e:
        print("Warn request: ", e)
        return None
    if not r.ok:
        return None
    tree = ET.ElementTree(ET.fromstring(r.content, parser=ET.XMLParser(encoding='utf-8')))
    root = tree.getroot()
    for element in root.iter():
        if element.text is not None and element.tag.split('}')[1]=='sequence':
            return element.text

# get_sequence_from_API(uniprotkb)

data = []
result = pd.DataFrame(data, columns=['protein1_sequence', 'protein2_sequence', 'affinity'])
result.to_csv('output.csv', index=False)

with open('unique_mitab.txt', 'r') as file:
    for idx, line in enumerate(file):
        line = line.strip().split('\t')
        protein1_id = line[0]
        protein2_id = line[1]
        affinity = line[-1].split(':')[-1]
        protein1_sequence = get_sequence_from_API(protein1_id.split(':')[1])
        protein2_sequence = get_sequence_from_API(protein2_id.split(':')[1])
        if protein1_sequence is None or protein2_sequence is None:
            continue
        data.append([protein1_sequence, protein2_sequence, affinity])
        if (idx) % 100 == 0:
            print('Completed: ', idx+1)
        result = pd.DataFrame([[protein1_sequence, protein2_sequence, affinity]], columns=['protein1_sequence', 'protein2_sequence', 'affinity'])
        result.to_csv('output.csv', mode='a', header=False, index=False)
print('Completed: ', idx+1, 'Total: ', len(data), '\nDone!')