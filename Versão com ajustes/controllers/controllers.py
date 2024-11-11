from flask import Blueprint, render_template, request, session, redirect, url_for, make_response, flash, abort
from datetime import datetime

blueprint_default = Blueprint("blueprint", __name__)

# Página inicial
@blueprint_default.route("/")
def index():
    return redirect(url_for('blueprint.index'))

#login do usuario
@blueprint_default.route("/login", methods=["GET", "POST"])
def login():
    if 'usuario' not in session:
        if request.method == "POST":
            usuario = request.form["usuario"]
            session['usuario'] = usuario  # Armazena o login na sessão
            return redirect(url_for('blueprint.musicas'))
        return render_template("login.html")
    else:
        return redirect(url_for('blueprint.musicas'))


# Página inicial com a lista de musicas/playlists
@blueprint_default.route('/musicas')
def musicas():
    musicas = session.get('musicas', [])  # Recupera musicas da sessão
    total_musicas = request.cookies.get('total_musicas', 0)  # Conta musicas do cookie
    return render_template("musica.html", musicas=musicas, total_musicas=total_musicas)

# Adicionar musica
@blueprint_default.route('/adicionar_musica', methods=['POST'])
def adicionar_musica():
    nome = request.form.get('nome')
    cantor = request.form.get('cantor')
    ano_lançamento= request.form.get('ano_lancamento')

    if not nome:
        flash('////O Nome da Música, deve estar  estar preecnhido para o cadastro da música.', 'danger')
        if not ano_lançamento:
            flash('////O Ano de lançamento, deve estar preecnhido para o cadastro da música.', 'danger')
        if not cantor:
            flash('////O nome do cantor, deve estar  estar preecnhido para o cadastro da música.', 'danger')
        return redirect(url_for('blueprint.musicas'))
    
    elif not ano_lançamento:
        flash('////O Ano de lançamento, deve estar preecnhido para o cadastro da musica.', 'danger')
        if not cantor:
            flash('////O Nome do cantor, deve estar  estar preecnhido para o cadastro da musica.', 'danger')
        if not nome:
            flash('////O Nome da musica, deve estar  estar preecnhido para o cadastro da musica.', 'danger')
        return redirect(url_for('blueprint.musicas'))
    
    elif not cantor:
        flash('////O Nome do cantor, deve estar  estar preecnhido para o cadastro da musica.', 'danger')
        if not nome:
            flash('////O Nome da Musica, deve estar  estar preecnhido para o cadastro da musica.', 'danger')
        if not ano_lançamento:
            flash('////O Ano de lançamento, deve estar preecnhido para o cadastro da musica.', 'danger')
        return redirect(url_for('blueprint.musicas'))

    
    
    musica = {
        "nome": nome,
        "cantor": cantor,
        "ano_lancamento": ano_lançamento or datetime.now().strftime("%d-%Y-%m")

    }
    
    musicas = session.get('musicas', [])
    musicas.append(musica)
    session['musicas'] = musicas  # Salva na sessão

    # Incrementa o total de musicas no cookie
    
    total_musicas = int(request.cookies.get('total_musicas', 0)) +1
    
    resp = make_response(redirect(url_for('blueprint.musicas')))
    resp.set_cookie('total_musicas', str(total_musicas), max_age=60*60) 
    flash('////Musica adicionada com sucesso!', 'success')
    
    return resp

# Logout
@blueprint_default.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('musicas', None)
    print("Saiu")
    flash('////Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('blueprint.login'))

@blueprint_default.route('/limpar')
def limpar():
    resp = make_response(redirect(url_for('blueprint.musicas')))
    resp.set_cookie('total_musicas', '', expires=0)  # Remove o cookie 
    session.pop('musicas', None)
    flash('////Catalogo limpo com sucesso!', 'success')
    return resp