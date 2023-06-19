from controller import Robot, Motor, GPS
from math import dist, acos, degrees
robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

gps = robot.getDevice('gps')
gps.enable(50)


ds = []
dsNames = ['sensor_izq', 'sensor_der', 'sensor_altura']


for i in range(3):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['wheel1', 'wheel2']


for i in range(2):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)


avoidObstacleCounter = 0

brazo = []
brazoNames = ['brazo', 'brazo_agarre']
for i in range(2):
    brazo.append(robot.getDevice(brazoNames[i]))
    brazo[i].setPosition(float('inf'))
    brazo[i].setVelocity(0.0)
    


def ubicacionZona():
    pos = gps.getValues()
    if (pos[0] > -1.25 and pos[0] < -0.75):
        if (pos[1] < 0.25 and pos[1] > -0.25):
            return True
        else:
            return False
    else:
        return False

def gg():
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
    
def activarBrazo(brazoEstirado):
    if(brazoEstirado):
        armSpeed = -1.0
        for i in range(50):
            robot.step(TIME_STEP)
            brazo[0].setVelocity(armSpeed)
            
        brazo[0].setVelocity(0)
        
        for i in range(40):
            robot.step(TIME_STEP)
            brazo[1].setVelocity(armSpeed)
            
        brazo[1].setVelocity(0)
    else:
        armSpeed = 1.0
        for i in range(40):
            robot.step(TIME_STEP)
            brazo[1].setVelocity(armSpeed)
            
        brazo[1].setVelocity(0)
        
        for i in range(50):
            robot.step(TIME_STEP)
            brazo[0].setVelocity(armSpeed)
            
        brazo[0].setVelocity(0)
    
# Comportamiento: Llevar objetivo
def llevarObjetivo():
    #Primer paso: retroceder un poco
    leftSpeed = -1.0
    rightSpeed = -1.0
    
    for i in range (30):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)
    
    #Segundo paso: girar 180 grados
    leftSpeed = 1.0
    for i in range (170):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)
    
    #Tercer paso: retroceder un poco
    leftSpeed = -1.0
    for i in range (30):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)
    
    #Cuarto Paso: Frenar
    wheels[0].setVelocity(0)
    wheels[1].setVelocity(0)
    #Quinto paso: agarrar el objetivo
    activarBrazo(True)
    gg()
        
# Comportamiento: Evitar obstaculos
def avoidObstacle():
    # Detecta a que lado es conveniente rotar
    if ds[0].getValue() > ds[1].getValue():     # Si hay algo a la derecha
        leftSpeed   = -1.0                      # Rota a izquierda
        rightSpeed  = 1.0
    else:                                       # Si hay algo a la izquierda
        leftSpeed   = 1.0                       # Rota a derecha
        rightSpeed  = -1.0

    # Esquiva el obstaculo
    for i in range (100):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(leftSpeed)
        wheels[1].setVelocity(rightSpeed)

def orientar():
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

def probarObjetivo():
    pos_inicial = gps.getValues()
    
    for i in range (10):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(1.0)
        wheels[1].setVelocity(1.0)
    
    pos_actual = gps.getValues()
    dif = (pos_inicial[0] - pos_actual[0])
    if dif < 0.01 and dif > -0.01:
        print("no se movio")
        avoidObstacle()
    else:
        print("si se movio")
        llevarObjetivo()
brazoEstirado = True
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
        avoidObstacle()
    # Sensores de distancia detectan objetivo
    elif (valor_izq < 20) and (valor_der < 20):
        probarObjetivo()
    elif (valor_izq - valor_der) < 100 and (valor_izq - valor_der) > -100:
        pass
    #Sensores de distancia detectan algo
    elif valor_izq < 950.0 or valor_der < 950.0:
        orientar()
    

    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)


