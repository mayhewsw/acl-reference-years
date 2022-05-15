import json
from collections import Counter
import matplotlib.pyplot as plt
import statistics
from download_paper_year_data import year_numbers
import numpy as np

"""
Use this script to make the main graph.
"""

all_means = []
all_medians = []
all_years = []
all_count_median = []
all_count_mean = []
all_percentiles = []

for i,year in enumerate(range(1979, 2022)):
    with open(f"data/papers_{year}.jsonl") as f:
        lines = [json.loads(line) for line in f]

    total_counter = Counter()

    num_references = []
    for line in lines:
        years = [ref["citedPaper"]["year"] for ref in line["references"]]
        years = [int(y)-year for y in years if y is not None]
        num_references.append(len(years))
        total_counter.update(years)

    sorted_items = sorted(total_counter.items())

    median_years_past = statistics.median(total_counter.elements())
    mean_years_past = statistics.mean(total_counter.elements())
    percentile = np.percentile(list(total_counter.elements()), 5)

    all_years.append(year)
    all_means.append(-1*mean_years_past)
    all_medians.append(-1*median_years_past)
    all_percentiles.append(-1 * percentile)
    
    all_count_median.append(statistics.median(num_references))
    all_count_mean.append(statistics.mean(num_references))


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, constrained_layout=True)



gg_red = "#f8766d"
gg_blue = "#00bfc4"
gg_green = "#7cae00"
gg_purple = "#c77cff"
gg_pink = "#ff61c3"

# Plot 1
total_papers = [sum(p[1]) for p in sorted(year_numbers.items())]
ax1.plot(all_years, total_papers, ".-", color=gg_pink, label="Total Accepted")
ax1.set_xlabel('ACL Year')
ax1.set_xticks(range(1980, 2025, 5))
ax1.set_yticks([0, 250, 500, 750])
ax1.legend()
ax1.set_ylabel('Count')
ax1.set_title("Number of Accepted Papers")

# Plot 2
ax2.plot(all_years, all_count_mean, ".-", color=gg_purple, label="Mean")
ax2.plot(all_years, all_count_median, ".-", color=gg_blue, label="Median")
ax2.legend()
ax2.set_ylabel('Count')
ax2.set_title("Count of ACL References")

# Plot 3
ax3.plot(all_years, all_means, ".-", color=gg_red, label="Mean")
ax3.plot(all_years, all_medians, ".-", color=gg_green, label="Median")
# ax3.plot(all_years, all_percentiles, ".-", color=gg_purple, label="5th Percentile")
ax3.set_ylabel('Age in Years')
ax3.set_title("Age of ACL References")

ax3.legend()

plt.savefig("average_age.png", dpi=400)
plt.show()