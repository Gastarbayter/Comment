import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import context

HOST_NAME = 'localhost'
PORT_NUMBER = 8080
DIRECTORIES = {'text/html': 'views', 'application/javascript': 'scripts'}


class HttpRequestHandler(BaseHTTPRequestHandler):
    """Класс обрабатывающий входящий запрос от браузера"""

    logging.basicConfig(filename='logs/server_errors.log', filemode='a', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    _context = context.Context.get_instance()

    def do_GET(self):
        """Обработчик для запросов GET"""

        try:
            if self.path in ('/comment', '/comment/'):
                self.path = 'comment.html'
            elif self.path in ('/stat/', '/stat/'):
                self.path = 'statistic.html'
            elif self.path == '/scripts/comment.js':
                self.path = 'comment.js'
            elif self.path in ('/view', '/view/'):
                self.path = 'view.html'
            elif self.path == '/scripts/view.js':
                self.path = 'view.js'
            elif self.path in ('/statistic', '/statistic/'):
                self.path = 'statistic.html'
            elif self.path == '/scripts/statistic.js':
                self.path = 'statistic.js'
            elif self.path == '/get_all_regions':
                region = self._context.get_all_regions()
                self._send_response(data=region)
            elif '/get_all_regions/' in self.path:
                city = self._context.get_cities_by_region_id(self.path.replace('/get_all_regions/', ''))
                self._send_response(data=city)
            elif self.path == '/get_all_comments':
                comments = self._context.get_all_comments()
                self._send_response(data=comments)
            elif self.path in ('/get_statistics', '/get_statistics/'):
                statistic = self._context.statistics()
                self._send_response(data=statistic)
            elif '/get_city_statistic/' in self.path:
                statistic = self._context.city_statistics_by_region(self.path.replace('/get_city_statistic/', ''))
                self._send_response(data=statistic)
            else:
                self.send_error(404, 'OOPS! ')

            send_reply = False
            if self.path.endswith(".html"):
                mime_type = 'text/html'
                send_reply = True
            elif self.path.endswith(".jpg"):
                mime_type = 'image/jpg'
                send_reply = True
            elif self.path.endswith(".js"):
                mime_type = 'application/javascript'
                send_reply = True
            elif self.path.endswith(".css"):
                mime_type = 'text/css'
                send_reply = True

            if send_reply:
                f = open(os.path.join(os.path.curdir, DIRECTORIES[mime_type], self.path), 'rb')
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except Exception as ex:
            logging.exception(ex)
            self.send_error(404, 'OOPS! ')

    def do_POST(self):
        """Обработчик для запросов POST"""

        try:
            if self.path == '/comment':
                post_data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))

                if bool(post_data):
                    self._context.add_comment(post_data['surname'],
                                              post_data['name'],
                                              post_data['comment'],
                                              int(post_data['city']),
                                              post_data['patronymic'] if 'patronymic' in post_data else str(),
                                              post_data['contact_number'] if 'contact_number' in post_data else str(),
                                              post_data['email'] if 'email' in post_data else str())

                    self._send_response(response_code=201)
                self._send_response(response_code=204)
        except Exception as ex:
            logging.exception(ex)
            self.send_error(404, 'OOPS! ')

    def do_DELETE(self):
        """Обработчик для запросов DELETE"""

        try:
            if '/comments/' in self.path:
                self._context.delete_comment_by_id(self.path.replace('/comments/', ''))
                self._send_response(response_code=201)
        except Exception as ex:
            logging.exception(ex)
            self.send_error(404, 'OOPS! ')

    def _send_response(self, data=None, response_code=None):
        try:
            self.send_response(response_code if response_code is not None else 200)
            self.end_headers()
            if data is not None:
                self.wfile.write(json.dumps(data).encode('utf-8'))
        except Exception as ex:
            logging.exception(ex)
            self.send_error(404, 'OOPS!')


try:

    server = HTTPServer((HOST_NAME, PORT_NUMBER), HttpRequestHandler)
    print('Started http server on port', PORT_NUMBER)
    server.serve_forever()

except KeyboardInterrupt:
    print('Stopped http server on port', PORT_NUMBER)
    server.socket.close()

if __name__ == '__main__':
    HttpRequestHandler()
