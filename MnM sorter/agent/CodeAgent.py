# agent/CodeAgent.py

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json


class CodeAgent:
    def __init__(self, model_name="gpt-4o", temperature=0):
        load_dotenv()

        # 프롬프트 템플릿 설정
        self.prompt_template = PromptTemplate(
            input_variables=["user_prompt"],
            template="""
아래 자연어 명령을 Python 코드로 변환하여 **JSON 문자열로만 출력하세요**.

❗ 반드시 아래 조건을 지키세요:
- 출력은 오직 JSON 형식만 허용됩니다. 
- 절대 ```json 이나 ``` 등의 마크다운 기호를 사용하지 마세요.
- "code" 필드 안에만 파이썬 코드를 포함하세요.
- 코드 외의 설명, 인사말, 여는 말 없이 JSON 하나만 출력하세요.

사용 가능한 함수:
- get_color(): 현재 물체 색상을 반환 (예: "yellow", "green", "unknown")
- printp(value): 값을 출력
- move(direction): "left" 또는 "right" 방향으로 이동

출력 형식 예시:
{{
  "code": "def user_code():\\n    if get_color() == 'green':\\n        move('right')"
}}

명령어:
"{user_prompt}"
""",
        )

        # 최신 방식 Chat LLM 로드
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Runnable 체인 구성
        self.chain = self.prompt_template | self.llm

    def generate_code(self, user_prompt: str) -> dict:
        result = self.chain.invoke({"user_prompt": user_prompt})

        # 응답은 문자열이므로 JSON 파싱
        try:
            return json.loads(result.content.strip())
        except json.JSONDecodeError:
            raise ValueError(f"CodeAgent 응답 JSON 파싱 실패: {result.content}")
