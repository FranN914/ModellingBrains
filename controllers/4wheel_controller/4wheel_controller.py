from controller import Robot, Motor, GPS
from behaviors import AvoidObstacle, TestTarget, OrientBody, CarryTarget

### Comienzo de la declaracion de variables ###

# Obtencion de instancia del robot
robot = Robot()

 # Obtencion del time step (tiempo virtual)
TIME_STEP = int(robot.getBasicTimeStep())

# Obtencion del gps
gps = robot.getDevice('gps')
gps.enable(50)

# Declaracion del estado del brazo robotico
brazoEstirado = True
# Declaracion del contador de obstaculos evitados, usado en el entrenamiento
avoidObstacleCounter = 0

# Lista de sensores del robot
ds = []
dsNames = ['sensor_izq', 'sensor_der', 'sensor_color', 'sensor_distancia']

# Se obtienen los sensores del robot
for i in range(4):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)

# Lista de ruedas del robot
wheels = []
wheelsNames = ['wheel1', 'wheel2']

# Se obtienen las ruedas del robot
for i in range(2):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

# Lista de brazos del robot
brazo = []
brazoNames = ['brazo', 'brazo_agarre']

# Se obtienen los brazos del robot
for i in range(2):
    brazo.append(robot.getDevice(brazoNames[i]))
    brazo[i].setPosition(float('inf'))
    brazo[i].setVelocity(0.0)

# Se obtiene el sensor de contacto
sc = robot.getDevice("touch sensor")
sc.enable(50)

colores = []
distancia_color = []
puntaje_color = []
def procesarColor(distancia, color):
    #guarda el valor del color
    encontrado = False
    iterador = 0
    print("Distancia del color: " + str(distancia))
    print("Lista de dist: " + str(distancia_color))
    for d in distancia_color:
        if (d < (distancia + 50)) and (d > (distancia - 60)):
            color_guardado = colores[iterador]
            encontrado = True
            break
        else:
            iterador = iterador + 1
        
    if(not encontrado):
        print("Color no encontrado en la lista")
        distancia_color.append(int(distancia))
        colores.append(int(color))
        puntaje_color.append(0)
        color_guardado = int(color)
        iterador = len(colores) - 1
    print("Indice: " + str(iterador))
    print("Puntajes actuales: "+str(puntaje_color))
    puntaje = puntaje_color[iterador]
    if(puntaje < -2):
        AvoidObstacle.evitarObstaculo(robot, wheels, ds, TIME_STEP)
    elif(puntaje > 2):
        while(sc.getValue() < 1):
            robot.step(TIME_STEP)
            OrientBody.orientarCuerpo(robot, wheels, ds, TIME_STEP)
            wheels[0].setVelocity(1.0)
            wheels[1].setVelocity(1.0)
        CarryTarget.llevarObjetivo(robot, gps, wheels, brazo, ds, TIME_STEP)
    else:
        while(sc.getValue() < 1):
            robot.step(TIME_STEP)
            OrientBody.orientarCuerpo(robot, wheels, ds, TIME_STEP)
            wheels[0].setVelocity(1.0)
            wheels[1].setVelocity(1.0)
        if(TestTarget.probarObjetivo(robot, gps, wheels, ds, brazo, TIME_STEP)):
            puntaje_color[iterador] = puntaje_color[iterador] + 1
        else:
            puntaje_color[iterador] = puntaje_color[iterador] - 1
    
# Bucle principal
while robot.step(TIME_STEP) != -1:
    # Comportamiento: Deambular
    leftSpeed = 1.0
    rightSpeed = 1.0
    
    valor_izq = ds[0].getValue()
    valor_der = ds[1].getValue()
    v = ds[2].getValue()
    g = ds[3].getValue()
    if CarryTarget.estaOrigen(gps):
        if valor_izq < 950.0 or valor_der < 950.0:
            AvoidObstacle.evitarObstaculosVarios(robot, wheels, ds, TIME_STEP)
    elif g < 1000.0:
        if (v < 1000.0):
            if (v > 900.0):
                procesarColor(g,v)
            else:
                leftSpeed = -1.0
                rightSpeed = -1.0
    elif valor_izq < 950.0 or valor_der < 950.0:
        OrientBody.orientarCuerpo(robot, wheels, ds, TIME_STEP)

    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)