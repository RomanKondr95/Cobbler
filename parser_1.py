import openpyxl as o
import json
import re
from transliterate import translit
import os

book = o.load_workbook(
    "data.xlsx"
)
sheet = book["Сущности"]

if not os.path.exists("json_files"):
    os.mkdir("json_files")


def is_english(text):
    return bool(re.match("^[a-zA-Z]+$", text))


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
            "ip_address": [ip.strip() for ip in row[5].split(",")],
            "mac_adress": (
                [item.strip() for item in row[6].split(",")]
                if row[6] is not None
                else ["None"],
            ),
            "mtu": "1500",
            "profile": "astra-1.7.0-x86_64",
        }

        filename = f"json_files/{node_name}.json"

        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(entity, json_file, ensure_ascii=False, indent=4)

    print("JSON-файлы успешно созданы.")
