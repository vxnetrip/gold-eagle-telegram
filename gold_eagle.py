import time

import random

import json

import tls_client

import base64

import hmac

import hashlib

import binascii

from colorama import init as clinit

from Crypto.PublicKey import RSA

from Crypto.Cipher import PKCS1_v1_5


clinit(autoreset=True)

# ✅ Terminal Colors

CYAN = "\033[96m"

YELLOW = "\033[93m"

GREEN = "\033[92m"

RED = "\033[91m"

BOLD = "\033[1m"

RESET = "\033[0m"

# ✅ Constants

SECRET = "FZYQHANLB3I2KAWEOKI4T2PVXHHZ4K5F"

ME_API_URL = "https://gold-eagle-api.fly.dev/user/me/progress"

TAP_API_URL = "https://gold-eagle-api.fly.dev/tap"

PEM = """-----BEGIN PUBLIC KEY-----

MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyH0A/d/2Dc1QGDCpVgD/

8Xx1o3GHccjybtK3AM4Wv0faLZL6J1jDLGdmOEnE2+HkTuxTBSVBZT1a+8Iazxkd

LqTihCZxGUxp6i9CZatICimC7LbdGJW++t+X9l7EH6uEBPuSjQcuNuaODQkefncW

//rni5iksdd3pjQRLM+PVEMzPw+pvgfPfAn0fUDqer0itUJFQ5P0+tVaL/6AlcBY

EqnirvIo8tfps/+9yGqc2znCVWwaR+1uCeVZ6gbt96XPVxaGf+hKn+TwiJo2sykH

OGADDSK8sEWca7DqSQScGSTc5/DD2CeSK78pwlhYOQb6694PI0Cr5g+tpPm94gk/

nwIDAQAB

-----END PUBLIC KEY-----

"""

# ✅ Define Tokens Directly

session = tls_client.Session(
    client_identifier="chrome_135",
    random_tls_extension_order=True
)

TOKENS = [
    "ENTER YOUR TOKEN HERE"
]

# ✅ Get progress
def get_available_energy(token: str):
    headers = {
        'authority': 'gold-eagle-api.fly.dev',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'origin': 'https://telegram.geagle.online',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://telegram.geagle.online/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    

    try:
        response = session.get(ME_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Resp: {response.status_code} {response.text}")
    except Exception as e:
        print(f"{RED}[-] Error {token[:10]}... {e}{RESET}")

    
    
    
    
    
    

# ✅ Load Tokens from Variable

def load_tokens():

    return TOKENS  # Directly returning the list of tokens




# ✅ Generate TOTP

def generate_totp_in_base64(secret_base32, step=3, digits=6, algorithm=hashlib.sha256):

    try:

        secret_bytes = base64.b32decode(secret_base32, casefold=True)

    except binascii.Error:

        raise ValueError("Invalid Base32 secret format!")

    time_counter = int(time.time() // step)

    time_counter_bytes = time_counter.to_bytes(8, byteorder="big")

    

    hmac_hash = hmac.new(secret_bytes, time_counter_bytes, algorithm).digest()

    offset = hmac_hash[-1] & 0x0F

    code_int = int.from_bytes(hmac_hash[offset:offset+4], byteorder="big") & 0x7FFFFFFF

    otp = code_int % (10 ** digits)

    

    return base64.b64encode(str(otp).zfill(digits).encode()).decode()

# ✅ RSA Encrypt Tap Data with Retry

def calculateGoldEagleData(taps, current_nonce, retries=3):

    input_data = {"st": taps, "ct": current_nonce}

    json_bytes = json.dumps(input_data).encode("utf-8")

    public_key = RSA.importKey(PEM)

    cipher = PKCS1_v1_5.new(public_key)

    for attempt in range(1, retries + 1):

        try:

            encrypted_data = cipher.encrypt(json_bytes)

            return base64.b64encode(encrypted_data).decode("utf-8")

        except Exception as e:

            print(f"{RED}[-] RSA Encryption Error (Attempt {attempt}/{retries}): {e}{RESET}")

            time.sleep(1)  # Wait 1 second before retrying

    print(f"{RED}[-] Failed to encrypt after {retries} attempts. Skipping token.{RESET}")

    return None

# ✅ Prepare Request Data

def prepare_data(count, secret):

    generated_nonce = generate_totp_in_base64(secret_base32=secret)

    calculationResult = calculateGoldEagleData(count, generated_nonce)

    if not calculationResult:

        return None  # Prevent sending invalid data

    return {"data": calculationResult}

def send_tap_request(token, index, total):
    

    taps_count = random.randint(950, 960)

    # headers = {

    #     "authority": "gold-eagle-api.fly.dev",

    #     "accept": "application/json, text/plain, */*",

    #     "authorization": f"Bearer {token}",

    #     "content-type": "application/json",

    #     "origin": "https://telegram.geagle.online",

    #     "referer": "https://telegram.geagle.online/",

    #     "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',

    #     "sec-ch-ua-mobile": "?1",

    #     "sec-ch-ua-platform": '"Android"',

    #     "sec-fetch-dest": "empty",

    #     "sec-fetch-mode": "cors",

    #     "sec-fetch-site": "cross-site",

    #     "user-agent": "Mozilla/5.0 (Linux; Android 10)"

    # }
    
    headers = {
        'authority': 'gold-eagle-api.fly.dev',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://telegram.geagle.online',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://telegram.geagle.online/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    print(f"{GREEN}[+] Running Token {index}/{total}: {BOLD}{token[:10]}...{RESET}")
    
    while True:

        me_response = get_available_energy(token)
        
        if me_response is not None:
        
            current_energy = me_response['energy']
            max_energy = me_response['max_energy']
            print(f"{GREEN}[INFO] Energy: {current_energy}/{max_energy}{RESET}")
            
            if current_energy >= taps_count:


                data = prepare_data(taps_count, SECRET)

                if not data:

                    print(f"{RED}[-] Skipping token {index} due to encryption error.{RESET}")

                    return None

                try:
                    response = session.post(TAP_API_URL, json=data, headers=headers)
                    
                    if response.status_code == 200:
                        print(f"{GREEN}[+] Token {index}/{total} | Taps: {taps_count} | Response ({response.status_code}): {response.text}{RESET}")
                        return response.json()
                    else:
                        print(f"{YELLOW}[!] Token {index}/{total} | Taps: {taps_count} | Response ({response.status_code}): {response.text}{RESET}")
                except Exception as e:
                    print(f"{RED}[-] Connection Error for Token {index}/{total}: {token[:10]}... {e}{RESET}")
                    
                time.sleep(3)
            else:
                calculate_wait_time = (taps_count - current_energy) + 1
                print(f"{YELLOW}[!] Token {index}/{total} | Taps: {taps_count} | Low Energy ({current_energy}/{max_energy})... Waiting {calculate_wait_time // 60} minutes {calculate_wait_time % 60} seconds...{RESET}")
                time.sleep(calculate_wait_time)

    

        

    

if __name__ == "__main__":

    tokens = load_tokens()

    

    if not tokens:

        print(f"{RED}[-] No tokens found! Exiting...{RESET}")

    # elif not proxies:

    #     print(f"{RED}[-] No proxies found! Exiting...{RESET}")

    else:

        while True:

            total_tokens = len(tokens)

            for i, token in enumerate(tokens):
                send_tap_request(token, i, total_tokens)
            