# control/runner.py

from agent.ImageAgent import ImageAgent
from control.microbit import send_to_microbit


def get_color():
    print("🎥 카메라로 이미지 캡처 후 GPT에게 색상 분류 요청 중...")
    agent = ImageAgent()
    try:
        color = agent.classify()
        print(f"🎨 LLM이 분류한 색상: {color}")
        return color
    except Exception as e:
        print(f"❌ get_color 실패: {e}")
        return "unknown"


def move(direction):
    print(f"🛞 모터를 {direction} 방향으로 회전합니다.")
    send_to_microbit(direction)


def printp(value):
    print(f"📢 출력: {value}")


# 2. 전달된 코드 문자열 실행 함수
def execute_code(code: str):
    global_namespace = {
        "get_color": get_color,
        "move": move,
        "printp": printp,
    }

    # 전달된 코드 컴파일 및 실행
    exec(code, global_namespace)

    # user_code()가 존재하면 실행
    if "user_code" in global_namespace:
        global_namespace["user_code"]()
    else:
        raise RuntimeError("user_code() 함수가 코드 내에 정의되어 있지 않습니다.")
