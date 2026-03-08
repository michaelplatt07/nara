# A Locally Hosted Recipe Book

## Requirements
The models directory requires a model be downloaded before running the system. The base model that is being used is the
`TheBloke/Mistral-7B-Instruct-v0.1-GGUF` and should be downloaded to the `models` directory. This can be done by installing
`pip install huggingface_hub` and running this code snippet:
```python
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", filename="mistral-7b-instruct-v0.1.Q4_K_M.gguf", local_dir="PATH/TO/MODELS/DIR")
```
This model is smaller and better
```python
from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
    filename="Phi-3-mini-4k-instruct-q4.gguf",
    local_dir="/home/michael/Desktop/programming/nara/models"
)```

## Deployment
The system is designed to be able to be deployed all locally on a system with a single `docker` command. Simply run
`sudo docker-compose -f docker-compose.yaml up --build` and the system will start.
