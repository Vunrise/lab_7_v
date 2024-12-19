import socket

# Настройки клиента
HOST = 'localhost'
PORT = 9090

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Подключено к серверу")

try:
    while True:
        # Ввод сообщения для отправки
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

        # Получение ответа от сервера
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Ответ от сервера: {data}")
finally:
    client_socket.close()
    print("Соединение закрыто")
