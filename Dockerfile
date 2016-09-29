FROM python:2.7
MAINTAINER Mattias Lyckne <mattias@lyckne.se>
USER root

ADD ./ /tvshow_parser

RUN echo "deb http://ftp.uk.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
Run echo "deb http://www.deb-multimedia.org jessie main non-free" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y --force-yes ffmpeg atomicparsley libfdk-aac-dev 

RUN cd /tvshow_parser && pip install -r requirements.txt

RUN ln -s /tvshow_parser/tvshow_parser.py /usr/local/bin/tvshow_parser

CMD ["bash"]
