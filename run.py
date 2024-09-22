from todo_project import app
from flask import Flask, request

# Função para adicionar cabeçalhos de segurança
@app.after_request
def set_security_headers(response):
    # Política CSP ajustada para ser mais restritiva
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://trusted-source.com; "
        "style-src 'self' https://trusted-source.com; "
        "img-src 'self' https://trusted-image-source.com; "
        "frame-ancestors 'none'; "
        "form-action 'self';"
    )
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Permissions-Policy'] = 'geolocation=(self)'
    return response

if __name__ == '__main__':
    # Rodar o app sem o modo de depuração
    app.run(host='0.0.0.0', port=5000)  # Mude o host e a porta conforme necessário