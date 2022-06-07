from flask import Flask, request, jsonify, abort
import socket
import json


# 챗봇 엔진 서버 접속 정보
# 이전에 만든 챗봇 엔진 서버에서 설정한 포트를 사용해야 한다
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)

# cors 가 문제다...
from flask_cors import CORS
CORS(app)

# 챗봇 엔진 서버와 통신 (소켓 통신!)
# 질의를 전송하고, 답변데이터를 수신한 경우 JSON 문자열을 dict 객체로 변환
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data


# 챗봇 에진 query 전송 API
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):

    data = request.get_json()
    try:        
        if bot_type == 'TEST':
            ret = get_answer_from_engine(bottype=bot_type, query=data['query'])
            return jsonify(ret)

        elif bot_type == "KAKAO":
            # 카카오톡 스킬 처리
            pass

        elif bot_type == "NAVER":
            # 네이버톡톡 Web hook 처리
            pass
        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 에러
        abort(500)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.10', port=5000)