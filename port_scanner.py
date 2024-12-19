import socket
import threading
from queue import Queue
from tqdm import tqdm

# Глобальные переменные
open_ports = []  # Список открытых портов
queue = Queue()  # Очередь для портов


# Функция для сканирования одного порта
def scan_port(host, port):
    try:
        # Попытка подключения
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Установим таймаут на 0.5 секунды
            if s.connect_ex((host, port)) == 0:  # Если порт открыт
                open_ports.append(port)
    except Exception:
        pass


# Функция для работы потока
def worker(host, progress_bar):
    while not queue.empty():
        port = queue.get()
        scan_port(host, port)
        progress_bar.update(1)  # Обновляем прогресс-бар
        queue.task_done()


# Основная функция
def main():
    # Запрос у пользователя имени хоста/IP
    host = input("Введите хост/IP для сканирования: ")

    # Очистим список открытых портов
    global open_ports
    open_ports = []

    # Заполним очередь портов
    for port in range(1, 65536):
        queue.put(port)

    # Создаем прогресс-бар
    total_ports = 65535
    with tqdm(total=total_ports, desc="Сканирование портов") as progress_bar:
        # Количество потоков
        num_threads = 100

        # Запускаем потоки
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker, args=(host, progress_bar))
            thread.daemon = True  # Закрыть потоки при завершении программы
            threads.append(thread)
            thread.start()

        # Ожидаем завершения очереди
        queue.join()

    # Сортируем список открытых портов и выводим их
    open_ports.sort()
    print("\nОткрытые порты:")
    for port in open_ports:
        print(f"Порт {port} открыт")


# Запуск программы
if __name__ == "__main__":
    main()
