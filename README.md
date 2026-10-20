# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 2.8 or later

#### Install Python using miniconda

1. Download and install MiniConda from [here]()
2. Create new environment using the following command:

```bash
$ conda create -n mini-rag python=3.8
```

3. Activate environment:

```bash
conda activate mini-rag
```

## Installations

### Install the required packages


```
pip install -r requirements.txt
```

### Setup the environment variables
```
cp .env.example .env
```

Set your environment variables in the '.env' file, like `OPENAI_API_KEY` variable

## Run the FastAPI server

``` bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
or 
``` bash
$ python -m uvicorn main:app --reload
```