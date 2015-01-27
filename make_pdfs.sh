#!/bin/bash

today=`date +%Y_%m_%d`
CV_name=`printf %s%s "$today" "_CV.pdf"`
Letter_name=`printf %s%s "$today" "_PersBrev.pdf"`

./run.py > output.svg  && inkscape --without-gui --export-pdf="$CV_name" output.svg
./pers_runner.py > letter_output.svg  && inkscape --without-gui --export-pdf="$Letter_name" letter_output.svg
