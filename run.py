rom todo_project import app
from flask import Flask, request, render_template
import logging

# Configurações de log
logging.basicConfig(filename='app_errors.log', level=logging.ERROR)

@app.after_request
def set_security_headers(response):
    # Remover cabeçalho "Server"
    if 'Server' in response.headers:
        del response.headers['Server']
        
    # Definindo o cabeçalho CSP
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self';"
    )
    
    # Política de Permissões
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # Configuração de Cookies
    response.set_cookie('session', value='value', secure=True, httponly=True, samesite='Strict')
    
    return response

# Manipuladores de erro (403, 404, 500)
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal Server Error: {error}')
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)