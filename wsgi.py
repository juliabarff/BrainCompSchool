#!/usr/bin/env python
# noinspection GrazieInspection
""" Web server runner.

Classes neste módulo:
    - :py:class:`DirectoryHandler` handle all routes from web.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>
.. codeauthor:: Craig Campbell <https://craig.is>

Changelog
---------
.. versionchanged::    24.03
   |br| Revert to enable serving index from root (07).

.. versionadded::    24.03
   |br| Initial server implementation (07).

|   **Open Source Notification:** This file is part of open source program **Pynoplia**
|   **Copyright © 2024  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   # Copyright (c) 2018, Craig Campbell
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <https://labase.github.io/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""

import os
import json
import src.arvora._model.database as DS
import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.escape import xhtml_escape
import tornado.websocket

# config options
define('port', default=8888, type=int, help='port to run web server on')
define('debug', default=True, help='start app in debug mode')
define('route_to_index', default=True, help='route all requests to index.html')
options.parse_command_line(final=True)

PORT = options.port
DEBUG = options.debug
ROUTE_TO_INDEX = options.route_to_index
ROUTE_TO_INDEX = True
PATH = '/'




class DirectoryHandler(tornado.web.StaticFileHandler):
    def validate_absolute_path(self, root, absolute_path):
        print("val0", absolute_path, self.request.uri, os.path.isdir(absolute_path))
        if ROUTE_TO_INDEX and self.request.uri != '/' and '.' not in self.request.uri:
            uri = self.request.uri
            print("validate", uri)
            if self.request.uri.endswith('/'):
                uri = uri[:-1]

            absolute_path = absolute_path.replace(uri, 'index.html')

        if os.path.isdir(absolute_path):
            index = os.path.join(absolute_path, 'src/arvora/index.html')
            print("os.path.isfile(index)", index, root, os.path.isfile(index))
            if os.path.isfile(index):
                print("if os.path.isfile(index)", index, absolute_path)
                return index

            return absolute_path

        return super(DirectoryHandler, self).validate_absolute_path(root, absolute_path)

    def get_content_type(self):
        if self.absolute_path.endswith('.vtt'):
            return 'text/vtt'

        if self.absolute_path.endswith('.m3u8'):
            return 'application/vnd.apple.mpegurl'

        content_type = super(DirectoryHandler, self).get_content_type()

        # default to text/html
        if content_type == 'application/octet-stream':
            return 'text/html'

        return content_type

    @classmethod
    def get_content(cls, abspath, start=None, end=None):
        relative_path = abspath.replace(os.getcwd(), '') + '/'
        print("get content", relative_path, abspath)

        if os.path.isdir(abspath):
            html = ('<html><title>Directory listing for %s</title><body><h2>Directory listing for %s</h2><hr><ul>'
                    % (relative_path, relative_path))
            for filename in os.listdir(abspath):
                force_slash = ''
                full_path = filename
                if os.path.isdir(os.path.join(relative_path, filename)[1:]):
                    full_path = os.path.join(relative_path, filename)
                    force_slash = '/'

                html += '<li><a href="%s%s">%s%s</a>' % (
                    xhtml_escape(full_path), force_slash, xhtml_escape(filename), force_slash)

            return html + '</ul><hr>'

        return super(DirectoryHandler, cls).get_content(abspath, start=start, end=end)

class ArticleHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')
    def get(self):
        self.write(json.dumps(DS.Article.load_articles()))
    def post(self):
        data = self.request.body
        DS.Article.insert(data)
        self.write(json.dumps({"message": "Article saved"}))


class UpdateStatusHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        try:
            data = json.loads(self.request.body)
            title = data['title']
            new_status = data['status']

            updated_article = DS.Article.update_status(title, new_status)
            if updated_article:
                self.write(json.dumps({'message': 'Status atualizado com sucesso', 'article': updated_article}))
            else:
                self.set_status(404)
                self.write(json.dumps({'error': 'Artigo não encontrado'}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'error': str(e)}))

class MainPageHandler(tornado.web.RequestHandler):
    async def get(self):
        session_id = self.get_cookie("session_id")
        if session_id and DS.User.is_valid_session(session_id):
            # Renderiza uma página HTML quando o usuário está logado
            self.render('main.html')  # Substitua por um arquivo HTML válido
        else:
            self.redirect('/login')

class LoginHandler(tornado.web.RequestHandler):
    async def post(self):
        form = self.request.body
        session_id = DS.User.login(form)

        self.set_header('Content-Type', 'application/json')

        if session_id:
            self.set_cookie("session_id", session_id)
            response = json.dumps({'status': 'ok', 'session_id': session_id})
            self.write(response)
        else:
            self.write(json.dumps({'status': 'error'}))



class AuthenticatedHandler(tornado.web.RequestHandler):
    async def prepare(self):
        session_id = self.get_cookie("session_id")
        if not session_id or not DS.User.is_valid_session(session_id):
            return "ops"

    def get(self):
        self.write("You are logged in")
class UserHandler(tornado.web.RequestHandler):
    def get(self):
         self.write(json.dumps(DS.User.load_users()))
    def post(self):
        data = self.request.body
        text = DS.User.create(data)
        self.write(json.dumps(text))

class CheckLoginHandler(tornado.web.RequestHandler):
    async def get(self):
        session_id = self.get_cookie("session_id")
        if session_id and DS.User.is_valid_session(session_id):
            self.write(session_id)
            print(session_id)
        else:
            self.write("not_logged_in")
class PegaIDHandler(tornado.web.RequestHandler):
    async def get(self):
        session_id = self.get_cookie("session_id")
        if session_id and DS.User.is_valid_session(session_id):
            self.write(session_id)
            print(session_id)
        else:
            self.write("not_logged_in")

class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        # Recebe o session_id do corpo da requisição
        data = tornado.escape.json_decode(self.request.body)
        session_id = data.get('session_id')

        if session_id:
            # Remover o session_id (adicione sua lógica de remoção)
            self.clear_cookie("session_id")
            self.write({"status": "success"})
        else:
            self.set_status(400)
            self.write({"status": "error", "message": "session_id não fornecido"})





settings = {
    'debug': DEBUG,
    'gzip': True,
    'static_handler_class': DirectoryHandler
}

application = tornado.web.Application([
    (r'/save-article', ArticleHandler),
    (r'/load-article', ArticleHandler),
    (r'/save-user',  UserHandler),
    (r"/update-status", UpdateStatusHandler),
    (r"/check-login", CheckLoginHandler),
    (r"/logout", LogoutHandler),
    (r"/pega-id", PegaIDHandler),
    (r'/login', LoginHandler),
    (r"/protected", AuthenticatedHandler),
    (r'/(.*)', DirectoryHandler, {'path': './'}),
    #(r'/', DirectoryHandler, {'path': './src/arvora/index.html'}),
], **settings)

if __name__ == "__main__":
    print("Listening on port %d..." % PORT)
    application.listen(PORT)
    IOLoop.instance().start()