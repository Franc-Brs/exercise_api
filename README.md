# Very Simple PoC for an interview

## Requirements
Windows users:
* Docker Desktop

Linux users:
* Docker
* Docker-Compose

## Description

Really easy and self-explanatory project consisting mostly in a FLASK api that manage model of signals.

## Useful commands
Put up the environment:
```bash
docker-compose up
```
Put down the environment:
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

