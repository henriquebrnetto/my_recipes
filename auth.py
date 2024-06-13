# auth.py
from flask import request, Response
from functools import wraps
import hashlib
from utils import decorate

def hash_password(password):
    """Gera um hash SHA-256 da senha."""
    password = decorate(password)
    return hashlib.sha256(password.encode()).hexdigest()

def check_auth(email, password, db):
    """Verifica se as credenciais de usuário e senha são válidas."""
    hashed_password = hash_password(password)
    filtro = {"email": email, "psswd": password} #COLOCAR HASHED PASSWORD
    usuario = db.users.find_one(filter=filtro)
    return bool(usuario)

def check_admin(email, password, db):
    """Verifica se as credenciais de usuário e senha são válidas."""
    hashed_password = hash_password(password)
    filtro = {"email": email, "psswd": password} #COLOCAR HASHED PASSWORD
    usuario = db.users.find_one(filter=filtro)
    if bool(usuario):
        return usuario['class'] == 'admin'
    else:
        return False


def authenticate():
    """Envia uma resposta que solicita autenticação ao usuário."""
    return Response(
        'Acesso negado. Por favor, autentique-se.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(db):
    """Decorador que protege rotas específicas com autenticação básica.
    Args:
        f (function): A função da rota Flask a ser decorada.
    Returns:
        function: A função decorada que agora inclui verificação de autenticação.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password, db):
                return authenticate()
            return f(*args, **kwargs)
        return decorated
    return decorator

def requires_admin(db):
    """Decorador que protege rotas específicas com autenticação básica.
    Args:
        f (function): A função da rota Flask a ser decorada.
    Returns:
        function: A função decorada que agora inclui verificação de autenticação.
    """

    def decorator_admin(f):
        @wraps(f)
        def decorated_admin(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_admin(auth.username, auth.password, db):
                return authenticate()
            return f(*args, **kwargs)
        return decorated_admin
    return decorator_admin