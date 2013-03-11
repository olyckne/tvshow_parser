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

`python tvshow_parser.py -h`

| flag                  | description | default | implemented
| --------------------- | ----------- | ------- | ------------- 
| -h                    | show help                                                   | -                     | x |
| -d                    | Debug level                                                 | -                     | - |
| -c                    | config file                                                 | ./config.yaml         | x |
| --filename            | Use this string for parsing info instead of actual filename | -                     | x |
| --sub-module          | subtitle module to use                                      | subliminal            | x |
| --sub                 | subtitle file to use                                        | input_filename.srt    | x |
| --type                | type of media (TV/Movie)                                    | TV                    | - |
| --season              | Set season number                                           | parses from filename  | x |
| --name                | Set name                                                    | parses from filename  | x |
| --episode             | Set episode number                                          | parses from filename  | x |
| --add-module          | Add module to use                                           | itunes                | x |
| --hd                  | Set HD quality: True/False                                  | parses from filename  | x |
| --notification-module | Notification module to use                                  | growl                 | x |
| --meta-module         | Metadata module to use                                      | trakt                 | x |



### Short story: 
Rewriting a tv show parser I wrote in php to python

### Long story:
I wanted to have my TV shows in iTunes but they often comes in a format that iTunes doesn't support  (we don't have TV Shows in iTunes Store in Sweden), so I needed to convert them, and enter metadata etc.

Getting the TV shows was automatic, so of course I wanted the converting and adding to iTunes to be automatic too.

And I wanted it NOW so I wrote the script in php cause that is the language I know the best.
Now I feel it's time to rewrite it in python.
