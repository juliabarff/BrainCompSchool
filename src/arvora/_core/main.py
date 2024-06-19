#! /usr/bin/env python
# -*- coding: UTF8 -*-
""" Ponto de entrada do módulo Arvora.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Classes neste módulo:
    - :py:class:`SimplePage` A page used as a base for the others.
    - :py:class:`LandingPage` Entry point for the platform.
    - :py:class:`LoginPage` User Registration page.
    - :py:class:`Arvora` Main class with the main functionality.
    - :py:func:`main` Called entry page to start the application.

Changelog
---------
.. versionadded::    24.03
   |br| first version of main (05)

|   **Open Source Notification:** This file is part of open source program **Arvora**
|   **Copyright © 2023  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <http://is.gd/3Udt>`_.
|   `Labase <http://labase.selfip.org/>`_ - `NCE <http://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.

"""
# Então, basicamente ele está transformando essa string com esses nomes em duas listas de substrings e juntando elas com o zip, e depois, transformando elas em uma tupla dos elementos dessa junção das sublistas. Aqui tem as partes do menu. Uma tupla é uma sequência imutável de valores. A função zip combina duas listas, combina o primeiro elemento da lista 1 com o primeiro elememto da lista 2. A função slip faz com que a string se transforme em uma lista de substrings.
MENU_OPTIONS = tuple(zip("PROJETO CONHECIMENTO PESQUISA PERGUNTAS LOGIN USER RASCUNHO ESCREVER ARTIGO".split(),
                         "bars-progress book book-medical question right-to-bracket user".split()))
import browser.ajax as ajax
import json
# Aqui uma base de página é criado.
class SimplePage:
    # Essa classe tem um dicionário de páginas
    PAGES = dict()

    # Aqui está declarando os atributos da classe
    def __init__(self, brython, menu=MENU_OPTIONS, hero="none_hero"):
        # os [] mostram um código condensado. Basicamente é:
        # _menu = []
        # for items, icons in menu:
        #     _menu.append({"title": items, "icon": icons})
        _menu = [{"title": items, "icon": icons} for items, icons in menu]
        self.brython = brython
        self.hero_class = hero
        self.items = []
        # aqui é a página recebando o menu (não achei informações sobre .navigator)
        self.page = self.hero(self.navigator(_menu))
        # aqui é outro código condensado. Ele é:
        # for item in self.items:
        #     item.bind("click", self.link)
        [item.bind("click", self.link) for item in self.items]

    # essa função pega o id do algo que foi clicado e mostra a página que contém esse id e está dentro do dic PAGES.
    def link(self, ev=None):
        # o ev.target.id pega o id da coisa que você clicou. O strip tira todos os tracinhos do id
        ev.preventDefault()
        page = ev.target.id.strip("-")
        self.PAGES[page].show()

    #Essa função definitivamente faz a página aparecer na tela. Ela é utilizada na funcção anterior.
    def show(self):
        # Primeiro ela limpa o HTML
        self.brython.document["pydiv"].html = ""
        # Depois bota a página como filho da div pydiv
        _ = self.brython.document["pydiv"] <= self.page
        #Essa linha eu não sei o que faz
        self.brython.document["_USER_-"].html = Arvora.ARVORA.current_user

    #Não sei o que faz
    def build_body(self):
        return ()

    # Essa função cria o arcabolso da página, com as divs e aplica o bulma nelas
    def hero(self, navigator):
        h = self.brython.html
        cnt = h.DIV(self.build_body(), Class="container has-text-centered pb-6 mgb-large")
        hby = h.DIV(cnt, Class="hero-body is-justify-content-center is-align-items-center")
        hea = h.DIV(navigator, Class="hero-head")
        sec = h.SECTION((hea, hby), Class=f"hero {self.hero_class} is-fullheight")
        return sec

    # Essa função constrói a barra de pesquisa
    def navigator(self, menu):
        h = self.brython.html

        def do_item(title=None, icon=None):
            spn = h.SPAN(
                h.I(Class=f"fa fa-lg fa-{icon}", Id=f"-_{title}_-") + h.SPAN(title, Id=f"_{title}_-"),
                Class="icon-text", style="color: #333;", Id=f"-_{title}_--")
            return h.A(spn, Id=f"_{title}_", Class="navbar-item", href="./#")

        aim = h.IMG(src="/src/arvora/_media/arvora_logo.png", alt="Arvora", height="28", Id="_MAIN_-")
        arv = h.A(aim, Id="_MAIN_", Class="navbar-item", href="./")
        nbr = h.DIV(arv, Class="navbar-brand", Id="-_MAIN_-")
        self.items = [do_item(**item) for item in menu]
        end = h.DIV(self.items[-1], Class="navbar-end")
        self.items = items = [nbr] + self.items[:-1] + [end]
        nav = h.NAV(items, Class="navbar")
        fna = h.DIV(h.DIV(nav, Class="container"), Class="first_nav")
        return fna


