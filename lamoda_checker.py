import requests
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#
#
#


# Конфигурация
year = "2024"  # Полный год
month = "12"  # Формат месяца: 01, 02, 03, ..., 12
cookie = "_"  # Куки
id = (
    "123"  # id партнера можно взять на стринице поставок (календарь) из адресной строки
)
toaddr_list = [
    "example1@mail.ru",
    "example2@mail.ru",
]  # Список email-адресов для отправки сообщений

fromaddr = "send_email@mail.ru"  # Почта, с которой будут отправляться письма
mypass = "password"  # Пароль от почты для внешних приложений. Для mail.ru брать по ссылке - https://account.mail.ru/user/2-step-auth/passwords

#
#
#


url = f"https://backend.gm.lamoda.ru/api/v1/calendar?month={year}-{month}&partnerId={id}&directionId=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://gm.lamoda.ru",
    "Connection": "keep-alive",
    "Referer": "https://gm.lamoda.ru/",
    "Cookie": cookie,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}


# Функция для отправки GET-запроса и получения JSON-ответа
# Возвращает: словарь JSON-ответа при успешном запросе или строку с ошибкой
def fetch_data(url: str, headers: dict) -> dict | str:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}")
        return f"Ошибка: {response.status_code}"


# Функция для подсчета доступных и недоступных слотов
# Возвращает: кортеж из трех чисел (доступные, недоступные, общее количество)
def count_slots(slots: dict) -> tuple[int, int, int]:
    available_count = 0  # Количество доступных слотов
    unavailable_count = 0  # Количество недоступных слотов

    for slot in slots["data"]["slots"]:
        if slot["startAt"].endswith(":00:00"):  # Фильтрация по времени
            if slot["availability"]:
                available_count += 1
            else:
                unavailable_count += 1

    total_count = available_count + unavailable_count
    return available_count, unavailable_count, total_count


# Функция для отправки email-уведомлений
def send_mail(
    available: int = None,
    unavailable: int = None,
    total: int = None,
    result: str = None,
) -> None:

    if result:
        tema = "ОШИБКА ПОЛУЧЕНИЯ СЛОТОВ LAMODA"  # Тема письма при ошибке
        body = f"""<p>{result}</p>
        <br>
        <p>Если ошибка имеет код 401, то нужно поменять cookie в скрипте.</p>
        <br>
        <p><b>Ссылка на календарь:</b> <a href="https://gm.lamoda.ru/calendar">https://gm.lamoda.ru/calendar</a></p>"""
    else:
        tema = "LAMODA СТАЛИ ДОСТУПНЫ СЛОТЫ"  # Тема письма, если слоты доступны
        body = f"""<p><b>LAMODA СТАЛИ ДОСТУПНЫ СЛОТЫ</b></p>
        <br>
        <p>Всего слотов: {total}</p>
        <p>Доступно слотов: <b>{available}</b> </p>
        <p>Недоступно слотов: {unavailable}</p>
        <br>
        <p><b>Ссылка на календарь:</b> <a href="https://gm.lamoda.ru/calendar">https://gm.lamoda.ru/calendar</a></p>"""

    # Формирование и отправка письма
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = ", ".join(toaddr_list)
    msg["Subject"] = tema
    msg.attach(MIMEText(body, "html"))

    max_retries = 2  # Количество попыток отправки email
    for _ in range(max_retries):
        try:
            server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
            server.login(fromaddr, mypass)  # Логин на сервере
            server.sendmail(fromaddr, toaddr_list, msg.as_string())  # Отправка письма
            server.quit()
            print(f"Сообщение отправлено.")
            print(
                f"Всего слотов: {total}, Доступно слотов: {available}, Недоступно слотов: {unavailable}"
            )
            print("_____________________________________________")
            time.sleep(2)
            break
        except smtplib.SMTPException as e:
            print(f"Ошибка при отправке письма: {e}. Повторяю отправку...")
            time.sleep(2)
    else:
        print(f"Все попытки отправки письма не увенчались успехом. Ошибка.")
    time.sleep(1)


# Основная функция
def main():
    result = fetch_data(url, headers)  # Получаем данные с сервера
    if isinstance(result, dict):  # Проверка на успешный результат
        available, unavailable, total = count_slots(result)  # Подсчет слотов
        if (
            int(available) < 10
        ):  # Если доступных слотов меньше 10, письмо не отправляется
            print(f"Доступных слотов {available}. НЕ шлю письмо")
        else:
            send_mail(
                available, unavailable, total
            )  # Отправка письма при достаточном количестве слотов
    else:
        print("ОШИБКА")
        send_mail(result=result)  # Отправка письма с текстом ошибки
