# Для чего этот скрипт

Скрипт нужен для мониторинга доступности поставок на склады Lamoda. 
Каждые 15 минут (время указывается в настройках триггера) отправляет запрос на сервер Lamoda, получает дату и интервалы времени, в которые доступна поставка товара на склад. Если доступных интервалов больше 10 (значение задается в скрипте), то на указанную почту отправляется письмо с уведомлением о том, что слоты стали доступны.

_______
# Начало работы
* [Создание функции](#создание-функции)
* [Настройка триггера](#настройка-триггера)
* [Запуск скрипта](#запуск-скрипта)
* [Остановка скрипта](#остановка-скрипта)
* [Работа скрипта](#работа-скрипта)
* [Изменение параметров (год, месяц, cookie, почта)](#изменение-параметров-год-месяц-cookie-почта)
* [Где взять cookie](#где-взять-cookie)



## Создание функции
1. Необходимо создать функцию python на [Yandex Cloud Functions](https://console.yandex.cloud/folders) 
2. Заменить содержимое файла `index.py` в вашей функции на содержимое файла `index.py` из данного репозитория
3. Создать в функции 2 файла - `lamoda_checker.py` и `requirements.txt`, вставить в них содержимое файлов `lamoda_checker.py` и `requirements.txt` из данного репозитория (не забудьте вставить актуальные куки/почту/другие параметры в файл `lamoda_checker.py`)
4. В настройках функции установить таймаут 60 секунд и сохранить изменения
![image](https://github.com/user-attachments/assets/7b72ff96-543e-4886-9ad9-751239dee50f) 
5. Сделать функцию публичной переключив тумблер в обзоре функции
![image](https://github.com/user-attachments/assets/251ebed7-2ee7-4a82-87cb-db9e51597b18)




## Настройка триггера

Создать триггер, который будет запускать функцию каждые 15 минут (время на ваше усмотрение)
![image](https://github.com/user-attachments/assets/84fcbbf3-58c6-4e24-9e97-7a6b8b90fa14)



## Запуск скрипта

Для запуска скрипта необходимо:
1.	Зайти на [Yandex Cloud Functions](https://console.yandex.cloud/folders) 
2.	Перейти в триггеры <br>
![image](https://github.com/user-attachments/assets/c133a1b2-3391-412f-ad8c-d323d5c13b1f)

3.	Кликнуть по триггеру <br>
![image](https://github.com/user-attachments/assets/022810c2-777f-4802-8244-7c61007b2f22)

4.	В правом верхнем углу нажать кнопку «Запустить»: <br>
![image](https://github.com/user-attachments/assets/96b367a9-c0ab-48a2-950a-5b31ea64a328) <br>
Подтвердить действие: <br>
![image](https://github.com/user-attachments/assets/96f6b7ff-4808-4a87-afa2-d34546aa0464)
5.	Скрипт запущен (будет проверять доступность слотов каждые 15 минут и как только слоты станут доступны – слать письмо)


## Остановка скрипта

1.	Зайти на [Yandex Cloud Functions](https://console.yandex.cloud/folders) 
2.	Перейти в триггеры  <br>
![image](https://github.com/user-attachments/assets/50766b2a-eec7-49a5-ac70-89dc429bd7d0)
3.	Кликнуть по триггеру  <br>
![image](https://github.com/user-attachments/assets/e91a3f46-8bbf-436e-9dd1-c93edaf33e6d)
4.	В правом верхнем углу нажать кнопку «Остановить»:  <br>
![image](https://github.com/user-attachments/assets/3994ec7e-c1ef-4a5b-a4c7-23c4eb178efa) <br>
Подтвердить действие: <br>
![image](https://github.com/user-attachments/assets/2dc12cd0-d367-4511-8ab9-41b05a48cd47)
5.	Скрипт остановлен


## Работа скрипта

При запущенном триггере скрипт будет запускаться каждые 15 минут и проверять на доступность слотов.
Когда слоты станут доступны (проверяю на количество доступных слотов, если больше 10, то считаю, что стали доступны) скрипт отправляет письмо на почту.
Пример:  <br>
![image](https://github.com/user-attachments/assets/2bea61c1-f83d-4e84-a5cd-220536d52e23)

Если во время работы скрипта произошла какая-то ошибка, то скрипт отправит письмо с кодом ошибки. <br>
Пример: <br>
![image](https://github.com/user-attachments/assets/ec1e3dcd-bb6e-4410-b2ca-e32cb968454a)


## Изменение параметров (год, месяц, cookie, почта)

1.	Зайти на [Yandex Cloud Functions](https://console.yandex.cloud/folders) 
2.	Перейти в функции: <br>
 ![image](https://github.com/user-attachments/assets/8bda57bd-3bd4-494e-8230-756831f1d33d)

3.	Кликнуть по функции: <br>
 ![image](https://github.com/user-attachments/assets/d91f2d4a-fbe5-4e2e-b235-749585e7d858)

4.	Нажать на раздел «Редактор»: <br>
 ![image](https://github.com/user-attachments/assets/898f4659-205b-4627-a3c5-9dd650f066c6)

5.	Перейти в файл `lamoda_checker.py` <br>
 ![image](https://github.com/user-attachments/assets/e4f9e3e1-1886-42da-a8c1-9b56cefac9a6)

6.	Внести необходимые изменения в параметры: <br>
 ![image](https://github.com/user-attachments/assets/04b833a9-dbff-4b5f-accb-eeec9b1a74b4)

7.	После внесения изменений пролистать вниз страницы и нажать на кнопку «Сохранить изменения» <br>
 ![image](https://github.com/user-attachments/assets/9f7c5009-0b34-46d3-833e-4f6127785b1e)

8.	Изменения внесены


## Где взять cookie

1.	Зайти на [Lamoda calendar](https://gm.lamoda.ru/calendar) 
2.	Нажать на клавиатуре «Ctrl+Shift+E»
3.	Обновить страницу (F5)
4.	Нажать на запрос, который начинается со слова «calendar»: <br>
 ![image](https://github.com/user-attachments/assets/19957b68-deb0-4469-977f-45de42ffaf25)

5.	В меню справа во вкладке «Заголовки» пролистать до пункта «Заголовки запроса» и найти строку «Cookie»: <br>
 ![image](https://github.com/user-attachments/assets/18322764-afee-4d26-bef1-c30f77216477)

6.	Нажать ПКМ по строке «Cookie» и нажать «Копировать значение»: <br>
 ![image](https://github.com/user-attachments/assets/49fe78f3-46f5-4760-8675-f3f370017893)

7.	Скопированные cookie вставить в параметры (cookie обновляются примерно раз в сутки, поэтому при запущенном скрипте необходимо раз в сутки заходить, копировать новые cookie и вставлять их в параметры скрипта)
