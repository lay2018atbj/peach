import signalsPool
from app import db, application
from models import RobotRunInfo


def signals_robot_start_callback(sender, *args, **kwargs):
    print(sender)


def signals_robot_stop_callback(sender,*args,**kwargs):
    pring(sender)


signalsPool.ROBOT_START.connect(signals_robot_start_callback)
signalsPool.ROBOT_STOP.connect(signals_robot_start_callback)



