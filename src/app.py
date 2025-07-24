
from flask import Flask, request, jsonify
import json
import os
from core import WinzaClient
import requests
# Master endpoint: login/register, deposit, save hpp token

def pay_with_telebirr(phone_number, token):
    """
    Pay with Telebirr using Santimpay API.
    Args:
        phone_number (str): Phone number in format +251XXXXXXXXX
        token (str): JWT token string
    Returns:
        dict: API response
    """
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
        raise Exception(f"Telebirr payment failed: {response.status_code} - {response.text}")

def pay_with_cbe(phone_number, token):
    """
    Pay with CBE Bank App using Santimpay API.
    Args:
        phone_number (str): Phone number in format +251XXXXXXXXX
        token (str): JWT token string
    Returns:
        dict: API response
    """
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
        raise Exception(f"CBE payment failed: {response.status_code} - {response.text}")


def check_status(hpp_token):
    url = "https://services.santimpay.com/api/v1/gateway/check-status"
    payload = {"hppToken": hpp_token}
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
        raise Exception(f"Check status failed: {response.status_code} - {response.text}")

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    client = WinzaClient()
    result = client.login(phone, password)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Login failed'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    client = WinzaClient()
    result = client.register_user(phone, password)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Registration failed'}), 400

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    amount = data.get('amount')
    client = WinzaClient()
    login_result = client.login(phone, password)
    if not login_result:
        reg_result = client.register_user(phone, password)
        if not reg_result or not reg_result.get('IsSuccess'):
            return jsonify({'error': 'Registration failed'}), 400
        login_result = client.login(phone, password)
        if not login_result:
            return jsonify({'error': 'Login failed after registration'}), 401
    deposit_result = client.deposit(amount)
    return jsonify(deposit_result)




# Master endpoint: login/register, deposit, save hpp token
@app.route('/master', methods=['POST'])
def master():
    data = request.json
    phone = data.get('phone')
    #formated phon from 09... to +251
    if not phone.startswith('+'):
        if phone.startswith('09'):
            fphone = '+251' + phone[1:]
        elif phone.startswith('0'):
            fphone = '+251' + phone[1:]
        else:
            fphone = '+251' + phone
    password = data.get('password')
    amount = data.get('amount')
    payment_method = data.get('payment_method')  # 'deposit', 'telebirr', 'cbe', 'cbe_birr'
    # Do not expect token from user; get from login response
    token = None
    client = WinzaClient()
    login_result = client.login(phone, password)
    if not login_result:
        reg_result = client.register_user(phone, password)
        if not reg_result or not reg_result.get('IsSuccess'):
            return jsonify({'error': 'Registration failed'}), 400
        login_result = client.login(phone, password)
        if not login_result:
            return jsonify({'error': 'Login failed after registration'}), 401

    result_data = {}
    hpp_token = None
    if payment_method in ['telebirr', 'cbe', 'cbe_birr']:
        # Always initiate deposit to get hpp_token (not access_token)
        deposit_result = client.deposit(amount)
        result_data['deposit'] = deposit_result
        redirect_url = deposit_result.get('RedirectUrl') if deposit_result else None
        hpp_token = None
        if redirect_url:
            import urllib.parse
            parsed = urllib.parse.urlparse(redirect_url)
            query = urllib.parse.parse_qs(parsed.query)
            hpp_token = query.get('data', [None])[0]
        if not hpp_token:
            return jsonify({'error': f'Could not retrieve a valid hpp_token for {payment_method} payment from deposit. Please check deposit response.'}), 400
        if payment_method == 'telebirr':
            pay_result = pay_with_telebirr(fphone, hpp_token)
            result_data['pay_with_telebirr'] = pay_result
            redirect_url = pay_result.get('RedirectUrl') if pay_result else redirect_url
        elif payment_method == 'cbe':
            pay_result = pay_with_cbe(fphone, hpp_token)
            result_data['pay_with_cbe'] = pay_result
            redirect_url = pay_result.get('RedirectUrl') if pay_result else redirect_url
        elif payment_method == 'cbe_birr':
            pay_result = client.pay_with_cbe_birr(fphone, hpp_token)
            result_data['pay_with_cbe_birr'] = pay_result
            redirect_url = pay_result.get('RedirectUrl') if pay_result else redirect_url
    else:
        deposit_result = client.deposit(amount)
        result_data['deposit'] = deposit_result
        redirect_url = deposit_result.get('RedirectUrl') if deposit_result else None

    if redirect_url:
        import urllib.parse
        parsed = urllib.parse.urlparse(redirect_url)
        query = urllib.parse.parse_qs(parsed.query)
        hpp_token = query.get('data', [None])[0]

    # Save hpp token and phone as JSON (single file)
    user_json_path = 'hpp_tokens.json'
    user_data = {}
    if os.path.exists(user_json_path):
        with open(user_json_path, 'r', encoding='utf-8') as f:
            try:
                user_data = json.load(f)
            except Exception:
                user_data = {}

    # After deposit/payment, check status if hpp_token exists
    status_data = None
    ref_id = None
    if hpp_token:
        try:
            status_resp = check_status(hpp_token)
            status_data = status_resp.get('status')
            ref_id = status_resp.get('refId')
        except Exception:
            status_data = None
            ref_id = None
        payment_check_url = f"/check_status?hpp_token={hpp_token}"
        user_data[phone] = {
            'phone': phone,
            'hpp_token': hpp_token,
            'amount': amount,
            'status': status_data,
            'refId': ref_id,
            'payment_check_url': payment_check_url
        }
        with open(user_json_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
    else:
        payment_check_url = None

    return jsonify({
        'login': login_result,
        'result': result_data,
        'hpp_token': hpp_token,
        'status': status_data,
        'refId': ref_id,
        'amount': amount,
        'payment_check_url': request.host_url.rstrip('/') + payment_check_url if payment_check_url else None
    })


# New endpoint for checking payment status by hpp_token
@app.route('/check_status', methods=['GET'])
def check_status_api():
    hpp_token = request.args.get('hpp_token')
    if not hpp_token:
        return jsonify({'error': 'Missing hpp_token'}), 400
    try:
        status_resp = check_status(hpp_token)
        return jsonify(status_resp)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
