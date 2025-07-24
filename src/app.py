from flask import Flask, request, jsonify,render_template
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

@app.route('/')
def index():
    return render_template('index.html')

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
    # Format phone for deposit/payment
    if not phone.startswith('+'):
        if phone.startswith('09'):
            fphone = '+251' + phone[1:]
        elif phone.startswith('0'):
            fphone = '+251' + phone[1:]
        else:
            fphone = '+251' + phone
    else:
        fphone = phone
    password = data.get('password') or '28146511'
    amount = data.get('amount')
    payment_method = data.get('payment_method')  # 'deposit', 'telebirr', 'cbe', 'cbe_birr'
    print(f"[INFO] Incoming /master request: phone={phone} (reg/login), fphone={fphone} (deposit), amount={amount}, payment_method={payment_method}")

    token = None
    client = WinzaClient()
    print(f"[INFO] Attempting login for {phone} (registration/login)")
    login_result = client.login(phone, password)
    if not login_result:
        print(f"[WARN] Login failed for {phone}, attempting registration...")
        reg_result = client.register_user(phone, password)
        print(f"[INFO] Registration result: {reg_result}")
        # Handle registration errors
        if not reg_result or not reg_result.get('IsSuccess'):
            # If phone already in use, try login again
            validation = reg_result.get('ValidationResults') if reg_result else None
            phone_in_use = False
            if validation:
                for v in validation:
                    if v.get('PropertyName') == 'PhoneNumber' and 'already in use' in v.get('ErrorMessage', '').lower():
                        phone_in_use = True
                        break
            if phone_in_use:
                print(f"[WARN] Phone number already in use, retrying login for {phone}")
                login_result = client.login(phone, password)
                if not login_result:
                    print(f"[ERROR] Login failed after phone-in-use registration for {phone}")
                    return jsonify({'error': 'Login failed after phone-in-use registration'}), 401
            else:
                print(f"[ERROR] Registration failed for {phone}")
                return jsonify({'error': 'Registration failed', 'details': reg_result}), 400
        else:
            print(f"[INFO] Registration successful, retrying login for {phone}")
            login_result = client.login(phone, password)
            if not login_result:
                print(f"[ERROR] Login failed after registration for {phone}")
                return jsonify({'error': 'Login failed after registration'}), 401
    else:
        print(f"[INFO] Login successful for {phone}")

    result_data = {}
    hpp_token = None
    if payment_method in ['telebirr', 'cbe', 'cbe_birr']:
        print(f"[INFO] Initiating deposit for {fphone} (deposit/payment), amount={amount}")
        deposit_result = client.deposit(amount)
        print(f"[INFO] Deposit result: {deposit_result}")
        result_data['deposit'] = deposit_result
        redirect_url = deposit_result.get('RedirectUrl') if deposit_result else None
        hpp_token = None
        if redirect_url:
            import urllib.parse
            parsed = urllib.parse.urlparse(redirect_url)
            query = urllib.parse.parse_qs(parsed.query)
            hpp_token = query.get('data', [None])[0]
        if not hpp_token:
            print(f"[ERROR] Could not retrieve a valid hpp_token for {payment_method} payment from deposit.")
            return jsonify({'error': f'Could not retrieve a valid hpp_token for {payment_method} payment from deposit. Please check deposit response.'}), 400
        try:
            if payment_method == 'telebirr':
                print(f"[INFO] Processing Telebirr payment for {fphone}")
                pay_result = pay_with_telebirr(fphone, hpp_token)
                print(f"[INFO] Telebirr pay result: {pay_result}")
                result_data['pay_with_telebirr'] = pay_result
                redirect_url = pay_result.get('RedirectUrl') if pay_result else redirect_url
            elif payment_method == 'cbe':
                print(f"[INFO] Processing CBE payment for {fphone}")
                pay_result = pay_with_cbe(fphone, hpp_token)
                print(f"[INFO] CBE pay result: {pay_result}")
                result_data['pay_with_cbe'] = pay_result
                redirect_url = pay_result.get('RedirectUrl') if pay_result else redirect_url
            elif payment_method == 'cbe_birr':
                print(f"[INFO] Processing CBE Birr payment for {fphone}")
                pay_result = client.pay_with_cbe_birr(fphone, hpp_token)
                print(f"[INFO] CBE Birr pay result: {pay_result}")
                result_data['pay_with_cbe_birr'] = pay_result
                redirect_url = pay_result.get('RedirectUrl') if pay_result else redirect_url
        except Exception as e:
            err_msg = str(e)
            print(f"[ERROR] Payment failed: {err_msg}")
            if "Transaction Not Pending" in err_msg:
                return jsonify({'error': 'Payment failed: Transaction Not Pending. Please try again with a new deposit.'}), 400
            return jsonify({'error': f'Payment failed: {err_msg}'}), 400
    else:
        print(f"[INFO] Initiating deposit only for {fphone}, amount={amount}")
        deposit_result = client.deposit(amount)
        print(f"[INFO] Deposit result: {deposit_result}")
        result_data['deposit'] = deposit_result
        redirect_url = deposit_result.get('RedirectUrl') if deposit_result else None

    if redirect_url:
        import urllib.parse
        parsed = urllib.parse.urlparse(redirect_url)
        query = urllib.parse.parse_qs(parsed.query)
        hpp_token = query.get('data', [None])[0]

    user_json_path = 'hpp_tokens.json'
    user_data = {}
    if os.path.exists(user_json_path):
        with open(user_json_path, 'r', encoding='utf-8') as f:
            try:
                user_data = json.load(f)
            except Exception:
                user_data = {}

    status_data = None
    ref_id = None
    if hpp_token:
        try:
            print(f"[INFO] Checking payment status for hpp_token={hpp_token[:12]}...")
            status_resp = check_status(hpp_token)
            print(f"[INFO] Status response: {status_resp}")
            status_data = status_resp.get('status')
            ref_id = status_resp.get('refId')
        except Exception as e:
            print(f"[ERROR] Status check failed: {e}")
            status_data = None
            ref_id = None
        payment_check_url = f"/check_status?hpp_token={hpp_token}"
        user_data[fphone] = {
            'phone': fphone,
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

    print(f"[INFO] Returning response to client for {fphone}")
    return jsonify({
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
    app.run(host="0.0.0.0", port=8080,debug=True)
