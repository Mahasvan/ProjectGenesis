import requests


def close_running_instance(config):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((config.get("host"), config.get("port")))
    except socket.error:
        print("Port is already in use. Shutting down running instance...")

        try:
            requests.get(f"http://{config.get('host')}:{config.get('port')}/host/shutdown")
        except requests.exceptions.ConnectionError:
            print("Could not connect to running instance. Assuming it is already shut down...")
        else:
            print("Closed running instance.")