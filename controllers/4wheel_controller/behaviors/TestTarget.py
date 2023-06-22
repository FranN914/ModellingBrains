from . import AvoidObstacle, CarryTarget

# Comportamiento: Probar objetivo
# Si puede moverlo, es un objetivo, si no es un obstaculo
def probarObjetivo(robot, gps, wheels, ds, brazo, TIME_STEP):
    pos_inicial = gps.getValues()

    for i in range(10):
        robot.step(TIME_STEP)
        wheels[0].setVelocity(1.0)
        wheels[1].setVelocity(1.0)

    pos_actual = gps.getValues()
    difx = (pos_inicial[0] - pos_actual[0])
    dify = (pos_inicial[1] - pos_actual[1])
    if (difx < 0.009 and difx > -0.009) and (dify < 0.009 and dify > -0.009):
        print("no se movio")
        AvoidObstacle.evitarObstaculo(robot, wheels, ds, TIME_STEP)
        return False
    else:
        print("si se movio")
        CarryTarget.llevarObjetivo(robot, gps, wheels, brazo, ds, TIME_STEP)
        return True