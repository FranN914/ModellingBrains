from controller import Robot, Motor, GPS

robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

gps = robot.getDevice('gps')
gps.enable(100)

ds = []
dsNames = ['sensor_der', 'sensor_izq', 'sensor_altura']
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
brazo = robot.getDevice('brazo')
brazo.setPosition(float('inf'))
brazo.setVelocity(0.0)
brazoa = robot.getDevice('brazo_agarre')
brazoa.setPosition(float('inf'))
brazoa.setVelocity(0.0)
def volverOrigen():
    pos = gps.getValues()
    if (pos[0] < 0.5 and pos[0] > -0.5):
        if (pos[1] < 0.5 and pos[1] > -0.5):
            return True
        else:
            return False
    else:
        return False
            
while robot.step(TIME_STEP) != -1:
    leftSpeed = 1.0
    rightSpeed = 1.0
    brazoSpeed = 0.2
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 1.0
        rightSpeed = -1.0
        brazoSpeed = 0.2
    else:  # read sensors
        if ds[2].getValue() < 950.0:
            avoidObstacleCounter = 100
    
    #if not volverOrigen():
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    brazo.setVelocity(brazoSpeed)
    brazoa.setVelocity(brazoSpeed)
       # print(gps.getValues())
    #else:
     #   print(gps.getValues())
      #  wheels[0].setVelocity(0)
       # wheels[1].setVelocity(0)