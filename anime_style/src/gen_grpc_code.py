import subprocess
from grpc_tools import protoc

subprocess.check_output('cp -f ../../server/src/magic_style/rpc/anime_style/anime_style.proto ./rpc', shell=True)
protoc.main(('', '-I./', '--python_out=.', '--grpc_python_out=.', './rpc/anime_style.proto'))
