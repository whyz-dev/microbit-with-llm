# agent/ImageAgent.py
import os
import cv2
import base64
import time
import subprocess
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

        self.capture_path = "captured.jpg"

    def capture_image(self):
        """
        imagesnap을 이용해 macOS 시스템 카메라에서 이미지 캡처
        """
        print("📸 imagesnap으로 이미지 캡처 중...")
        subprocess.run(["imagesnap", "-w", "2", self.capture_path])
        print(f"✅ 이미지 저장됨: {self.capture_path}")
        image = cv2.imread(self.capture_path)
        if image is None:
            raise RuntimeError("❌ 이미지 로딩 실패 (imagesnap 결과 확인 필요)")
        return image

    def image_to_base64(self, image):
        # 원본 이미지 저장 (디버깅용)
        cv2.imwrite("original.jpg", image)

        # 원본 그대로 인코딩
        _, buffer = cv2.imencode(".jpg", image)
        return base64.b64encode(buffer).decode("utf-8")

    def classify(self) -> str:
        # image = self.capture_image()
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
        print(response)

        valid_colors = ["red", "green", "yellow", "blue", "orange", "brown"]
        if color in valid_colors:
            return color
        else:
            print(f"❌ 유효하지 않은 색상: {color}")
            return "unknown"

    def release_camera(self):
        pass  # imagesnap은 카메라 점유가 없기 때문에 무시
