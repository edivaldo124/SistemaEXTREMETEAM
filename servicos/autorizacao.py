from functools import wraps

from flask import redirect, session


def admin_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get('tipo_usuario') != 'admin':
            return redirect('/login')
        return view(*args, **kwargs)
    return wrapper


def professor_ou_admin_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get('tipo_usuario') not in ('admin', 'professor'):
            return redirect('/login')
        return view(*args, **kwargs)
    return wrapper
