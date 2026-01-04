from dataclasses import dataclass, field
from typing import List, Literal, Dict, Any
from netmiko import ConnectHandler   # pip install netmiko


Vendor = Literal["None", "cisco_ios", "juniper_junos", "arista_eos", "nokia_srl", "mikrotik_routeros", "hp_procurve"]  # и т.п. [web:7]


@dataclass
class Commutator:
    ip: str
    hostname: str
    username: str
    commands: List[str]     # список show / config команд
    password_hash: str
    password: str = ''
    vendor: Vendor = "None"          # тип/вендор для Netmiko [web:7]
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