import click
from pprint import pprint
from .parser import parse as parse_src
from .runtime import eval, env
from . import __version__ as version


@click.command()
@click.argument('file', type=click.File(), required=False)
@click.option('--parse', '-p', is_flag=True, help='Realiza análise sintática sem executar código.')
def main(file, parse):
    if file is None:
        e = env()
        while True:
            src = input('lispy> ')
            if not src and input('sair? [y/n]').lower() == 'y':
                break
            ast = parse_src(src)
            try:
                print(eval(ast, e))
            except Exception as exc:
                print(exc.__class__.__name__, exc)
    else:
        ast = parse_src(file.read())
        if parse:
            pprint(ast)
        value = eval(ast, env())
        if value is not None:
            print(value)


if __name__ == '__main__':
    main()