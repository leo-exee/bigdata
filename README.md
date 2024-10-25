# Big Data Project
This repository contains code and tools for a big data project focusing on data processing, analysis, and service management.
It is necessary for this project to have a [Hadoop instance](https://hadoop.apache.org/).

## Features
- Count the number of words in a text file
- Find the most repeated occurrence in a genome

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
```

## Running the Project
To run the main script, execute:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Go to the doc
To access the doc and use the API, please go to the [project swagger](http://localhost:8000/docs).
