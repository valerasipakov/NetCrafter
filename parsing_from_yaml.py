import yaml
import hashlib
from commutator_handler import Commutator


# class Commutator:
#     def __init__(self, ip=None, hostname=None, username=None,
#                  password_hash=None, commands=None, password=None):
#         self.ip = ip
#         self.hostname = hostname
#         self.username = username
#         self.password_hash = password_hash
#         self.commands = commands
#         self.password = password

#     def __repr__(self):
#         return (f"Commutator(ip={self.ip}, hostname={self.hostname}, "
#                 f"username={self.username}, password_hash={self.password_hash}, "
#                 f"commands={self.commands}, password={self.password})")

#     def check_password(self, password):
#         """Проверяет совпадает ли хеш пароля с хранимым хешем"""
#         if not self.password_hash or not password:
#             return False

#         # Преобразуем пароль в SHA256 хеш
#         hash_obj = hashlib.sha256()
#         hash_obj.update(password.encode('utf-8'))
#         password_hash = hash_obj.hexdigest()

#         return password_hash == self.password_hash


def parse_devices_from_yaml(file_path):
    """
    Парсит YAML файл с устройствами и создает список объектов Commutator

    Args:
        file_path (str): Путь к YAML файлу

    Returns:
        list: Список объектов Commutator
    """
    commutators = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        # Проверяем наличие ключа 'devices' в данных
        if 'devices' not in data:
            print(f"В файле {file_path} нет ключа 'devices'")
            return commutators

        # Создаем объекты Commutator для каждого устройства
        for device_data in data['devices']:
            # Извлекаем только те поля, которые есть в YAML
            # Остальные поля получат значение None по умолчанию
            commutator = Commutator(
                ip=device_data.get('ip'),
                hostname=device_data.get('hostname'),
                username=device_data.get('username'),
                password_hash=device_data.get('password_hash'),
                commands=device_data.get('commands', [])
                # password не указан, поэтому останется None
            )
            commutators.append(commutator)

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    except yaml.YAMLError as e:
        print(f"Ошибка при чтении YAML файла: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return commutators


def print_devices_info(devices):
    """
    Выводит информацию обо всех устройствах в удобном формате

    Args:
        devices (list): Список объектов Commutator
    """
    if not devices:
        print("Список устройств пуст")
        return

    print(f"Найдено устройств: {len(devices)}")
    for i, device in enumerate(devices, 1):
        print(f"\nУстройство {i}:")
        print(f"  IP: {device.ip}")
        print(f"  Hostname: {device.hostname}")
        print(f"  Username: {device.username}")
        print(f"  Password hash: {device.password_hash}")
        print(f"  Commands: {device.commands}")
        print(f"  Password: {device.password}")


# Пример использования
if __name__ == "__main__":
    # Парсим файл devices.yaml
    devices = parse_devices_from_yaml("devices.yaml")

    # Выводим результат с помощью новой функции
    print_devices_info(devices)
