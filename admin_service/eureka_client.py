import requests
import socket
import atexit
import time
import threading
from config import Config

EUREKA_SERVER = Config.EUREKA_SERVER.rstrip("/")
APP_NAME = Config.APP_NAME
PORT = Config.APP_PORT

HOSTNAME = socket.gethostname()
IP_ADDR = socket.gethostbyname(HOSTNAME)
INSTANCE_ID = f"{HOSTNAME}:{APP_NAME}:{PORT}"

registration_payload = {
    "instance": {
        "instanceId": INSTANCE_ID,
        "app": APP_NAME.upper(),
        "hostName": IP_ADDR,
        "ipAddr": IP_ADDR,
        "vipAddress": APP_NAME.lower(),
        "secureVipAddress": APP_NAME.lower(),
        "status": "UP",

        "port": {
            "$": PORT,
            "@enabled": "true"
        },

        "healthCheckUrl": f"http://{IP_ADDR}:{PORT}/actuator/health",
        "statusPageUrl": f"http://{IP_ADDR}:{PORT}/actuator/health",
        "homePageUrl": f"http://{IP_ADDR}:{PORT}/",

        "metadata": {
            "management.port": str(PORT)
        },

        "dataCenterInfo": {
            "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
            "name": "MyOwn"
        }
    }
}

def register_to_eureka():
    url = f"{EUREKA_SERVER}/apps/{APP_NAME}"
    try:
        print("Registering to Eureka:", url)
        r = requests.post(url, json=registration_payload, headers={"Content-Type": "application/json"})
        if r.status_code in (200, 204):
            print("Registered to Eureka")
        else:
            print("Eureka registration status:", r.status_code, r.text)
    except Exception as e:
        print("Eureka registration failed:", e)

def send_heartbeat():
    url = f"{EUREKA_SERVER}/apps/{APP_NAME}/{INSTANCE_ID}"
    while True:
        try:
            requests.put(url)
        except Exception:
            pass
        time.sleep(30)

def deregister_from_eureka():
    url = f"{EUREKA_SERVER}/apps/{APP_NAME}/{INSTANCE_ID}"
    try:
        requests.delete(url)
        print("Deregistered from Eureka")
    except Exception:
        pass

def start_eureka_client():
    # register once
    try:
        register_to_eureka()
    except Exception as e:
        print("Eureka registration exception:", e)
    # start heartbeat
    t = threading.Thread(target=send_heartbeat)
    t.daemon = True
    t.start()
    atexit.register(deregister_from_eureka)
