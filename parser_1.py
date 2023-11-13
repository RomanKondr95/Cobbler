import openpyxl as o
import json
import re
from transliterate import translit
import os
import secrets

book = o.load_workbook(
    "data.xlsx"
)
sheet = book["Сущности"]

if not os.path.exists("json_files"):
    os.mkdir("json_files")


def is_english(text):
    return bool(re.match("^[a-zA-Z]+$", text))


def generate_mac_address():
    mac = [0x00, 0x16, 0x3e]  # OUI
    mac.extend(secrets.randbits(8) for _ in range(3)) 
    return ':'.join(map(lambda x: "%02x" % x, mac))



def create_json(min_r, max_r):
    for row in sheet.iter_rows(min_row=min_r, max_row=max_r, values_only=True):
        node_name = (
            row[0].lower().replace(" ", "_")
            if is_english(row[0])
            else translit(row[0].lower().replace(" ", "_"), "ru", reversed=True)
        )
        entity = {
            "name": node_name,
            "dns_name": f"{row[3].lower()}.{row[4]}",
            "interface": "eth0",
            "ip_address": row[5], 
            "mac_address": row[6] if row[6] != None else generate_mac_address(),
            "gateway": row[7],
            "mtu": "1500",
            "profile": "astra-1.7.0-x86_64",
            "hostname": node_name,
            "name_servers": "10.40.19.5",

        }

        filename = f"json_files/{node_name}.json"

        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(entity, json_file, ensure_ascii=False, indent=4)

    print("JSON-файлы успешно созданы.")
