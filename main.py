"""flaregun updates CloudFlare DNS to point to your local machine.

Usage:
    main.py --zone=<zone> --record=<record>
    main.py (-h | --help)

Options:
    --zone=<zone name>      Name of DNS zone to update (example: "sjodle.com")
    --record=<record name>  Name of DNS A record to update (example: "altus.sjodle.com")
    -h --help               Show this help

"""
import os

from typing import Optional

from docopt import docopt
import requests

CLOUDFLARE_TOKEN = os.environ.get('CLOUDFLARE_TOKEN')


def get_zone_id(zone_name: str) -> str:
    req = requests.get(
        "https://api.cloudflare.com/client/v4/zones",
        params={
            "name": zone_name
        },
        headers={
            "Authorization": f"Bearer {CLOUDFLARE_TOKEN}"
        }
    )
    res = req.json()
    return res["result"][0]["id"]


def get_record_id(zone_id: str, record_name: str) -> Optional[str]:
    req = requests.get(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
        params={
            "name": record_name,
            "type": "A"
        },
        headers={
            "Authorization": f"Bearer {CLOUDFLARE_TOKEN}"
        }
    )
    res = req.json()
    result = res["result"]
    if len(result) > 0:
        return result[0]["id"]
    else:
        return None


def put_a_record(zone_id: str, record_name: str, record_value: str, record_id: Optional[str] = None):
    if record_id is None:
        uri = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        requests.post(
            uri,
            json={
                "type": "A",
                "name": record_name,
                "content": record_value,
                "ttl": 1,
                "proxied": False
            },
            headers={
                "Authorization": f"Bearer {CLOUDFLARE_TOKEN}"
            }
        ).raise_for_status()
    else:
        uri = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        requests.patch(
            uri,
            json={
                "type": "A",
                "name": record_name,
                "content": record_value,
                "ttl": 1,
                "proxied": False
            },
            headers={
                "Authorization": f"Bearer {CLOUDFLARE_TOKEN}"
            }
        ).raise_for_status()


def get_my_ip() -> str:
    return requests.get("https://ifconfig.me").text


def main(zone_name: str, record_name: str):
    zone_id = get_zone_id(zone_name)
    record_id = get_record_id(zone_id, record_name)
    my_ip = get_my_ip()
    put_a_record(zone_id, record_name, my_ip, record_id)
    print(f"Updated {record_name} = {my_ip}")


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args['--zone'], args['--record'])
