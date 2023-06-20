# Comportamiento: Orientar el cuerpo
def orientarCuerpo(robot, wheels, ds, TIME_STEP):
    # Detecta a que lado es conveniente rotar
    if ds[0].getValue() > ds[1].getValue():     # Si hay algo a la derecha
        leftSpeed   = 1.0                       # Rota a derecha
        rightSpeed  = 0
    else:                                       # Si hay algo a la izquierda
        leftSpeed   = 0                         # Rota a izquierda
        rightSpeed  = 1.0

    # Perfila para quedar de frente
    for i in range (5):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)