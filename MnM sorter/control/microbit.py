import serial
import serial.tools.list_ports
import os
import time

def send_to_microbit(direction: str):
    """
    방향 ('left' 또는 'right')을 micro:bit로 전송합니다.
    """
    if direction not in ("left", "right"):
        raise ValueError("direction은 'left' 또는 'right'만 가능합니다.")

    try:
        # 시리얼 포트 연결
        SERIAL_PORT = os.getenv("MICROBIT_PORT")
        BAUD_RATE = 115200
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            # 명령어에 줄 바꿈 문자를 추가하여 전송
            ser.write((direction + "\n").encode())
            print(f"✅ micro:bit에 명령 전송: {direction}")

            # 마이크로비트로부터 응답 수신 (선택 사항)
            response = ser.readline().decode(errors="ignore").strip()
            if response:
                print(f"micro:bit 응답: {response}")

            time.sleep(0.5)  # 약간의 대기 시간
    except serial.SerialException as e:
        print(f"❌ micro:bit 연결 실패: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
