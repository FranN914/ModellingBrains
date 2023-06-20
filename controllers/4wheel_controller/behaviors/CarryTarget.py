from .armcontroller import ArmState
from math import dist, acos, degrees

def gg(robot, gps, wheels, TIME_STEP):
    pos1 = gps.getValues()

    for i in range (15):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(1.0)
        wheels[1].setVelocity(1.0)

    pos2 = gps.getValues()
    a = (pos1[0],pos1[1])
    b = (pos2[0],pos2[1])
    c = (-1, 0)
    x = dist(a,b)
    y = dist(b,c)
    z = dist(c,a)
    print(x)
    print(y)
    print(z)
    angulo = degrees(acos((x * x + y * z - z * z)/(2.0 * x * y)))
    print(angulo)
    cor = 180 - angulo
    for i in range (int(cor)):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(-1.0)
        wheels[1].setVelocity(1.0)

# Comportamiento: Llevar objetivo
def llevarObjetivo(robot, gps, wheels, brazo, TIME_STEP):
    # Primer paso: retroceder un poco
    leftSpeed = -1.0
    rightSpeed = -1.0

    for i in range(30):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)

    # Segundo paso: girar 180 grados
    leftSpeed = 1.0
    for i in range(170):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)

    # Tercer paso: retroceder un poco
    leftSpeed = -1.0
    for i in range(30):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)

    # Cuarto Paso: Frenar
    wheels[0].setVelocity(0)
    wheels[1].setVelocity(0)

    # Quinto paso: agarrar el objetivo
    ArmState.activarBrazo(True, robot, brazo, TIME_STEP)  # Toma el objetivo con el brazo
    gg(robot, gps, wheels, TIME_STEP)