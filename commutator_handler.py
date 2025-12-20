from dataclasses import dataclass, field
from typing import List, Literal, Dict, Any
from netmiko import ConnectHandler   # pip install netmiko


Vendor = Literal["cisco_ios", "juniper_junos", "arista_eos", "nokia_srl", "mikrotik_routeros", "hp_procurve"]  # и т.п. [web:7]


@dataclass
class Commutator:
    ip: str
    hostname: str
    username: str
    password: str
    vendor: Vendor          # тип/вендор для Netmiko [web:7]
    commands: List[str]     # список show / config команд
    system: str             # например "ios", "nxos", "junos" и т.п.
    status: bool = False    # успешно ли выполнились команды
    results: Dict[str, Any] = field(default_factory=dict)

    def run_commands(self) -> None:
        """Подключиться к свичу и выполнить команды."""
        conn_params = {
            "device_type": self.vendor,
            "host": self.ip,
            "username": self.username,
            "password": self.password,
        }                       # словарь в стиле Netmiko [web:7][web:13]

        try:
            with ConnectHandler(**conn_params) as conn:
                for cmd in self.commands:
                    print(f"Выполняю команду: {cmd}")
                    self.results[cmd] = conn.send_command(cmd)  # напр. "show version" [web:13]
            self.status = True
        except Exception as exc:
            self.status = False
            self.results["error"] = str(exc)


sw1 = Commutator(
    ip="192.168.1.10",
    hostname="sw-core-1",
    username="admin",
    password="secret",
    vendor="cisco_ios",
    commands=["show version", "show ip interface brief"],
    system="ios",
)

sw1.run_commands()
print(sw1.status)                  # True/False

print(f"Использованная команда: {sw1.commands[0]}")