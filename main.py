import os
import sys
import time
import requests

def red_to_yellow(text):
    colored_lines = []
    for line in text.splitlines():
        last = max(len(line) - 1, 1)
        colored_lines.append("".join(
            f"\033[38;2;255;{round(255 * i / last)};0m{char}"
            for i, char in enumerate(line)
        ))
    return "\n".join(colored_lines) + "\033[0m"

def ask_user(prompt):
    while True:
        answer = input(prompt).strip()
        if answer.lower() == "close":
            print("Exiting...")
            raise SystemExit
        return answer


def ask_yes_no(prompt):
    while True:
        answer = ask_user(prompt)
        normalized = answer.lower()
        if normalized in {"yes", "y", "no", "n"}:
            return normalized in {"yes", "y"}
        print("Please answer with yes or no.")


def check_webhook(url):
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        print(f"Webhook check failed: {exc}")
        return False, None

    if response.status_code == 200:
        try:
            data = response.json()
            name = data.get("name") or "Unknown webhook"
            return True, name
        except ValueError:
            return True, "Unknown webhook"

    print("webhook was deleted, geeg")
    return False, None


def post_message(url, content):
    try:
        response = requests.post(url, json={"content": content}, timeout=10)
    except requests.RequestException as exc:
        print(f"Request error: {exc}")
        return False

    if response.status_code in {200, 201, 204}:
        print("Message posted successfully.")
        return True

    print(f"Failed to post message: {response.status_code} - {response.text[:200]}")
    return False


def delete_webhook(url):
    try:
        response = requests.delete(url, timeout=10)
    except requests.RequestException as exc:
        print(f"Delete request failed: {exc}")
        return False

    if response.status_code in {200, 202, 204}:
        print("Webhook deleted successfully.")
        return True

    if response.status_code in {404, 410}:
        print("webhook was deleted, geeg")
        return False

    print(f"Delete failed: {response.status_code} - {response.text[:200]}")
    return False


def main():
    print(red_to_yellow("""
░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░ 
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░   
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
   ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
                   [1] logger deletion
                   [2] webhook deleter          
"""))                                                              
                                                                                           
    source = ask_user("1 or 2? : ")
    if source == "1":
        webhook_url = ask_user("paste victims webhook here - ")
        if not webhook_url:
            print("No webhook was provided.")
            return

        response = requests.get(webhook_url)
        data = response.json()
        webhook_name = data.get("name")
    
        LOGGER_MESSAGE = """@everyone 
        ```Your ass thought you can send loggers on tiktok/discord without daddy dyw finding your webhooks, dumbass nigger next time you try scam kids with an "open source" logger, try do it better dickknob. anyways join my discord server if you wanna speak to me nigger``` https://discord.gg/duQJPVKDDY.
        https://cdn.discordapp.com/attachments/1562439973825941545/1566799324346851388/togif-4.gif?ex=6aefc9d4&is=6aee7854&hm=97d3e4987479fde13f05179fac78262cc3a9da825b38c1d001abd0cb07812dcb&"""

        LOGGER_SELF_DESTRUCT_MESSAGE = f"""@everyone
        ```oh and btw, ive given your stupid webhook "{webhook_name}" about 180 seconds before it turns emo and kills itself. you will get a message in the meantime``` https://discord.gg/duQJPVKDDY"""
    
        LOGGER_AUTO_DELETE_WARNING_MESSAGE = f"""@everyone
        ```ok, "{webhook_name}" just killed himself, if you still wanna be a dickhead and log kids, make sure to obfuscate your coding.``` https://discord.gg/duQJPVKDDY
        https://klipy.com/gifs/chopper-one"""
        AUTO_DELETE_SECONDS = int(os.getenv("WEBHOOK_TORTURE_SELF_DESTRUCT_SECONDS", "180"))

        valid, webhook_name = check_webhook(webhook_url)
        if not valid:
            print("The webhook is unavailable. Exiting.")
            return

        print(f"Webhook found: {webhook_name}")

        send_normal = ask_yes_no("wanna send the message? (yes/no): ")
        if send_normal:
            post_message(webhook_url, LOGGER_MESSAGE)

        send_self_destruct = ask_yes_no("wanna send self destruction message? (yes/no): ")
        if send_self_destruct:
            post_message(webhook_url, LOGGER_SELF_DESTRUCT_MESSAGE)

        seconds = AUTO_DELETE_SECONDS
        if seconds <= 0:
            seconds = 0

        print(f"Webhook auto-delete timer started for {seconds} seconds.")

        for remaining in range(seconds, 0, -1):
            if remaining <= 5:
                new_name = f"{webhook_name} self destructed lolz"
                edit_data = {"name": new_name,}
                requests.patch(webhook_url, json=edit_data)
                print(f"Auto-deleting in {remaining} seconds...")
                if remaining == 5:
                    post_message(webhook_url, LOGGER_AUTO_DELETE_WARNING_MESSAGE)
            time.sleep(1)

        delete_webhook(webhook_url)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        sys.exit(0)