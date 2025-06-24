// 패키지 다운로드 필수
// https://github.com/DFRobot/pxt-motor

serial.redirectToUSB()
motor.servo(motor.Servos.S1, 90)

serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let command = serial.readUntil(serial.delimiters(Delimiters.NewLine)).trim()
    serial.writeLine("Received: " + command)
    moveAction(command)
})

function moveAction(direction:string) {
    if (direction == "left") {
        motor.servo(motor.Servos.S1, 0)
        basic.pause(700)
        motor.servo(motor.Servos.S1, 90)
    } else if (direction == "right") {
        motor.servo(motor.Servos.S1, 180)
        basic.pause(700)
        motor.servo(motor.Servos.S1, 90)
    } else if (direction == "center") {
        motor.servo(motor.Servos.S1, 90)
    } else {
        serial.writeLine("Unknown command: " + direction)
    }
}
