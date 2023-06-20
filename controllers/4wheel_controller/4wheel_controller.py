from controller import Robot, Motor, GPS
from behaviors import AvoidObstacle, TestTarget, OrientBody

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
dsNames = ['sensor_izq', 'sensor_der', 'sensor_altura']

# Se obtienen los sensores del robot
for i in range(3):
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

### Fin de la declaracion de variables ###


''' Este metodo podria borrarse porque no se utiliza nunca
def ubicacionZona():
    pos = gps.getValues()                       # Se obtienen los valores que otorga el gps
    if (pos[0] > -1.25 and pos[0] < -0.75):
        if (pos[1] < 0.25 and pos[1] > -0.25):
            return True
        else:
            return False
    else:
        return False
'''

# Bucle principal
while robot.step(TIME_STEP) != -1:
    # Comportamiento: Deambular
    leftSpeed = 1.0
    rightSpeed = 1.0
    
    valor_izq = ds[0].getValue()
    valor_der = ds[1].getValue()

    # Sensor de altura detecta algo
    if ds[2].getValue() < 950.0:
        # Llamada a método que evita obstaculos
        AvoidObstacle.evitarObstaculo(robot, wheels, ds, TIME_STEP)
    # Sensores de distancia detectan objetivo
    elif (valor_izq < 20) and (valor_der < 20):
        TestTarget.probarObjetivo(robot, gps, wheels, ds, brazo, TIME_STEP)
    elif (valor_izq - valor_der) < 100 and (valor_izq - valor_der) > -100:
        pass
    # Sensores de distancia detectan algo
    elif valor_izq < 950.0 or valor_der < 950.0:
        OrientBody.orientarCuerpo(robot, wheels, ds, TIME_STEP)

    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)