#!/usr/bin/env bash
export PYTHONUNBUFFERED=1
parallel --linebuffer --tag -j 34 ./test_encoding.py ::: xaa xab xac xad xae xaf xag xah xai xaj xak xal xam xan xao xap xaq xar xas xat xau xav xaw xax xay xaz xba xbb xbc xbd xbe xbf xbg xbh
cat header.md res/x*_different.md > res/combined_different.md
cat header.md res/x*_same.md > res/combined_same.md
cat res/x*all.csv > res/combined_all.csv
cat res/x*skipped.csv > res/combined_skipped.csv
cat res/x*exceptions.txt > res/combined_exceptions.txt
cat res/x*summary.csv > res/combined_summary.csv
