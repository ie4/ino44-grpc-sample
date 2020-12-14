import grpc
import time
import ino44_pb2
import ino44_pb2_grpc
from concurrent import futures

class Ino44ServiceServicer(ino44_pb2_grpc.Ino44ServiceServicer):
    def __init__(self):
        pass

    def Attack(self, request, context):
        print('Req: ', request.msg)
        msg = 'Moushin!!'
        print('Res: ', msg)
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