class LandingPage(SimplePage):
    # Inicia os atributos da classe
    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")

    # Constroi a lading page,, essa é bem intuitiva
    def build_body(self):

        h = self.brython.html
        tt1 = h.IMG(src="/src/arvora/_media/arvora_logo.png", style="width: 465px;")
        tt1D = h.DIV(tt1)
        tt2 = h.IMG(src="/src/arvora/_media/asset2.png", style="width: 265px;margin-top:10px")
        tt2D = h.DIV(tt2)
        # phr = phrase
        phr = h.P("Seu lugar de pesquisas de neurociência!", Class='main-text title is-3')
        # retorna uma div com todos os elementos da página
        return h.DIV((tt1D, tt2D, phr))



class LoginPage(SimplePage):
    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")
        # inicia o self.form, self.login e o self.passd
        #self.form = self.login = self.passd = None

    def write(self, data=None):
        ajax = self.brython.ajax
        def on_complete(req):
            if req.status==200:
                print("complete ok: " + f'{req.status}')
                if json.loads(req.text) == "ok":
                    SimplePage.PAGES["_MAIN_"].show()
                if json.loads(req.text) == "error":
                    div_resultados = self.brython.document['resultado']
                    div_resultados.clear()
                    text = self.brython.html.P('Este e-mail não esta cadastrado.')
                    men = self.brython.html.DIV(text, Class="notification is-danger is-light")
                    div_resultados <= men
                if json.loads(req.text) == "!ok":
                    div_resultados = self.brython.document['resultado']
                    div_resultados.clear()
                    text = self.brython.html.P('Senha incorreta.')
                    men = self.brython.html.DIV(text, Class="notification is-danger is-light")
                    div_resultados <= men

            else:
                print("error detected: " + f'{req.status}')

        req = ajax.Ajax()
        req.bind('complete', on_complete)
        req.open('POST', '/login', True)
        req.set_header('content-type', 'application/json')
        req.send(json.dumps(data))
    def click(self, ev=None):
        _ = self
        _ = self
        doc = _.brython.document
        # Pegando os dados informados para login
        email = doc["email"].value
        password = doc["password"].value
        doc["email"].value = ""
        doc["password"].value = ""
        #verificando se os dados estão corretos


        data = {
            "email": email,
            "password": password,
        }
        print(data)
        #if data['email'] == email:
         #   print('deu certo')
        #else:
         #   print('n foi')


        self.write(data)

        # USER_OPTIONS = form.elements["username"].value
        # Arvora.ARVORA.user(form.elements["username"].value)




    def build_body(self):
        def click(ev):
            if ev.target.id == "cadastro":
                SimplePage.PAGES["_CADASTRO_"].show()

        h = self.brython.html

        # email
        resultado = h.DIV(id = "resultado")
        ema = h.LABEL('E-mail', Class="label mt-4", style="text-align: left;")
        self.login = h.INPUT(Id="email", Class="input is-success", type="email", placeholder="ex.: alexsmith@hhh.com")
        emaC = h.DIV(self.login, Class="control")
        emaD = h.DIV((ema, emaC), Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finale = h.DIV(emaD, Class="columns is-mobile")

        # senha
        pas = h.LABEL('Senha', Class="label mt-4", style="text-align: left;")
        self.passd = h.INPUT(Id="password", Class="input is-success", type="password")
        pasC = h.DIV(self.passd, Class="control has icons-left")
        pasD = h.DIV((pas, pasC), Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finalg = h.DIV(pasD, Class="columns is-mobile")

        # button
        button = h.BUTTON("Login", Class="button is-success is-outlined")
        buttonD = h.DIV(button, Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finalh = h.DIV(buttonD, Class="columns is-mobile")

        #btn = h.BUTTON("Login", Class="button is-primary is-fullwidth", type="submit")
        # Aqui ele faz os inputs de senha e login e coloca um label neles. Não sei pq tem que ser self.login

        # psw = h.DIV(h.LABEL("Password", For="Name") + self.passd, Class="field")
        # self.login = h.INPUT(Id="username", Class="input is-primary", type="email", placeholder="Email address")
        # eid = h.DIV(h.LABEL("Email", For="email") + self.login,  Class="field")
        link = h.A("Se cadastre aqui", Id='cadastro', Class = "has-text-dark")
        linkD = h.DIV(link, Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finall = h.DIV(linkD, Class="columns is-mobile")
        link.bind("click", click)
        form = h.DIV((resultado,finale, finalg, finall, finalh), Class="column")
        # Aqui ele bota um submit ao apertar o botão do form e chama a função click
        button.bind("click", self.click)

        # Aqui ele retorna a div com todos os elementos, após aplicar o bulma
        cls = h.DIV(form, Class="columns is-flex is-centered")
        return cls





0

class CadastroPage(SimplePage):
    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_pesquisa")

    def click(self, ev=None):

        ajax = self.brython.ajax
        doc = self.brython.document

        name = doc['name'].value
        email = doc["email"].value
        phone = doc["phone"].value
        password = doc["password"].value

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password,
        }

        def on_complete(req):
            if req.status == 200:
                print("cadastro completo " + f'{req.status}')
                if json.loads(req.text) == "ok":
                    SimplePage.PAGES["_MAIN_"].show()
            else:
                print("error detected " + f'{req.status}')
        print(data)
        req = ajax.Ajax()
        req.bind("complete", on_complete)
        req.open('POST', '/save-user', True)
        req.set_header("content-Type", "application/json")
        req.send(json.dumps(data))

        #SimplePage.PAGES["_MAIN_"].show()

    def build_body(self):
        h = self.brython.html
        tit = h.P('Cadastro', Class="title is-1 is-spaced", style="font-family: fantasy;")

        #nome
        nom = h.LABEL('Nome', Class="label mt-4", style="text-align: left;")
        nomI = h.INPUT(Id="name", Class="input is-success", type="text", placeholder="ex.: Alex Smith")
        nomC = h.DIV(nomI, Class="control")
        nomD = h.DIV((tit,nom, nomC), Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finald = h.DIV(nomD,  Class="columns is-mobile")

        #email
        ema = h.LABEL('E-mail', Class="label mt-4", style="text-align: left;")
        emaI = h.INPUT(Id="email", Class="input is-success", type="text", placeholder="ex.: alexsmith@hhh.com")
        emaC = h.DIV(emaI, Class="control")
        emaD = h.DIV((ema, emaC), Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finale = h.DIV(emaD,  Class="columns is-mobile")

        #telefone
        tel = h.LABEL('Telefone', Class="label mt-4", style="text-align: left;")
        telI = h.INPUT(Id="phone", Class="input is-success", type="text", placeholder="ex.: (00)0000-0000")
        telC = h.DIV(telI, Class="control")
        telD = h.DIV((tel, telC), Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finalf = h.DIV(telD,  Class="columns is-mobile")

        #senha
        pas = h.LABEL('Senha', Class="label mt-4", style="text-align: left;")
        pasI = h.INPUT(Id="password", Class="input is-success", type="text")
        pasC = h.DIV(pasI, Class="control")
        pasD = h.DIV((pas, pasC), Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finalg = h.DIV(pasD, Class="columns is-mobile")

        #button
        button = h.BUTTON("Salvar", Class="button is-success is-outlined")
        buttonD = h.DIV(button, Class="field column is-half is-offset-one-quarter", style="width:500px;")
        finalh = h.DIV(buttonD, Class="columns is-mobile")

        button.bind("click", self.click)

        form = h.DIV((finald, finale, finalf, finalg, finalh), Class="form")

        return form

class PesquisaPage(SimplePage):
    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_pesquisa")


    def build_body(self):
        h = self.brython.html
        ajax = self.brython.ajax
        tor = []

        def refresh(ev):
            def on_complete(req):
                if req.status == 200:
                    text = req.text
                    try:
                        resultados = json.loads(text)

                    except:
                        resultados = [{"title": "Rascunho 1", "abstract": "resumo"},
                                  {"title": "Rascunho 2", "abstract": "resumo 2"},
                                  {"title": "Rascunho 3", "abstract": "resumo 3"}]
                    show(resultados)

            wrp.clear()
            wrp <= h.DIV((img, pes, bt), Class="column body-columns")
            req = ajax.Ajax()
            req.bind('complete', on_complete)
            req.open('GET', '/load-article', True)
            req.set_header('content-type', 'application/json')
            req.send()

        def show(resultados):
            tor = []
            # Loop que mostra as páginas de rascunho
            pes_value = pes.value
            for d in resultados:
                print("u")
                if pes_value == d.get("tags"):
                    title = d.get("title")
                    body = d.get("body")
                    tags = d.get("tags")

                    tit = h.P(title, Class='title is-4')
                    abst = h.P(body, Class='text is-6')
                    tag = h.P(("tag: ", tags), Class="text is-6")


                    # todos os rascunhos
                    tor.append(h.DIV((tit, abst, tag), Class='box'))



            wrp.clear()
            wrp <= h.DIV( tor, Class="column body-columns")




            return wrp

        img = h.IMG(src="/src/arvora/_media/arvora_logo.png", Class="img_logo")
        log = h.IMG(src="/src/arvora/_media/lupa.svg", style="width: 365px;")
        pes = h.INPUT(log, type="text", Class="input is-success is-rounded mt-5 input-icon", placeholder="Rounded in", style="width: 1000px;")
        bt = h.BUTTON("Pesquisar", id="bt-pesquisa", Class="button is-success is-rounded mt-5 is-responsive", width="68", type='submit').bind("click", refresh)


        wrp = h.DIV((img,pes, bt, tor), Class="column body-columns")

        return wrp


class ProjectPage(SimplePage):
    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")
    def build_body(self):

        #   ATENÇÃO
        #   Segue abaixo as seguintes informações importantes:
        #   Legenda: Title _t Subtitle _s Anchor _a Imagem _img
        #   Temos Introdução, Objetivo, Usuario(Cliente) e Estágio Atual
        #
        #   O QUE FALTA? Estou com problemas em dimensionar a imagem. O código está na linha 145 com o r_img. Boa sorte e obrigado!
        #   Se conseguir aumentar a parto do PROJETO ARVORA eu agradeceria também ehehehhe


        h = self.brython.html

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        #hr = h.HR(Class = "content-divider")

        pj_t1 = h.H1("Projeto ", Class = "title main-subtext")
        pj_t2 = h.H1("ARVORA", Class="title main-text")
        pj_t = h.DIV((pj_t1, pj_t2), Class="columns")
        pj_s = h.H2("O que é a Brain Computational School", Class = "subtitle is-1")
        pj_a = h.A("Comece aqui!", href='#intro', Class = "button is-white is-medium is-inverted")
        pj_div=h.DIV((pj_t, pj_s, pj_a), Class="has-text-centered")
        pj = h.SECTION(pj_div, Class=" hero is-medium hero-body is-fullheight columns is-centered")

        r_t = h.H1("Introdução", id = "intro", Class="title is-3 ") # resume title
        r_img = h.FIGURE((h.IMG(src="https://bulma.io/images/placeholders/256x256.png")), Class="image is-fullwidth")
        r_fig = h.DIV(r_img, Class="column is-3 ")
        r_p = h.P(text, Class="subtitle")

        r_text = h.DIV((r_t, r_p), Class="hero is-large hero-body container column is-6 featured-content")
        r = h.SECTION((r_fig, r_text), Class="columns")

        obj_t = h.H1("Objetivo", Class="title is-3 ") # objective title
        obj_p = h.P(text,  Class = "subtitle")
        obj = h.SECTION((obj_t, obj_p),
                        Class="hero is-large hero-body container has-text-left")

        cli_t = h.H1("Usuário", Class="title is-3 ")  # client title
        cli_img = h.FIGURE((h.IMG(src="https://bulma.io/images/placeholders/256x256.png")), Class="image is-fullwidth")
        cli_fig = h.DIV(cli_img, Class="column is-3 ")
        cli_p = h.P(text,  Class = "subtitle")
        cli_text = h.DIV((cli_t, cli_p), Class="hero is-large hero-body container column is-6 featured-content")
        cli = h.SECTION((cli_text, cli_fig), Class="columns")

        done_t = h.H1("Estágio Atual", Class="title is-3 ")  # Estage title
        done_p1 = h.P(text, Class="subtitle")
        done_p2 = h.P(text, Class="subtitle")
        done = h.SECTION((done_t, done_p1, done_p2),
                        Class="hero is-large hero-body container has-text-left columns")
        #r = h.SECTION((r_t, r_p), Class = "content has-text-left")

        box = h.DIV((r, obj, cli, done), CLass = "hero box m-6")
        sec = h.DIV((pj, box), Class = "")

        return sec

users = [
    {
        "name": "Roberto",
        "email": "roberto@mail",
        "points": "100",
        "id": "1",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "tags": "#mav",
        "date": "2021-01-21"
    },
    {
        "name": "Amanda",
        "email": "amanda@mail",
        "points": "72",
        "id": "2",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "tags": "#mav",
        "date": "2021-01-21"
    },
    {
        "name": "Roberto",
        "email": "roberto@mail",
        "points": "100",
        "id": "1",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "tags": "#mav",
        "date": "2021-01-21"
    },
    {
        "name": "Amanda",
        "email": "amanda@mail",
        "points": "72",
        "id": "2",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "tags": "#mav",
        "date": "2021-01-21"
    },
    {
        "name": "Amanda",
        "password": "1234",
        "email": "amanda@mail",
        "posts":[
            {
                "id": "1",
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "tags": "#mav",
                "date": "2021-01-21"
            },
        ]
     },]


class KnowledgePage(SimplePage):
    # def refresh(ev):
    #     def on_complete(req):
    #         if req.status == 200:
    #             text = req.text
    #             try:
    #                 drafts = json.loads(text)
    #
    #             except:
    #                 drafts = [{"title": "Rascunho 1", "abstract": "resumo"},
    #                           {"title": "Rascunho 2", "abstract": "resumo 2"},
    #                           {"title": "Rascunho 3", "abstract": "resumo 3"}]
    #             show(drafts)
    #
    #     req = ajax.Ajax()
    #     req.bind('complete', on_complete)
    #     req.open('GET', '/load-article', True)
    #     req.set_header('content-type', 'application/json')
    #     req.send()
    #
    # def show(drafts):
    #     tor = []
    #     # Loop que mostra as páginas de rascunho
    #     for d in drafts:
    #         print("u")
    #
    #         title = d.get("title")
    #         body = d.get("body")
    #
    #         tit = h.P(title, Class='title is-4')
    #         abst = h.P(body, Class='text is-6')
    #         btnd = h.BUTTON("Deletar", Class="button is-danger is-rounded mt-5 is-responsive block is-fullwidth",
    #                         type='submit')
    #
    #         # todos os rascunhos
    #         tor.append(h.DIV((tit, abst, btnd), Class='box'))
    #     wrp.clear()
    #     wrp <= h.DIV((bt, tor), Class="column body-columns")
    #
    #     return wrp

    def __init__(self, brython, menu = MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")

    def click(self, ev=None):
        if ev.target.id == "Draft":
            SimplePage.PAGES["_RASCUNHO_"].show()
        elif ev.target.id == "Writing":
            SimplePage.PAGES["_ESCREVER_"].show()
    def show_article(ev):
        SimplePage.PAGES["_ARTIGO_"].show()

    def build_body(self):
        ajax = self.brython.ajax
        h = self.brython.html

        posts = h.P("Error")
        def get_article():
            def on_complete(req):
                if req.status == 200:
                    text = req.text
                    try:
                        drafts = json.loads(text)

                    except:
                        drafts = [{"title": "Rascunho 1", "abstract": "resumo"},
                                  {"title": "Rascunho 2", "abstract": "resumo 2"},
                                  {"title": "Rascunho 3", "abstract": "resumo 3"}]
                    show(drafts)
            req = ajax.Ajax()
            req.bind('complete', on_complete)
            req.open('GET', '/load-article', True)
            req.set_header('content-type', 'application/json')
            req.send()

        def show(articles):
            card = ""
            search_bar = h.FORM(h.DIV(
                h.INPUT(type="text", Class="input is-success is-rounded mt-5 input-icon green-placeholder",
                        placeholder="Pesquise aqui"), Class="column"))
            # Loop que mostra as páginas de rascunho
            for article in articles:
                card_img = h.FIGURE(h.IMG(src="https://bulma.io/images/placeholders/256x256.png"),
                                    Class="card-image image is-4by3")

                card_content = h.DIV((
                    h.FIGURE(
                        (h.IMG(src="https://res.cloudinary.com/ameo/image/upload/v1639144778/typocat_svbspx.png")),
                        Class="media-left image is-48x48"),
                    h.P(article.get("title"), Class="title is-4"),
                    h.P("email", Class="subtitle is-6"),
                    h.P("Estrelas: " + "10"),
                    h.P(article.get("body")),
                    h.P(article.get("tags")),
                    h.P("data")), Class="content")

                card_buttons = h.DIV((
                    h.BUTTON("Comentar", Class="button is-primary"),
                    h.BUTTON("Perguntar", Class="button is-info"),
                    h.BUTTON("Artigos Filhos", Class="button")), Class="card-footer")

                card += h.DIV((card_img, card_content, card_buttons), Class="box").bind("click", self.show_article)
            post = h.DIV((search_bar, card), Class="column is-half is-offset-one-quarter ")
            posts.clear()
            posts <= h.DIV(post, Class="columns body-columns")
            return posts

        get_article()

        btn1 = h.BUTTON("Rascunho", Id='Draft',
                        Class="button is-success is-rounded mt-5 is-responsive block is-fullwidth")
        btn2 = h.BUTTON("Escreva seu artigo", Id="Writing",
                        Class="button is-success is-rounded mt-5 is-responsive block is-fullwidth")
        side_tab = h.DIV((btn2, btn1), Class="column is-3")
        side_tab.bind("click", self.click)


        wrapper = h.DIV((side_tab, posts))
        return wrapper


class Article(SimplePage):
    def __init__(self, brython, menu = MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")
    def build_body(self):
        h = self.brython.html
        user = users[0]


        card_img = h.FIGURE(h.IMG(src="https://bulma.io/images/placeholders/256x256.png"),
                            Class="card-image image is-4by3")

        card_content = h.DIV((
            h.FIGURE((h.IMG(src="/src/arvora/_media/arvora_logo.png")),
                     Class="media-left image is-48x48"),
            h.P(user["name"], Class="title is-4"),
            h.P(user["email"], Class="subtitle is-6"),
            h.P("Estrelas: " + user["points"]),
            h.P(user["text"]),
            h.P(user["tags"]),
            h.P(user["date"])), Class="content")

        card_buttons = h.DIV((
            h.BUTTON("Comentar", Class="button is-primary"),
            h.BUTTON("Perguntar", Class="button is-info"),
            h.BUTTON("Artigos Filhos", Class="button")), Class="card-footer")





        #comment section




        #user comment
        user_photo = h.FIGURE(
            h.P((h.IMG(src="https://bulma.io/images/placeholders/128x128.png")), Class="image is-64x64"),
            Class="media-left")
        comment_box = h.DIV(h.TEXTAREA(placeholder = "Escreva aqui...", Class = " Focused textarea is-success has-fixed-size has-text-success-dark"), Class = "media-content field control")
        comment_section = h.ARTICLE((user_photo, comment_box), Class="media mt-5")

        card = h.DIV((card_img, card_content, card_buttons, comment_section), Class="box")
        post = h.DIV(card, Class="column is-half is-offset-one-quarter ")
        posts = h.DIV(post, Class="columns body-columns")

        return posts

class WritingPage(SimplePage):
    # Adicionando o init
    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")
        self.form = self.text = None

    def write(self, data=None):
        ajax = self.brython.ajax
        def on_complete(req):
            if req.status==200:
                print("complete ok>>>> " + f'{req.status}')
            else:
                print("error detected>>>> " + f'{req.status}')

        req = ajax.Ajax()
        req.bind('complete', on_complete)
        req.open('POST', '/save-article', True)
        req.set_header('content-type', 'application/json')
        req.send(json.dumps(data))
    def click(self, ev=None):

        _ = self
        doc = _.brython.document
        # form = doc['form'].html
        title = doc["title"].value
        body = doc["body"].value
        tags = doc["tags"].value
        data = {
            "title": title,
            "body": body,
            "tags": tags
        }

        self.write(data)
        # USER_OPTIONS = form.elements["username"].value
        #Arvora.ARVORA.user(form.elements["username"].value)
        SimplePage.PAGES["_MAIN_"].show()

    # construindo a página em si
    def build_body(self):

        h = self.brython.html
        # um botão para enviar o formulário
        btn1 = h.BUTTON("Enviar", Class="button is-success is-rounded mt-5 is-responsive block is-fullwidth", type="submit")
        btn2 = h.BUTTON("Deletar", Class="button is-danger is-rounded mt-5 is-responsive block is-fullwidth", type='submit')
        # O campo onde as pessoas pode escrever o texto delas, esse monte de tag é o bulma. Ela tem os placeholders e o rows que é a quantidade padrão de linhas
        self.text = h.TEXTAREA(
            Class="textarea is-success has-fixed-size block mb-4 mt-0 has-text-success-dark is-medium",
            Id = "body",
            rows='17', type="text", placeholder="Comece a escrever aqui!")
        # Aqui eu criei uma div para armazenar todos os componentes da página
        div = h.DIV()
        # tit == titulo. Esse é o título da página
        tit = h.P("Escrev0a seu artigo", Class='title is-2 block hero p-2 has-text-success incText')
        # aut == autor. Aqui que a pessoa pode botar o nome dela ((só uma ideia inicial))
        aut = h.INPUT(placeholder='Título',
                      Id = "title",
                      Class='input is-success has-fixed-size block has-text-success-dark is-medium')
        tag = h.INPUT(placeholder='Tags',
                      Id = "tags",
                      Class='input is-success has-fixed-size block has-text-success-dark is-medium')
        # Aqui eu to adicionando tudo dentro da div, na ordem que eu quero que eles aparecam
        div <= (tit, aut, self.text, tag)
        # aqui eu encapsulei a div com tudo e o botão em um formulário
        btn1.bind("click", self.click)
        form = h.DIV((div, btn1, btn2), Id = 'form', Class="column")

        # inte == interactions. aqui eu adicionei tudo isso em outra div
        quest = h.DIV(form, Class="columns is-flex")
        # Aqui eu to retornando a div com todos os elementos
        return quest

class DraftPage(SimplePage):

    def __init__(self, brython, menu=MENU_OPTIONS):
        super().__init__(brython, menu, hero="main_hero")

    def build_body(self):
        h = self.brython.html
        ajax = self.brython.ajax
        tor = []
        def refresh(ev):
            def on_complete(req):
                if req.status == 200:
                    text = req.text
                    try:
                        drafts = json.loads(text)

                    except:
                        drafts = [{"title": "Rascunho 1", "abstract": "resumo"},
                                  {"title": "Rascunho 2", "abstract": "resumo 2"},
                                  {"title": "Rascunho 3", "abstract": "resumo 3"}]
                    show(drafts)
            req = ajax.Ajax()
            req.bind('complete', on_complete)
            req.open('GET', '/load-article', True)
            req.set_header('content-type', 'application/json')
            req.send()
        def show(drafts):
            tor = []
            # Loop que mostra as páginas de rascunho
            for d in drafts:
                print("u")

                title = d.get("title")
                body = d.get("body")
                tags = d.get("tags")

                tit = h.P(title, Class='title is-4')
                abst = h.P(body, Class='text is-6')
                tag = h.P(("tags: ", tags), Class="text is-6")
                btnd = h.BUTTON("Deletar", Class="button is-danger is-rounded mt-5 is-responsive block is-fullwidth",
                                type='submit')

                # todos os rascunhos
                tor.append(h.DIV((tit, abst, tag, btnd), Class='box'))
            wrp.clear()
            wrp <= h.DIV((bt, tor), Class="column body-columns")

            return wrp

        bt = h.BUTTON("Atualizar", Class="button is-primary is-rounded mt-5 is-responsive block is-fullwidth",
                        type='submit').bind("click", refresh)


        wrp = h.DIV((bt,tor), Class="column body-columns")

        return wrp

class Arvora:
    ARVORA = None

    # Iniciando os atributos da classe
    def __init__(self, br):
        #Separando os usuários entre admin e user
        self.users = dict(ADMIN="admin", USER="user")
        self.brython = br
        self.current_user = None
        Arvora.ARVORA = self

    #Criando a função do usuário atual
    def user(self, current_user):
        self.current_user = current_user

    #Função para iniciar
    def start(self):
        br = self.brython
        # Aqui as o nome das páginas são lincadas com as respectivas classes das páginas
        SimplePage.PAGES = {f"_{page}_": SimplePage(br) for page, _ in MENU_OPTIONS}
        SimplePage.PAGES["_MAIN_"] = LandingPage(br)
        SimplePage.PAGES["_PESQUISA_"] = PesquisaPage(br)
        SimplePage.PAGES["_LOGIN_"] = LoginPage(br)
        SimplePage.PAGES['_CADASTRO_'] = CadastroPage(br)
        SimplePage.PAGES["_PROJETO_"] = ProjectPage(br)
        SimplePage.PAGES["_CONHECIMENTO_"] = KnowledgePage(br)
        SimplePage.PAGES["_ARTIGO_"] = Article(br)
        # SimplePage.PAGES['_PERGUNTAS_'] = QuestionsPage(br)
        SimplePage.PAGES["_RASCUNHO_"] = DraftPage(br)
        SimplePage.PAGES["_ESCREVER_"] = WritingPage(br)

        _main = LandingPage(br)
        _main.show()
        return _main


def main(br):
    return Arvora(br).start()
