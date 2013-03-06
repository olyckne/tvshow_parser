tvshow_parser
=============

Parses TV Shows. Mainly for converting to iTunes friendly format, adding metadata, subtitle and adding to iTunes

## Still early in development

### Setup

- Download (d'oh!)
- cd to directory
- `pip install -r requirements.txt`
- `cp config-sample.yaml config.yaml` and edit it to your liking.

--

### Usage
- basic usage: `python tvshow_parser.py filename`



### Short story: 
Rewriting a tv show parser I wrote in php to python

### Long story:
I wanted to have my TV shows in iTunes but they often comes in a format that iTunes doesn't support  (we don't have TV Shows in iTunes Store in Sweden), so I needed to convert them, and enter metadata etc.

Getting the TV shows was automatic, so of course I wanted the converting and adding to iTunes to be automatic too.

And I wanted it NOW so I wrote the script in php cause that is the language I know the best.
Now I feel it's time to rewrite it in python.
