#!/bin/bash

git add Noneapartments.db
git add database.csv 
git add log.txt

git commit -m "Scrapper database backup: $(date)"

git push
