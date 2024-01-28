import pathway as pw

import requests
from api.service import host

print("Starting logger")


table = pw.demo.range_stream(nb_rows=100000000)

print(table.value)

seconds = 0

content = {
    "content": "",
    "embeds": None,
    "attachments": []
}


def on_change(key: pw.Pointer, row: dict, time: int, is_addition: bool):
    global seconds
    seconds += 1
    print("Seconds: ", seconds)
    if seconds >= 20:
        seconds = 0
    else:
        return
    # send discord webhook
    host_deets = host.hostinfo()
    uptime = host.uptime()
    content["content"] = f"**{host_deets['hostname']}**\n" \
                         f"**OS**: {host_deets['os']}\n" \
                         f"**CPU**: {host_deets['cpu']} ({host_deets['cpu_threads']} threads)\n" \
                         f"**CPU Usage**: {host_deets['cpu_usage']}%\n" \
                         f"**Memory Usage**: {host_deets['memory_usage']}%\n" \
                         f"**Uptime**: {uptime['text']}\n"
    url = (r"https://canary.discord.com/api/webhooks/1201118785856340028"
           r"/wBzmHqnarASUcOUWB6e6MrlGW4fsMGo5wnCcGhslRCUprYtb0KvAo3a0i9K84DSsKZ8W")
    requests.post(url, json=content)
    # send webhook


pw.io.subscribe(table, on_change)

pw.run()
