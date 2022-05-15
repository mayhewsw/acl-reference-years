import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import statistics
from download_paper_year_data import year_numbers
import numpy as np

"""
Use this script to look at percentiles of age.
"""

all_years = []
all_percentiles = defaultdict(list)

for i,year in enumerate(range(1979, 2022)):
    with open(f"data/papers_{year}.jsonl") as f:
        lines = [json.loads(line) for line in f]

    total_counter = Counter()
    by_paper_counter = Counter()

    num_references = []
    for line in lines:
        # reference years for a specific paper
        years = [ref["citedPaper"]["year"] for ref in line["references"]]
        years = [year-int(y) for y in years if y is not None]
        if len(years) > 0:
            median_year = statistics.median(years)
            by_paper_counter[median_year] += 1

        num_references.append(len(years))
        total_counter.update(years)


    sorted_items = sorted(total_counter.items())
    by_paper_sorted_items = sorted(by_paper_counter.items())


    for p in [95, 90, 75, 50, 25, 10]:
        elements = [e for e in by_paper_counter.elements()]
        percentile = np.percentile(elements, p)
        all_percentiles[p].append(percentile)
    
    all_years.append(year)
    

fig, ax = plt.subplots(1, 1, sharex=True, constrained_layout=True)

ax.set_title("Age of ACL References: Percentiles")

gg_red = "#f8766d"
gg_blue = "#00bfc4"
gg_green = "#7cae00"
gg_purple = "#c77cff"
gg_pink = "#ff61c3"

# This is just oldest paper.
# ax.plot(all_years, all_percentiles[100], ".-", color="black", label="100th Percentile")
ax.plot(all_years, all_percentiles[95], ".-", color=gg_red, label="95th Percentile")
ax.plot(all_years, all_percentiles[90], ".-", color=gg_pink, label="90th Percentile")
ax.plot(all_years, all_percentiles[75], ".-", color=gg_purple, label="75th Percentile")
ax.plot(all_years, all_percentiles[50], ".-", color=gg_green, label="50th Percentile")
ax.plot(all_years, all_percentiles[25], ".-", color=gg_blue, label="25th Percentile")
ax.plot(all_years, all_percentiles[10], ".-", color=gg_red, label="10th Percentile")

ax.set_xlabel('ACL Year')
ax.set_ylabel('Age in Years')
ax.set_xticks(range(1980, 2021, 5))

fig.set_size_inches(10,4)

ax.legend(loc="center left", bbox_to_anchor=(1.0,0.5))
plt.savefig("percentiles.png", dpi=400)
plt.show()