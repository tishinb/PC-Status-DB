import sqlite3
import sys

con = sqlite3.connect('college_computers.db')
cursor = con.cursor()
print('Программа для учета компьютеров\n'
      'Введите help для документации')

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS college_computers_status (
            number TEXT PRIMARY KEY NOT NULL,
            cpu TEXT,
            motherboard TEXT,
            ram_gb INTEGER,
            disk_mb INTEGER,
            os INTEGER NOT NULL DEFAULT '0',
            disk_partition INTEGER NOT NULL DEFAULT '0',
            number_on_case INTEGER NOT NULL DEFAULT '0',
            accounts INTEGER NOT NULL DEFAULT '0',
            network_params INTEGER NOT NULL DEFAULT '0',
            internet INTEGER NOT NULL DEFAULT '0',
            domain INTEGER NOT NULL DEFAULT '0',
            kes INTEGER NOT NULL DEFAULT '0',
            other_software INTEGER NOT NULL DEFAULT '0'
        ) STRICT
    ''')
    con.commit()

def main():
    create_table()
    answer = input('Ввод: ')
    if answer == 'help':
        print('Введите add to table для добавления данных о номере и характеристиках компьютера\n'
              'Введите edit table для изменения данных о характеристиках компьютера\n'
              'Введите rename для изменения номера компьютера\n'
              'Введите edit status для изменения статуса готовности к работе\n'
              'Введите check status для проверка статуса готовности к работе\n'
              'Введите remove row для удаления строки данных из таблицы'
              'Введите remove all для удаления таблицы'
              'Введите print names для вывода имён компьютеров\n'
              'Введите exit для выхода')
    if answer == 'add to table':
        number_input = input('Введите номер компьютера (обязательно!): ')
        cpu_input = input('Введите наименование процессора: ')
        motherboard_input = input('Введите наименование материнской платы: ')
        ram_gb_input = input('Введите объём оперативной памяти в Гб (писать только число!): ')
        disk_mb_input = input('Введите объём основного накопителя Мб (писать только число!): ')
        try:
            cursor.execute('INSERT INTO college_computers_status (number, cpu, motherboard, ram_gb, disk_mb) VALUES (?, ?, ?, ?, ?)', (number_input, cpu_input, motherboard_input, ram_gb_input, disk_mb_input))
            con.commit()
            print('Данные добавлены!')
        except sqlite3.IntegrityError as e:
                print(f"Произошла ошибка в работе с базой данных: {e}")
    elif answer == 'edit table':
        number_input = input('Введите номер компьютера: ')
        cpu_input = input('Введите наименование процессора: ')
        motherboard_input = input('Введите наименование материнской платы: ')
        ram_gb_input = input('Введите объём оперативной памяти в Гб (писать только число!): ')
        disk_mb_input = input('Введите объём основного накопителя Мб (писать только число!): ')
        cursor.execute(
            "UPDATE college_computers_status SET cpu = ?, motherboard = ?, ram_gb = ?, disk_mb = ? WHERE number = ?",
            (cpu_input, motherboard_input, ram_gb_input, disk_mb_input, number_input))
        con.commit()
        print('Данные обновлены!')
    elif answer == 'edit status':
        print('1 - Да, 0 или пропуск - Нет')
        computer_number_input = input('Введите номер компьютера: ')
        os_input = input('Готовность ОС: ')
        disk_partition_input = input('Готовность разделов диска: ')
        number_on_case_input = input('Наклеен номер пк на корпус: ')
        accounts_input = input('Готовность учетных записей: ')
        network_params_input = input('Готовность сетевых параметров: ')
        internet_input = input('Проверен доступ к интернету: ')
        domain_input = input('Готовность домена: ')
        kes_input = input('Готовность KES: ')
        other_software_input = input('Готовность Microsoft Office/Pycharm/JDK: ')
        cursor.execute(
            "UPDATE college_computers_status SET os = ?, disk_partition = ?, number_on_case = ?, accounts = ?, network_params = ?, internet = ?, domain = ?, kes = ?, other_software = ? WHERE number = ?",
            (os_input, disk_partition_input, number_on_case_input, accounts_input, network_params_input, internet_input, domain_input, kes_input, other_software_input, computer_number_input))
        con.commit()
        print('Данные обновлены!')
    elif answer == 'check status':
        computer_number_input = input('Введите номер компьютера: ')
        cursor.execute("SELECT * FROM college_computers_status WHERE number = ?", (computer_number_input,))
        result = cursor.fetchone()
        if result is not None:
            print('Характеристики:')

            print(f'Процессор: {result[1]}')
            print(f'Материнская плата: {result[2]}')
            print(f'Объём оперативной памяти в ГБ: {result[3]} Гб')
            print(f'Объём основного накопителя МБ: {result[4]} Мб')

            print('Готовность к использованию(1 - да, 0 -нет):')

            print(f'Готовность ОС: {result[5]}')
            print(f'Готовность разделов диска: {result[6]}')
            print(f'Отмечена нумерация на корпусе: {result[7]}')
            print(f'Готовность учетных записей: {result[8]}')
            print(f'Готовность параметров сети: {result[9]}')
            print(f'Есть доступ в интернет: {result[10]}')
            print(f'Настроен домен: {result[11]}')
            print(f'Установлен KES: {result[12]}')
            print(f'Установлено прочее ПО: {result[13]}')
        else:
            print("Данные не найдены")
    elif answer == 'print names':
        cursor.execute("SELECT number FROM college_computers_status")
        result = cursor.fetchall()
        for number in result:
            print(number[0])
    elif answer == 'rename':
        computer_number_input = input('Введите номер компьютера: ')
        computer_number_input_new = input('Введите новый номер компьютера: ')
        cursor.execute(
            "UPDATE college_computers_status SET number = ? WHERE number = ?",
            (computer_number_input_new, computer_number_input))
        con.commit()
        print('Данные обновлены!')
    elif answer == 'remove row':
        computer_number_input = input('Введите номер компьютера: ')
        cursor.execute(
            "DELETE FROM college_computers_status WHERE number = ?",
            (computer_number_input,))
        con.commit()
        print('Строка удалена!')
    elif answer == 'remove all':
        cursor.execute(
            "DROP TABLE IF EXISTS college_computers_status")
        con.commit()
        print('Таблица удалена!')
    elif answer == 'exit':
        sys.exit()
    else:
        print('Неверный ввод!')
main()

# Цикл работы программы
while True:
    try:
        main()
    except Exception as e:
        print("Произошла ошибка!", e)
        print("Перезапуск ... ")
