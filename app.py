from flask import Flask, escape, request, render_template
from decouple import config
import requests
import html

app = Flask(__name__)

api_url = "https://api.telegram.org/bot"
token = config("TELEGRAM_BOT_TOKEN")
google_key = config("GOOGLE_TRANSLATE_KEY")
naver_id = config("NAVER_CLIENT_ID")
naver_secret = config("NAVER_SECRET")


# @app.route('/')
# def hello():
#     name = request.args.get("name", "World")
#     return f'Hello, {escape(name)}!'


# @app.route("/write")
# def write():
#     return render_template("write.html")

# @app.route("/send")
# def send():
#     user_input = request.args.get("user_input")
#     get_user_api = f"{api_url}{token}/getUpdates"

#     res = requests.get(get_user_api).json()
    
#     user_id = res["result"][0]["message"]["from"]["id"]

#     send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}"
#     requests.get(send_url)
#     return render_template("send.html")

#telegram에서 보낸 메세지를 flask와 연결하는 작업
#번외 local 서버를 외부에서 접속 하는 방법중 ngrok을 사용해 서버를 받을 수 있다. 서버 설정은 ./ngrok http 5000 
# flask 에 설정되어 있는 5000이라는 포트 번호 -> 개발자 모드 최대 사용 시간 7시간
# @app.route("/telegram" , methods = ["POST"])
# def telegram():
#     req = request.get_json()

#     user_id = req["message"]["from"]["id"]
#     user_input = req["message"]['text']

#     if user_input == '로또':
#         return_data = '로또를 입력하셨습니다.'
#     elif user_input[0:2] == '번역':
#         google_api_url = 'https://translation.googleapis.com/language/translate/v2'
#         before_text = user_input[3:]
#         data ={
#             'q' : before_text,
#             'source' : 'ko',
#             'target' : 'en'
#         }
#         request_url = f'{google_api_url}?key={google_key}'
#         res = requests.post(request_url, data).json()

#         escaped_data = res['data']['translations'][0]['translatedText']
#         return_data = html.unescape(escaped_data)
#         print (return_data)

#     else:
#         return_data = '사용가능한 명령어가 아닙니다.'

#     send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}"
#     requests.get(send_url)
#     return "ok" , 200

@app.route("/telegram" , methods = ["POST"])
def telegram():

    req = request.get_json()
    user_id = req["message"]["from"]["id"]
    user_input = req["message"]['text']

    naver_api_url = 'https://openapi.naver.com/v1/search/movie.json'
    headers = {"X-Naver-Client-Id" : naver_id, "X-Naver-Client-Secret" : naver_secret}

    request_url = f'{naver_api_url}?query={user_input}&display=1'
    res = requests.get(request_url, headers=headers).json()


    if user_input == '/start':
        return_data = '환영합니다. 영화를 검색합니다.'

    else:
        try:
            res = res['items'][0]
            return_data = f"\n 제목 : {res['title'].replace('<b>','').replace('</b>','')}" \
                + f"\n 상세정보 : {res['link']}" \
                + f"\n 영어제목 : {res['subtitle']}" \
                + f"\n 제작년도 : {res['pubDate']}" \
                + f"\n 감독 : {res['director']}" \
                + f"\n 배우 : {res['actor']}" \
                + f"\n 평점 : {res['userRating']}"
        except:
            return_data = '검색결과가 없습니다.'
        print(res)

    send_url = f"https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}"
    requests.get(send_url)
    return "ok" , 200


if __name__ == '__main__':
    app.run(debug=True)