import json
import random
import threading
import time

import capsolver
import loguru
import requests
import modules.internxt as internxt

capsolver.api_key = json.loads(open("settings.json","r").read())["capsolver_key"]
class PınterestGen:
    def __init__(self):
        self.session = requests.session()

        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'tr-TR,tr;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        self.internxtmailapi = internxt.Internxt()
        self.email, self.emailToken = self.internxtmailapi.get_new_mail()
        self.accountPassw = "".join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+=-') for i in range(10)])

        proxy = random.choice(open("proxies.txt").readlines()).strip()
        self.session.proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}


    def get_csrf(self):
        response = self.session.get('https://tr.pinterest.com/')
        self.session.headers['x-csrftoken'] = response.cookies['csrftoken']
        self.session.headers['x-pinterest-appstate'] = 'active'
        self.session.headers['x-pinterest-pws-handler'] = 'www/index.js'
        self.session.headers['x-pinterest-source-url'] = '/'
        self.session.headers['x-requested-with'] = 'XMLHttpRequest'
    def get_bday(self):
        current_year = time.localtime().tm_year
        random_years_ago = random.randint(18, 30)
        selected_year = current_year - random_years_ago

        start_time = time.mktime((selected_year, 1, 1, 0, 0, 0, 0, 0, 0))
        end_time = time.mktime((selected_year + 1, 1, 1, 0, 0, 0, 0, 0, 0))

        random_epoch = random.randint(int(start_time), int(end_time))
        return random_epoch
    def solve_recaptcha(self):
        captcha_token = capsolver.solve(
            {
                "type": "ReCaptchaV3EnterpriseTaskProxyless",
                "websiteURL": "https://tr.pinterest.com",
                "websiteKey": "6Ldx7ZkUAAAAAF3SZ05DRL2Kdh911tCa3qFP0-0r",
                "apiDomain": "www.recaptcha.net",
                "pageAction": "web_unauth"
            }
        )["gRecaptchaResponse"]
        loguru.logger.info(f"Captcha solved, {captcha_token[:50]}..")
        return captcha_token
    def send_signup_req(self):
        data = {
            'source_url': '/',
            'data': json.dumps({"options":{"type":"email","birthday":int(self.get_bday()),"email":self.email,"password":self.accountPassw,"country":"US","first_name":"Alita","last_name":"","recaptchaV3Token":self.solve_recaptcha(),"visited_pages":json.dumps([{"path":"/","pageType":"home","ts":int(str(time.time()).replace(".","")[:13])}]),"user_behavior_data":"{}"},"context":{}})
        }

        response = self.session.post('https://tr.pinterest.com/resource/UserRegisterResource/create/',data=data)
        if response.json()["resource_response"]["status"] == "success":
            loguru.logger.success(f"[{self.email}] Account created successfully.")

        pinterest_sess_cookie = self.session.cookies["_pinterest_sess"]

        open("accounts.txt","a").write(f"{self.email}:{self.accountPassw}:{pinterest_sess_cookie}\n")

def handle_tread():
    while True:
        pin = PınterestGen()
        pin.get_csrf()
        pin.send_signup_req()

if __name__ == '__main__':
    thread_count = input("how much thread? > ")
    for i in range(int(thread_count)):
        threading.Thread(target=handle_tread).start()