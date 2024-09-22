from todo_project import app
from flask import Flask, request, render_template

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

# Manipulador de erro 403
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

# Manipulador de erro 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Manipulador de erro 500
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Rodar o app sem o modo de depuração
    app.run(host='0.0.0.0', port=5000)  # Mude o host e a porta conforme necessário