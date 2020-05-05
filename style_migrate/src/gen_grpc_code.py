import subprocess
from grpc_tools import protoc

subprocess.check_output('cp -f ../../server/src/magic_style/rpc/style_migrate/style_migrate.proto ./rpc', shell=True)
protoc.main(('', '-I./', '--python_out=.', '--grpc_python_out=.', './rpc/style_migrate.proto'))
