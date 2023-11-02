import subprocess
import json
import os


# кастомные ошибки лучше вынести в отдельный файл
class AddToCobblerExc(Exception):
    pass


class CreateHostExc(Exception):
    pass


class CobblerHost:
    def __init__(
        self, name, profile, dns_name, interface, ip_address, mac_address, mtu
    ):
        self.name = name
        self.profile = profile
        self.dns_name = dns_name
        self.interface = interface
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.mtu = mtu

    def add_to_cobbler(self):
        try:
            command = (
                f"cobbler system add "
                f"--name={self.name} "
                f"--profile={self.profile} "
                f"--dns-name={self.dns_name} "
                f"--interface={self.interface} ")
            for ip in self.ip_address:
                command += f"--ip-address={ip} "
            if self.mac_address and self.mac_address[0] != "None":
                for mac in self.mac_address:
                    command += f"--mac-address={mac} "
            command += f"--mtu={self.mtu}"

            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                print(f"Successfully added {self.name} to Cobbler.")
                return f"Successfully added {self.name} to Cobbler."
            else:
                raise AddToCobblerExc(f"subprocess_err: {result.stderr}")
        except AddToCobblerExc as err:
            print(f"Error: {err}")
            raise AddToCobblerExc from err


def create_hosts():
    json_folder = "json_files"

    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            full_path = os.path.join(json_folder, filename)
            with open(full_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

        for host_data in data:
            try:
                host = CobblerHost(
                    name=host_data["name"],
                    profile=host_data["profile"],
                    dns_name=host_data["dns_name"],
                    interface=host_data["interface"],
                    ip_address=host_data["ip_address"][0],
                    mac_address=host_data["mac_address"][0][0]
                    if host_data["mac_address"][0][0] != "None"
                    else None,
                    mtu=host_data["mtu"],
                )
                host.add_to_cobbler()
            except AddToCobblerExc as err:
                # log
                print('Add_to_cob', err)
                # continue

            except Exception as err:
                # обработать ошибки/перехватить далее
                # log
                print('Unknow exc', err)
                raise CreateHostExc from err
