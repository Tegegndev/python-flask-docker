import requests
import urllib.parse

# class WinzaClient:
#     BASE_URL = 'https://apis-hub.webapis.sk'
#     SESSION = requests.Session()
#     HEADERS = {
#         'accept': 'application/json, text/plain, */*',
#         'accept-language': 'en-US,en;q=0.9,om;q=0.8,ru;q=0.7,am;q=0.6',
#         'origin': 'https://m.winza.bet',
#         'priority': 'u=1, i',
#         'referer': 'https://m.winza.bet/',
#         'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'cross-site',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#         'content-type': 'application/form-urlencoded[]',
#     }
#     SESSION.headers.update(HEADERS)

#     def check_status(self, hpp_token):
#         url = "https://services.santimpay.com/api/v1/gateway/check-status"
#         payload = {"hppToken": hpp_token}
#         headers = {
#             "accept": "application/json, text/plain, */*",
#             "accept-language": "en,en-US;q=0.9",
#             "content-type": "application/json",
#             "origin": "https://services.santimpay.com",
#             "priority": "u=1, i",
#             "referer": "https://services.santimpay.com/",
#             "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
#             "sec-ch-ua-mobile": "?1",
#             "sec-ch-ua-platform": '"Android"',
#             "sec-fetch-dest": "empty",
#             "sec-fetch-mode": "cors",
#             "sec-fetch-site": "same-origin",
#             "user-agent": "Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.67 Mobile Safari/537.36",
#             "x-requested-with": "com.radolyn.ayugram"
#         }
#         response = requests.post(url, json=payload, headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise Exception(f"Check status failed: {response.status_code} - {response.text}")


class WinzaClient:
    BASE_URL = 'https://apis-hub.webapis.sk'
    SESSION = requests.Session()
    HEADERS = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,om;q=0.8,ru;q=0.7,am;q=0.6',
        'origin': 'https://m.winza.bet',
        'priority': 'u=1, i',
        'referer': 'https://m.winza.bet/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'content-type': 'application/form-urlencoded[]',
    }
    SESSION.headers.update(HEADERS)

    def login(self, phone, password):
        url = f'{self.BASE_URL}/AuthApi/token'
        data = {
            'grant_type': 'password',
            'username': phone,
            'password': password,
            'client_id': 'd554ad6f31aa4b5288ab5132f94b65b4',
            'terminal_type': '2',
        }
        response = self.SESSION.post(url=url, data=data, headers=self.HEADERS)
        if response.status_code == 200:
            token = response.json().get('access_token')
            if token:
                self.SESSION.headers.update({'Authorization': f'Bearer {token}'})
            return response.json()
        else:
            return None

    def register_user(self, phone, password):
        url = f"{self.BASE_URL}/UserApi/api/user/v2/tz/registration"
        payload = {
            "PhoneNumber": phone,
            "Password": password,
            "PasswordConfirm": password,
            "AcceptTerms": True,
            "RecordingPersonalData": True,
            "Captcha": "",
            "ReferrerAttendant": "",
            "UserReferrerUrl": "https://services.santimpay.com/"
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en",
            "content-type": "application/json",
            "device-type": "mobile",
            "languageid": "en",
            "origin": "https://m.winza.bet",
            "priority": "u=1, i",
            "referer": "https://m.winza.bet/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "terminalid": "15",
            "user-agent": "Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.67 Mobile Safari/537.36",
            "x-requested-with": "com.radolyn.ayugram"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def deposit(self, amount, provider_id=105):
        url = f"{self.BASE_URL}/WalletApiCore/api/wallet/deposit"
        payload = {
            "ProviderId": provider_id,
            "DepositAmount": amount,
            "SaveCardId": False,
            "UserMail": None,
            "VerificationCode": None,
            "SelectedBonusId": None,
            "SuccessfulUrl": "https://tegegndev.vercel.app",
            "UnsuccessfulUrl": "https://tegegndev.vercel.app"
        }
        headers = self.SESSION.headers.copy()
        headers.update({
            "content-type": "application/json",
            "device-type": "desktop",
            "languageid": "en",
            "terminalid": "14"
        })
        response = self.SESSION.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            redirect_url = result.get("RedirectUrl")
            hpp_token = None
            if redirect_url:
                parsed = urllib.parse.urlparse(redirect_url)
                query = urllib.parse.parse_qs(parsed.query)
                data_param = query.get("data", [None])[0]
                if data_param:
                    hpp_token = data_param
                    print(f"HPP Token: {hpp_token[:20]}...")
            return result
        else:
            return None

    def pay_with_telebirr(self, phone_number, token):
        url = "https://services.santimpay.com/api/v1/gateway/process-payment"
        payload = {
            "paymentMethod": "Telebirr",
            "phoneNumber": phone_number,
            "token": token
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en,en-US;q=0.9",
            "content-type": "application/json",
            "origin": "https://services.santimpay.com",
            "priority": "u=1, i",
            "referer": "https://services.santimpay.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.67 Mobile Safari/537.36",
            "x-requested-with": "com.radolyn.ayugram"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def pay_with_cbe(self, phone_number, token):
        url = "https://services.santimpay.com/api/v1/gateway/process-payment"
        payload = {
            "paymentMethod": "CBE",
            "phoneNumber": phone_number,
            "token": token
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en,en-US;q=0.9",
            "content-type": "application/json",
            "origin": "https://services.santimpay.com",
            "priority": "u=1, i",
            "referer": "https://services.santimpay.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.67 Mobile Safari/537.36",
            "x-requested-with": "com.radolyn.ayugram"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def pay_with_cbe_birr(self, phone_number, token):
        url = "https://services.santimpay.com/api/v1/gateway/process-payment"
        payload = {
            "paymentMethod": "CBE Birr",
            "phoneNumber": phone_number,
            "token": token
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en,en-US;q=0.9",
            "content-type": "application/json",
            "origin": "https://services.santimpay.com",
            "priority": "u=1, i",
            "referer": "https://services.santimpay.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.67 Mobile Safari/537.36",
            "x-requested-with": "com.radolyn.ayugram"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None


if __name__ == '__main__':
    client = WinzaClient()
    #login 
    phone = '0987624298'
    password = '28146511'
    login_response = client.login(phone, password)
    if login_response:
        print("Login successful:", login_response)
    else:
        print("Login failed")