import unittest
import os
import json
from unittest.mock import patch
from parser_1 import create_json

class TestCreateJson(unittest.TestCase):

    @patch('openpyxl.load_workbook')
    def test_create_json(self, mock_load_workbook):
        mock_workbook = mock_load_workbook.return_value
        mock_sheet = mock_workbook['Сущности']
        
        # Это мне пригодилось бы если бы реальные json еще не были созданы
        mock_rows = [
            ("host-1_uu-1", "srv-001", "acc.abb", "172.14.13.12", "00:26:57:00:1f:02", "172.14.13.254", "host-1_uu-1", "10.40.19.5"),
            ("host-2_uu-2", "srv-002", "acc.abb", "172.14.13.13", "00:26:57:00:1f:03", "172.14.13.254", "host-2_uu-2", "10.40.19.5"),
        ]

        mock_sheet.iter_rows.return_value = mock_rows

        create_json(3, 7)

        self.assertTrue(os.path.exists("json_files"))  

        self.assertTrue(os.path.exists("json_files/host-1_uu-1.json"))
        self.assertTrue(os.path.exists("json_files/host-2_uu-2.json"))

        with open("json_files/host-1_uu-1.json", "r", encoding="utf-8") as json_file:
            host_1_data = json.load(json_file)
        self.assertEqual(host_1_data["name"], "host-1_uu-1")
        self.assertEqual(host_1_data["dns_name"], "srv-001.acc.abb")
        self.assertEqual(host_1_data["ip_address"], "172.14.13.12")
        self.assertEqual(host_1_data["mac_address"], "00:26:57:00:1f:02")
        self.assertEqual(host_1_data["gateway"],"172.14.13.254")
        self.assertEqual(host_1_data["hostname"],"host-1_uu-1")
        self.assertEqual(host_1_data["name_servers"],"10.40.19.5")

        with open("json_files/host-2_uu-2.json", "r", encoding="utf-8") as json_file:
            host_2_data = json.load(json_file)
        self.assertEqual(host_2_data["name"], "host-2_uu-2")
        self.assertEqual(host_2_data["dns_name"], "srv-002.acc.abb")
        self.assertEqual(host_2_data["ip_address"], "172.14.13.13")
        self.assertEqual(host_2_data["mac_address"], "00:26:57:00:1f:03")
        self.assertEqual(host_2_data["gateway"], "172.14.13.254")
        self.assertEqual(host_2_data["hostname"], "host-2_uu-2")
        self.assertEqual(host_2_data["name_servers"],"10.40.19.5")

if __name__ == '__main__':
    unittest.main()

# python -m unittest tests/test_parser.py