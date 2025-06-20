# /jbrbabel/blues/cli.py

from flask import Blueprint


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('foo')
def foo():
    print('This is a (foo) test!')