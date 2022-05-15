import json
from collections import defaultdict
import matplotlib.pyplot as plt

"""
Use this script to create probabilities.png. 

This shows the probability of selecting a paper from a given year
with max reference age less than N years.
"""

all_years = range(1979, 2022)
probs = defaultdict(list)

for i,year in enumerate(all_years):
    with open(f"data/papers_{year}.jsonl") as f:
        lines = [json.loads(line) for line in f]

    max_ref_ages = []
    for line in lines:
        # reference years for a specific paper
        years = [ref["citedPaper"]["year"] for ref in line["references"]]
        years = [year - int(y) for y in years if y is not None]

        # years is all positive.
        # get the most positive value (oldest reference)
        if len(years) > 0:
            oldest_ref = max(years)
            max_ref_ages.append(oldest_ref)    

    denom = len(max_ref_ages)

    for thresh in [3, 5, 10, 20]:
        num = len([v for v in max_ref_ages if v <= thresh])
        prob = num / denom
        probs[thresh].append(prob)


fig, ax = plt.subplots(1, 1, sharex=True, constrained_layout=True)

ax.set_title("Probability of randomly selecting a paper from year X with oldest reference less than N years")

gg_red = "#f8766d"
gg_blue = "#00bfc4"
gg_green = "#7cae00"
gg_purple = "#c77cff"
gg_pink = "#ff61c3"

ax.plot(all_years, probs[5], ".-", color=gg_green, label="5 years")
ax.plot(all_years, probs[10], ".-", color=gg_purple, label="10 years")

ax.set_xlabel('ACL Year')
ax.set_ylabel('Probability')
ax.set_xticks(range(1980, 2021, 5))
ax.set_yticks([i/10. for i in range(0,9,1)])

fig.set_size_inches(10,4)

ax.legend()
plt.savefig("probabilities.png", dpi=400)
plt.show()