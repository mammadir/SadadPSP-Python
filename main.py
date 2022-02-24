import base64
import datetime
import json
import uuid
import requests
from Crypto.Cipher import DES3
key = ""  # Your Key
MerchantId = ""  # YourMerchantId
TerminalId = ""  # YourTerminalId
Amount = 2  # YourAmount (Rials)
OrderId = int(str(uuid.uuid4().int)[-1 * 16:])  # orderID
LocalDateTime = datetime.datetime.today().strftime("%m/%d/%Y %H:%M:%S %a")  # DateTime
ReturnUrl = "http://YourSite.Com/verify.php"  # Return Url


def pad(text, pad_size=16):
    text_length = len(text)
    last_block_size = text_length % pad_size
    remaining_space = pad_size - last_block_size
    text = text + (remaining_space * chr(remaining_space))
    return text


def encrypt_des3(text):
    secret_key_bytes = base64.b64decode(key)
    text = pad(text, 8)
    cipher = DES3.new(secret_key_bytes, DES3.MODE_ECB)
    cipher_text = cipher.encrypt(str.encode(text))
    return base64.b64encode(cipher_text).decode("utf-8")


def get_payment_link():
    text = TerminalId + ';' + str(OrderId) + ';' + str(Amount)
    sign_data = encrypt_des3(text)
    data = {
        'TerminalId': TerminalId,
        'MerchantId': MerchantId,
        'Amount': Amount,
        'SignData': sign_data,
        'ReturnUrl': ReturnUrl,
        'LocalDateTime': LocalDateTime,
        'OrderId': OrderId,
    }
    response = requests.post("https://sadad.shaparak.ir/vpg/api/v0/Request/PaymentRequest", data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
    load_json = json.loads(response.content)
    if int(load_json['ResCode']) == 0:
        print(load_json)
        print("Payment Link : https://sadad.shaparak.ir/VPG/Purchase?Token=" + load_json['Token'])
        print("Payment Order ID : " + str(OrderId))
    else:
        print(load_json)


def get_payment_info(Token):
    data = {
        'Token': Token,
        'SignData': encrypt_des3(Token),
    }
    response = requests.post("https://sadad.shaparak.ir/vpg/api/v0/Advice/Verify", data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
    print(response.content.decode())
    # اگر ResCode صفر یا منفی 1 بود یعنی پرداخت انجام نشده


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_payment_link()  # دریافت لینک پرداخت
    # get_payment_info(Token) #دریافت اطلاعات پرداخت شده داخل تابع توکن برگشتی را وارد کنید


