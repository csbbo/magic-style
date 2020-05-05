from grpc_tools import protoc

protoc.main(('', '-I./', '--python_out=.', '--grpc_python_out=.', './style_migrate/style_migrate.proto'))
protoc.main(('', '-I./', '--python_out=.', '--grpc_python_out=.', './anime_style/anime_style.proto'))
