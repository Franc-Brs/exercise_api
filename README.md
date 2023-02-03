# Very Simple PoC for an interview

## Requirements
Windows users:
* Docker Desktop

Linux users:
* Docker
* Docker-Compose

## Description
Semplice e self-explanatory, progetto che consiste in una FLASK api che gestisce dei modelli di segnale.
```bash
│   .dockerignore
│   .env.dev
│   .gitignore
│   docker-compose.yml
│   README.md
│
└───app
    │   Dockerfile
    │   manage.py
    │   requirements.txt
    │
    └───project
        │   utilsl.py
        │   __init__.py
```
* docker-compose.yml è il gestore dei servizi di questo repo (monoservizio)
* .env.dev è un file che contiene le variabili di ambiente utilizzate nel container
* la cartella app contiene il Dockerfile per generare l'immagine, il manage.py per creare eventuali comandi da utilizzare via cli in Flask e i requirements per quanto riguarda python
* la cartella project contiene il progettino con le views (__init__.py) e le classi per accedere al modello dei segnali (utilsl.py), quest'ultimo contiene anche due funzioni di cui una necessaria per leggere un eventuale JSON, scritta in maniera purtroppo imprecisa per mancanza di tempo (si veda issue)
## Useful commands
Tirare su l'ambiente:
```bash
docker-compose up
```
Tirare già l'ambiente:
```bash
docker-compose down
```

## How to test it?

You can send a JSON with concatenation of operations, try for example cURL:
```cURL
curl --location --request POST 'http://localhost:8080/computation_example' \
--header 'Content-Type: application/json' \
--data-raw '{
    "action": "multiply",
    "input": [
      {
        "action": "sum",
        "input": [
          {
            "action": "amplitudemod",
            "parameters": {
              "multiplier": 5
            },
            "input": {
              "action": "squarewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          },
          {
            "action": "thresholdup",
            "parameters": {
              "threshold": 5
            },
            "input": {
              "action": "sinewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          }
        ]
      },
      {
        "action": "sawtoothwave",
        "parameters": {
          "amplitude": 5,
          "frequency": 12
        }
      }
    ]
  }'
  ```
Or simply ping the following endpoint with Postman `http://localhost:8080/computation_example`
sendig a POST request with this JSON:
```
{
    "action": "multiply",
    "input": [
      {
        "action": "sum",
        "input": [
          {
            "action": "amplitudemod",
            "parameters": {
              "multiplier": 5
            },
            "input": {
              "action": "squarewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          },
          {
            "action": "thresholdup",
            "parameters": {
              "threshold": 5
            },
            "input": {
              "action": "sinewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          }
        ]
      },
      {
        "action": "sawtoothwave",
        "parameters": {
          "amplitude": 5,
          "frequency": 12
        }
      }
    ]
  }
```

