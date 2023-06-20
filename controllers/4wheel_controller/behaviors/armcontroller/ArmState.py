# Metodo que controla el movimiento del brazo robotico para tomar un objetivo o volverlo a su posicion original
def activarBrazo(brazoEstirado, robot, brazo, TIME_STEP):
    if (brazoEstirado):
        armSpeed = -1.0

        # Baja el brazo hacia el objetivo
        for i in range(50):
            robot.step(TIME_STEP)
            brazo[0].setVelocity(armSpeed)

        brazo[0].setVelocity(0)

        # Toma el objetivo con la parte superior del brazo
        for i in range(40):
            robot.step(TIME_STEP)
            brazo[1].setVelocity(armSpeed)

        brazo[1].setVelocity(0)
    else:
        armSpeed = 1.0

        # Vuelve a estirar el brazo
        for i in range(40):
            robot.step(TIME_STEP)
            brazo[1].setVelocity(armSpeed)

        brazo[1].setVelocity(0)

        # Vuelve a posicionarlo sobre su cabeza
        for i in range(50):
            robot.step(TIME_STEP)
            brazo[0].setVelocity(armSpeed)

        brazo[0].setVelocity(0)