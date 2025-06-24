# main.py

from agent.CodeAgent import CodeAgent
from control.runner import execute_code


def main():
    code_agent = CodeAgent()

    while True:
        try:
            # 1. 사용자 명령 입력
            user_input = input("🗣 명령을 입력하세요 (종료하려면 'exit'): ")
            if user_input.lower() in ("exit", "quit"):
                break

            # 2. LLM에게 코드 생성 요청
            response = code_agent.generate_code(user_input)
            code = response.get("code")

            print("\n📦 생성된 코드:")
            print(code)

            # 3. 코드 실행
            print("\n🚀 코드 실행 중...")
            execute_code(code)

        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()
