# agent/ImageAgent.py
import os
import cv2
import base64
import time
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


class ImageAgent:
    def __init__(self, model="gpt-4o"):
        load_dotenv()

        self.llm = ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0,
        )

        # 카메라 연결
        print("📸 카메라 연결 시도 중...")
        self.cap = cv2.VideoCapture(0)
        retry = 0
        while not self.cap.isOpened():
            retry += 1
            print(f"⏳ 카메라 준비 중... 재시도 {retry}")
            time.sleep(1)
            self.cap = cv2.VideoCapture(0)

        print("✅ 카메라 연결 완료!")

    def capture_image(self):
        print("🖼 이미지 캡처 중...")
        for _ in range(10):
            ret, frame = self.cap.read()
            if ret:
                print("✅ 이미지 캡처 성공!")
                return frame
            print("⚠️ 실패. 재시도...")
            time.sleep(0.5)
        raise RuntimeError("❌ 이미지 캡처에 실패했습니다.")

    def image_to_base64(self, image):
        _, buffer = cv2.imencode(".jpg", image)
        return base64.b64encode(buffer).decode("utf-8")

    def classify(self) -> str:
        image = self.capture_image()
        image_b64 = self.image_to_base64(image)

        messages = [
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                    {
                        "type": "text",
                        "text": "이 이미지에 있는 M&M's의 색깔을 한 단어로만 대답해줘. (예: red, green, yellow, blue).white나 black, gray 같은 색은 없어. 그림자의 영향이 있을 수 있음을 감안해줘. 그리고 오로지 한 단어로만 답변해줘. 단어 말고 다른 문장 문장부호는 넣지마. 최대한 색을 구분하되, 아무것도 없다면 unknown을 출력해줘.",
                    },
                ]
            )
        ]

        print("🧠 GPT-4o에게 분류 요청 중...")
        response = self.llm.invoke(messages)
        color = response.content.strip().lower()

        # 색상 리스트 검증 (예: red, green, yellow, blue)
        valid_colors = ["red", "green", "yellow", "blue", "orange", "brown"]
        if color in valid_colors:
            return color
        else:
            print(f"❌ 유효하지 않은 색상: {color}")
            return "unknown"

    def release_camera(self):
        if self.cap.isOpened():
            self.cap.release()
            print("📷 카메라 연결 종료됨.")
