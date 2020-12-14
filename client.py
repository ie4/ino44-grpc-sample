import grpc
import ino44_pb2
import ino44_pb2_grpc

with grpc.insecure_channel('localhost:1044') as channel:
  stub = ino44_pb2_grpc.Ino44ServiceStub(channel)
  msg = "Chototsu!!"
  print('Req: ', msg)
  response = stub.Attack(ino44_pb2.Req(msg=msg))

print('Res: ', response.msg)
