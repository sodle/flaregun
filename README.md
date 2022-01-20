# flaregun
Updates a CloudFlare DNS record to point to your local machine.

# Requirements
- Python 3
- Poetry

## Usage
Install dependencies:
```shell
poetry install
```

Run:
```shell
CLOUDFLARE_TOKEN=your_token_here poetry run python main.py --zone=example.com --record=myhost.example.com
```

## Run via Kubernetes
Add secret to Kubernetes:
```shell
kubectl create secret generic cloudflare-token --from-literal=CLOUDFLARE_TOKEN=your_token_here
```

Edit `cronjob.yaml` - configure the schedule and ZONE/RECORD parameters as needed.

Add the cronjob to Kubernetes:
```shell
kubectl apply -f ./cronjob.yaml
```