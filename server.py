import RPi.GPIO as GPIO
import grpc
import time
import ino44_pb2
import ino44_pb2_grpc
from concurrent import futures

IN1Rear = 16 #GPIO23 to IN1 Rear-right wheel direction
IN2Rear = 18 #GPIO24 to IN2 Rear-right wheel direction

IN3Rear = 13 #GPIO27 to IN3 Rear-left wheel direction
IN4Rear = 15 #GPIO22 to IN4 Rear-left wheel direction

IN1Front = 40 #GPIO21 to IN1 Front Model X right wheel direction
IN2Front = 38 #GPIO20 to IN2 Front Model X right wheel direction

IN3Front = 36 #GPIO16 to IN3 Front Model X left wheel direction
IN4Front = 32 #GPIO12 to IN4 Front Model X left wheel direction

GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1Rear, GPIO.OUT)
GPIO.setup(IN2Rear, GPIO.OUT)
GPIO.setup(IN3Rear, GPIO.OUT)
GPIO.setup(IN4Rear, GPIO.OUT)
GPIO.setup(IN1Front, GPIO.OUT)
GPIO.setup(IN2Front, GPIO.OUT)
GPIO.setup(IN3Front, GPIO.OUT)
GPIO.setup(IN4Front, GPIO.OUT)

def rr_ahead():
    GPIO.output(IN1Rear,True)
    GPIO.output(IN2Rear,False)

def rl_ahead():
    GPIO.output(IN3Rear,True)
    GPIO.output(IN4Rear,False)

def rr_back():
    GPIO.output(IN2Rear,True)
    GPIO.output(IN1Rear,False)

def rl_back():
    GPIO.output(IN4Rear,True)
    GPIO.output(IN3Rear,False)

def fr_ahead():
    GPIO.output(IN1Front,True)
    GPIO.output(IN2Front,False)

def fl_ahead():
    GPIO.output(IN3Front,True)
    GPIO.output(IN4Front,False)

def fr_back():
    GPIO.output(IN2Front,True)
    GPIO.output(IN1Front,False)

def fl_back():
    GPIO.output(IN4Front,True)
    GPIO.output(IN3Front,False)


def go_ahead():
    rl_ahead()
    rr_ahead()
    fl_ahead()
    fr_ahead()

def go_back():
    rr_back()
    rl_back()
    fr_back()
    fl_back()

def turn_right():
    rl_ahead()
    rr_back()
    fl_ahead()
    fr_back()

def turn_left():
    rr_ahead()
    rl_back()
    fr_ahead()
    fl_back()

def shift_left():
    fr_ahead()
    rr_back()
    rl_ahead()
    fl_back()

def shift_right():
    fr_back()
    rr_ahead()
    rl_back()
    fl_ahead()

def upper_right():
    rr_ahead()
    fl_ahead()

def lower_left():
    rr_back()
    fl_back()

def upper_left():
    fr_ahead()
    rl_ahead()

def lower_right():
    fr_back()
    rl_back()

def stop_car():
    GPIO.output(IN1Rear,False)
    GPIO.output(IN2Rear,False)
    GPIO.output(IN3Rear,False)
    GPIO.output(IN4Rear,False)
    GPIO.output(IN1Front,False)
    GPIO.output(IN2Front,False)
    GPIO.output(IN3Front,False)
    GPIO.output(IN4Front,False)

def kurui_zaki():
    go_ahead()
    time.sleep(1)
    stop_car()
    go_back()
    time.sleep(1)
    stop_car()
    turn_left()
    time.sleep(1)
    stop_car()
    turn_right()
    time.sleep(1)
    stop_car()
    shift_right()
    time.sleep(1)
    stop_car()
    shift_left()
    time.sleep(1)
    stop_car()
    upper_left()
    time.sleep(1)
    stop_car()
    lower_right()
    time.sleep(1)
    stop_car()
    upper_right()
    time.sleep(1)
    stop_car()
    lower_left()
    time.sleep(1)
    stop_car()
    #GPIO.cleanup()

class Ino44ServiceServicer(ino44_pb2_grpc.Ino44ServiceServicer):
    def __init__(self):
        pass

    def Attack(self, request, context):
        print('Req: ', request.msg)
        msg = 'Moushin!!'
        print('Res: ', msg)
        kurui_zaki()
        return ino44_pb2.Res(
            msg = msg
        )

# start server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ino44_pb2_grpc.add_Ino44ServiceServicer_to_server(Ino44ServiceServicer(), server)
server.add_insecure_port('[::]:1044')
server.start()
print('run server')
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    server.stop(0)
