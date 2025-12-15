import clients.akm2501.st00.main
import clients.akm2501.st14.main
import clients.asm2504.st00.main
import clients.asm2504.st10.main
import clients.asm2504.st12.main
import clients.akm2501.st08.main
import clients.asm2504.st18.main
# import clients.akm2501.st08.main
import clients.akm2501.st03.main
import clients.asm2504.st06.main
import clients.akm2501.st09.main
import clients.asm2504.st09.main
import clients.asm2504.st24.main
import clients.asm2504.st03.main
import clients.akm2501.st18.main
import clients.asm2504.st18.main
#import clients.akm2501.st04.main
import clients.asm2504.st29.main
import clients.asm2504.st05.main
import clients.asm2504.st16.main
import clients.asm2504.st23.main
import clients.akm2501.st11.main
import clients.asm2504.st01.main
import clients.asm2504.st26.main

# добавить импорт своего модуля по шаблону
# import clients.<код группы>.st<номер по журналу>.main

MENU = [
    ["[2501-00] Образец 2501", clients.akm2501.st00.main.main],
    ["[2501-14] Погосян", clients.akm2501.st14.main.main],
    ["[2504-00] Образец 2504", clients.asm2504.st00.main.main],
    ["[2504-10] Князев", clients.asm2504.st10.main.main],
    ["[2504-12] Комаров Дмитрий", clients.asm2504.st12.main.main],
    # ["[2501-08] Зубков", clients.akm2501.st08.main.main],
    ["[2501-03] Бердичев", clients.akm2501.st03.main.main],
    ["[2501-09] Исламов", clients.akm2501.st09.main.main],
    # ["[2501-08] Зубков", clients.akm2501.st08.main.main],
    ["[2504-12] Комаров", clients.asm2504.st12.main.main],
    ["[2501-08] Зубков", clients.akm2501.st08.main.main],
    ["[2504-18] Нуритдинов", clients.asm2504.st18.main.main],
    ["[2504-06] Галимов", clients.asm2504.st06.main.main],
    ["[2504-09] Карпова", clients.asm2504.st09.main.main],
    ["[2504-24] Столер", clients.asm2504.st24.main.main],
    ["[2504-03] Батюшкова", clients.asm2504.st03.main.main],
 #   ["[2501-04] Долгов", clients.akm2501.st04.main.main],
    ["[2501-18] Сунагатова", clients.akm2501.st18.main.main],
    ["[2504-18] Нуритдинов", clients.asm2504.st18.main.main],
    ["[2504-23] Степура", clients.asm2504.st23.main.main],
    ["[2504-29] Яшонков", clients.asm2504.st29.main.main],
    ["[2504-05] Брыгина", clients.asm2504.st05.main.main],
    ["[2504-16] Медведев", clients.asm2504.st16.main.main],
    ["[2501-11] Кондакова", clients.akm2501.st11.main.main],
    ["[2504-01] Алешко", clients.asm2504.st01.main.main],
    ["[2504-26] Шипов", clients.asm2504.st26.main.main],
]


def menu():
    print("------------------------------")
    for i, item in enumerate(sorted(MENU)):
        print("{0:2}. {1}".format(i, item[0]))
    print("------------------------------")
    return int(input())

try:
    while True:
        sorted(MENU)[menu()][1]()
except Exception as ex:
    print(ex, "\nbye")
