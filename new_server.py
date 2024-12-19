import socket
import threading

# Настройки сервера
HOST = 'localhost'
PORT = 9090

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Ожидание до 5 подключений
print(f"Сервер запущен на {HOST}:{PORT} и ожидает подключения...")


# Функция обработки клиента
def handle_client(client_socket, address):
    print(f"Новое подключение: {address}")
    try:
        while True:
            # Принимаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"Клиент {address} отключился")
                break
            print(f"Получено от {address}: {data}")

            # Отправляем обратно данные (эхо)
            client_socket.send(f"Эхо: {data}".encode('utf-8'))
    except Exception as e:
        print(f"Ошибка с клиентом {address}: {e}")
    finally:
        client_socket.close()
        print(f"Соединение с {address} закрыто")


# Основной цикл ожидания клиентов
try:
    while True:
        client_socket, client_address = server_socket.accept()
        # Создаем новый поток для каждого клиента
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("\nСервер остановлен")
finally:
    server_socket.close()
