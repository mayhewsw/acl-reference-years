import json
from collections import Counter

"""
Use this to get the most cited papers by year table
"""

table = """<table><tr>
    <th>Year</th>
    <th>3 most cited papers</th>
    <th>Citation year</th>
    <th>Citation count</th>
  </tr>"""

for i,year in enumerate(range(1979, 2022)):

    with open(f"data/papers_{year}.jsonl") as f:
        lines = [json.loads(line) for line in f]
    
    ref_counter = Counter()
    id_to_title = {}
    id_to_year = {}

    for line in lines:
        refs = line["references"]
        for ref in refs:
            paper_id = ref['citedPaper']['paperId']
            id_to_title[paper_id] = ref['citedPaper']['title']
            id_to_year[paper_id] = ref['citedPaper']['year']
            ref_counter[paper_id] += 1

    del ref_counter[None]
    first = True
    for ref,count in ref_counter.most_common(3):

        if first:
            table += "<tr style='border-top: solid 1.5px gray;'>"
            table += f"<td rowspan='3'>{year}</td>"
            first = False
        else:
            table += "<tr>"

        table += f"<td><a href='https://www.semanticscholar.org/paper/{ref}'>{id_to_title[ref]}</a></td>"
        table += f"<td>{id_to_year[ref]}</td>"
        table += f"<td>{count}</td>"
        table += "</tr>"

table += "</table>"

print(table)