from grpc_tools import protoc

protoc.main(('', '-I./', '--python_out=.', '--grpc_python_out=.', './rpc/style_migrate/style_migrate.proto'))
protoc.main(('', '-I./', '--python_out=.', '--grpc_python_out=.', './rpc/anime_style/anime_style.proto'))

# python rpc/gen_grpc_code.py
