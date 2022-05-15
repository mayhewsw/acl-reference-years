# ACL Reference Data
I used the code in this repo for my blog post: http://mayhewsw.github.io/2022/05/03/how-old-are-acl-references/

See individual files for comments.

## Setup

This uses python 3.9. I like to use an environment.

```bash
$ python -m venv .pyenv
$ source .pyenv/bin/activate
$ pip install -r requirements.txt
```

## Data

The data is already included in the `data/` folder, but you can download it again with:

```bash
$ python download_paper_year_data.py
```