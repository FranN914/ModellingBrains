from .armcontroller import ArmState
from math import dist, acos, degrees

def debajo( p1, p2, pp):
    pendiente = (p1[1] - p2[1]) / (p1[0] - p2[0])
    ter_ind = (pendiente * -1) * p1[0] + p1[1]
    
    valor_y = pendiente * pp[0] + ter_ind
    
    if(valor_y < pp[1]):
        return False
    else:
        return True
    
def estaOrigen(gps):
    pos = gps.getValues()                       # Se obtienen los valores que otorga el gps
    if (pos[0] > -1.25 and pos[0] < -0.75):
        if (pos[1] < 0.25 and pos[1] > -0.25):
            return True
        else:
            return False
    else:
        return False

def orientarOrigen(robot, gps, wheels, TIME_STEP):
    pos1 = gps.getValues()

    for i in range (30):
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
    angulo = degrees(acos((x * x + y * z - z * z)/(2.0 * x * y)))
    cor = (180 - angulo) / 2
    abajo = debajo(a,c,b)
    izquierda = (pos2[0] < -1)

    if(abajo and izquierda):
        for i in range (int(cor)):
            robot.step(TIME_STEP)
            wheels[0].setVelocity(-1.0)
            wheels[1].setVelocity(1.0)
    elif(abajo and not izquierda):
        for i in range (int(cor)):
            robot.step(TIME_STEP)
            wheels[0].setVelocity(1.0)
            wheels[1].setVelocity(-1.0)
    elif(not abajo and izquierda):
        for i in range (int(cor)):
            robot.step(TIME_STEP)
            wheels[0].setVelocity(1.0)
            wheels[1].setVelocity(-1.0)
    else: 
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
    while(not estaOrigen(gps)):
        orientarOrigen(robot, gps, wheels, TIME_STEP)
        for i in range(30):
            robot.step(TIME_STEP)
            wheels[0].setVelocity(1.0)
            wheels[1].setVelocity(1.0)
            
    ArmState.activarBrazo(False, robot, brazo, TIME_STEP)