from decouple import config
token = config("TELEGRAM_BOT_TOKEN")
ngrok_url = "https://33050e73.ngrok.io/telegram"
ngrok_url = "https://time9300.pythonanywhere.com/telegram"
url = f"https://api.telegram.org/bot{token}/setWebHook"

#setWedHook이라는 aip를 사용하는데 연결 시킬 url은 ?url={ngrok_url} 라는 형식을 가진다.
setWebHook_url  = f"{url}?url={ngrok_url}"

print(setWebHook_url)