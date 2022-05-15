import requests
import json
import time
from typing import TextIO
import os

"""
This script downloads all the data used in the blog post. In particular, it does smart retries
when the API limit is reached.

See the Semantic Scholar link here:
https://www.semanticscholar.org/product/api

Notes on ACL Ids:
- For 2020, the id was 2020.acl-main.1
- For 2019, the id started at P19-1001
- Same pattern for 2018, and in fact, all the way back to 1979!!!
"""

year_numbers = {
  1979:(29,0),
  1980:(45,0),
  1981:(37,0),
  1982:(40,0),
  1983:(26,0),
  1984:(117,0),  # combined with COLING
  1985:(41,0),
  1986:(42,0),
  1987:(35,0),
  1988:(36,0),
  1989:(35,0),
  1990:(40,0),
  1991:(57,0),
  1992:(55,0),
  1993:(48,0),
  1994:(53,0),
  1995:(57,0),
  1996:(59,0),
  1997:(74,0), # combined with EACL
  1998:(123,129), # combined with COLING, second volume not necessarily short
  1999:(84,0),
  2000:(80,0),
  2001:(71,0),
  2002:(66,0),
  2003:(72,42),
  2004:(89,13),
  2005:(78,27),
  2006:(148,126), # combined with COLING
  2007:(132,58),
  2008:(120,69),
  2009:(122,94),
  2010:(161,71),
  2011:(165,129),
  2012:(112,77),
  2013:(175,155),
  2014:(148,140),
  2015:(175,145),
  2016:(232,98),
  2017:(196,108),
  2018:(257,126),
  2019:(661,0),
  2020:(779,0),
  2021: (572, 140)
}


def get_title(paper_id: str) -> requests.models.Response:
  url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,year,authors"
  return requests.get(url)


def get_reference_years(paper_id) -> requests.models.Response:
  url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=title,year,authors"
  return requests.get(url)


def enumerate_ids(year, is_long: bool = True):
  top_range_long = year_numbers[year][0] + 1
  top_range_short = year_numbers[year][1] + 1
  if year == 2021:
    # do long and then switch to short
    if is_long:
      return [f"ACL:2021.acl-long.{i}" for i in range(1, top_range_long)]
    else:
      return [f"ACL:2021.acl-short.{i}" for i in range(1, top_range_short)]

  if year == 2020:
    # do only main
    if is_long:
      return [f"ACL:2020.acl-main.{i}" for i in range(1, top_range_long)]
    else:
      return []
  if year <= 2019:
    # do PXX-1001 then switch to PXX-2001
    last_two_digits = str(year)[2:]
    if is_long:
      return [f"ACL:P{last_two_digits}-{1000 + i}" for i in range(1, top_range_long)]
    else:
      return [f"ACL:P{last_two_digits}-{2000 + i}" for i in range(1, top_range_short)]


def get_from_paper_id(paper_id: str, out: TextIO) -> None:
  
  paper_response = get_title(paper_id)
  references_response = get_reference_years(paper_id)

  # Status code 429 means rate limiting
  while paper_response.status_code == 429 or references_response.status_code == 429:
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(f"Time is: {result}, sleeping for 5 minutes...")
    # Semantic Scholar makes you wait for 5 minutes
    time.sleep(5*60)
    # then retry
    paper_response = get_title(paper_id)
    references_response = get_reference_years(paper_id)

  # Status code 404 means the link doesn't exist
  if paper_response.status_code == 404 or references_response.status_code == 404:
    # just ignore...
    print("Something wrong here...")
  elif paper_response.status_code == 200 and references_response.status_code == 200:
    paper_json = json.loads(paper_response.text)      
    references_json = json.loads(references_response.text)
    paper_json["references"] = references_json["data"]
    paper_json["aclId"] = paper_id
    out.write(json.dumps(paper_json) + "\n")
  else:
    print(f"Shouldn't get here! Status codes for papers and referneces are: {paper_response.status_code}, {references_response.status_code}")



def get_papers(year):
  out_fname = f"data/papers_{year}.jsonl"

  if os.path.exists(out_fname):
    print(f"{out_fname} exists. Skipping...")
    return

  with open(out_fname, "a") as out:
    for paper_id in enumerate_ids(year, is_long = True):
      get_from_paper_id(paper_id, out)
        
    for paper_id in enumerate_ids(year, is_long = False):
      get_from_paper_id(paper_id, out)


if __name__ == "__main__":
  os.makedirs("data", exist_ok=True)

  for year in range(1979, 2022):
    print("Starting year...")
    get_papers(year)


