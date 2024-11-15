import threading
import random
from fake_useragent import UserAgent
import requests
from termcolor import colored
import string

def load_proxies_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def generate_phone_number():
    country_codes = ['+1', '+7', '+20', '+30', '+31', '+32', '+33', '+34', '+36', '+39', '+40', '+41', '+42', '+43', '+44', '+45', '+46', '+47', '+48', '+49', '+51', '+52', '+53', '+54', '+55', '+56', '+57', '+58', '+60', '+61', '+62', '+63', '+64', '+65', '+66', '+81', '+82', '+84', '+86', '+90', '+91', '+92', '+93', '+94', '+95', '+98', '+212', '+213', '+216', '+218', '+220', '+221', '+222', '+223', '+224', '+225', '+226', '+227', '+228', '+229', '+230', '+231', '+232', '+233', '+234', '+235', '+236', '+237', '+238', '+239', '+240', '+241', '+242', '+243', '+244', '+245', '+246', '+247']
    country_code = random.choice(country_codes)
    phone_number = ''.join(random.choices('0123456789', k=10))
    formatted_phone_number = f'{country_code}{phone_number}'
    return formatted_phone_number

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru", "aol.com", "icloud.com", "zoho.com", "yandex.ru", "protonmail.com", "tutanota.com", "gmx.com", "inbox.com", "fastmail.com", "libero.it", "seznam.cz", "qq.com", "126.com", "163.com", "web.de"]
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    return email

def send_complaint(username, telegram_id, number, email, repeats, complaint_choice, proxies=None):
    url = 'https://telegram.org/support'
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    complaints_sent = 0

    text = f'Добрый день поддержка Telegram! Аккаунт {username}, {telegram_id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться.Прошу разберитесь с этим. Заранее спасибо!'

    payload = {'text': text, 'number': number, 'email': email}

    try:
        for _ in range(int(repeats)):
            response = requests.post(url, headers=headers, data=payload, proxies=proxies)
            if response.status_code == 200:
                print(colored(f"Send: {email} {number} {proxies}", 'green'))
            else:
                print("ERROR. code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

def send_complaints_thread(username, telegram_id, repeats, proxies_list):
    number = generate_phone_number()
    email = generate_random_email()
    if proxies_list:
        proxies = {'http': random.choice(proxies_list)}
    else:
        proxies = None
    send_complaint(username, telegram_id, number, email, repeats, "1", proxies)

def main():
    proxy_file = 'proxies.txt'
    proxies_list = load_proxies_from_file(proxy_file)

    username = input(colored(f"Enter username: ", "green"))
    telegram_id = input(colored(f"Enter Telegram ID: ", "green"))
    repeats = int(input(colored(f"How many reports make?: ", "green")))

    max_threads = 4
    threads = []

    for _ in range(repeats):
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []

        thread = threading.Thread(target=send_complaints_thread, args=(username, telegram_id, 1, proxies_list))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
