import requests

class Internxt:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'tr-TR,tr;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://internxt.com/temporary-email',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def get_new_mail(self):
        response = self.session.get('https://internxt.com/api/temp-mail/create-email')
        return response.json()["address"], response.json()["token"]
    def get_inbox(self, mail_token):
        params = {
            'token': mail_token,
        }

        response = self.session.get('https://internxt.com/api/temp-mail/get-inbox', params=params)
        return response.json()["emails"]


