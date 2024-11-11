from flask import Flask, render_template,flash, session, request, abort, make_response, redirect, url_for, flash
from controllers.controllers import blueprint_default as pagina

app = Flask(__name__)
app.secret_key = 'music'  # Defina uma chave secreta para a sessão

# Configurações de segurança para cookies de sessão
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protege contra XSS
app.config['SESSION_COOKIE_SECURE'] = True  # Só envia o cookie via HTTPS

rotas_publicas=['static','blueprint_index','blueprint_login', 'blueprint.index']
rotas_privadas=['static','blueprint_musicas', 'blueprint_logout', 'blueprint_limpar', 'blueprint_adicionar_musica']
#Evita que pessoas sem um usuario acesse a pagina de musicas
@app.before_request
def verificaSessao():
    
    if request.endpoint not in rotas_privadas and request.endpoint not in rotas_publicas:
        abort(404)
    if request.endpoint in rotas_publicas:
        return
    
    elif "usuario" not in session:
        print("Bloqueado")
        abort(403)

    return

app.register_blueprint(pagina)


@app.route('/login', methods=['GET', 'POST']) #sessao
def usuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == 'admin' and senha == '12345':
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario ou senha incorretos!')
            return redirect(url_for('usuario'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return f'Bem-vindo, {session["usuario"]}!'
    return redirect(url_for('usuario'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('usuario'))

class MeuMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print("Antes da Requisição")
        response = self.app(environ, start_response)
        print("Após a Requisição")
        return response
    

app.wsgi_app = MeuMiddleware(app.wsgi_app)


@app.route('/')
def home():
    nome = "musicas"
    return render_template('index.html', nome=nome)




#leva para uma pagina de erro caso alguem digite errado a url
@app.errorhandler(404)
def page_not_found(e):
    flash('A url da pagina parece estar incorreta, tente voltar para a pagina de login','warning')
    return render_template('404.html'), 404

#leva para uma pagina de erro caso alguem não tenha uma sessão de usuario
@app.errorhandler(403)
def acesso_negado(e):
    flash('Voce parece não estar logado tente voltar para a pagina de login','warning')
    return render_template('403.html'), 403


# Manipulador de erros genéricos
@app.errorhandler(Exception)
def handle_generic_error(e):
    return render_template('erro.html', message=str(e)), 500

@app.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie foi configurado!")
    resp.set_cookie('username', 'music?')
    return resp

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f'Cookie encontrado: {username}'
    return 'Nenhum cookie encontrado.'


if __name__ == "__main__":
    app.run(debug=True)
