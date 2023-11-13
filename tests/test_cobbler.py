import unittest
from unittest.mock import patch
from cobbler_1 import CobblerHost, create_hosts, AddToCobblerExc
import subprocess

class TestCreateHosts(unittest.TestCase):

    @patch('subprocess.run')
    def test_add_to_cobbler(self, mock_run):
        # Подготовка данных для теста
        host_data = {
            "name": "host-1",
            "profile": "astra-1.7.0-x86_64",
            "dns_name": "example.com",
            "interface": "eth0",
            "ip_address": "192.168.1.1",
            "mac_address": "00:11:22:33:44:55",
            "gateway": "192.168.1.254",
            "mtu": "1500",
            "hostname": "host-1",
            "name_servers": "10.40.19.5",
        }

        # Мокирую выполнение subprocess.run
        mock_run.return_value.returncode = 0  # Успешное выполнение команды

        # Создаем объект CobblerHost и вызываем метод add_to_cobbler
        host = CobblerHost(**host_data)
        host.add_to_cobbler()

        # Это моя ожидаемая команда
        expected_command = (
            "cobbler system add "
            "--name=host-1 "
            "--profile=astra-1.7.0-x86_64 "
            "--dns-name=example.com "
            "--interface=eth0 --ip-address=192.168.1.1 "
            "--mac-address=00:11:22:33:44:55 "
            "--gateway=192.168.1.254 "
            "--mtu=1500 "
            "--hostname=host-1 "
            "--name-servers=10.40.19.5"
        )
        mock_run.assert_called_with(
            expected_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        self.assertEqual(
            host.add_to_cobbler(),
            "Successfully added host-1 to Cobbler."
        )

    @patch('subprocess.run')
    def test_add_to_cobbler_failure(self, mock_run):
        mock_run.return_value.returncode = 1  # Неуспешное выполнение команды

        host_data = {
            "name": "host-1",
            "profile": "astra-1.7.0-x86_64",
            "dns_name": "example.com",
            "interface": "eth0",
            "ip_address": "192.168.1.1",
            "mac_address": "00:11:22:33:44:55",
            "gateway": "192.168.1.254",
            "mtu": "1500",
            "hostname": "host-1",
            "name_servers": "10.40.19.5",

        }
        host = CobblerHost(**host_data)
        with self.assertRaises(AddToCobblerExc):
            host.add_to_cobbler()

if __name__ == '__main__':
    unittest.main()


# python -m unittest tests/test_cobbler.py