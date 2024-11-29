from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, parse_qsl
import cgi


# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        # Проверяем, какой URL был запрошен
        if self.path == "/":
            # Если запрошен корневой URL, отправляем страницу "Контакты"
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Читаем содержимое HTML-файла с контактами
            with open("templates/contacts.html", "r", encoding='utf-8') as f:
                html_content = f.read()
            self.wfile.write(bytes(html_content, "utf-8"))
        else:
            # Если запрошен другой URL, отправляем 404 Not Found
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<h1>404 Not Found</h1>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = dict(parse_qsl(post_data))
        print(f"Name: {post_params['name']}, email: {post_params['email']}, message: {post_params['message']}")

        # Do something with the post_params here

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open("templates/contacts.html", "r", encoding='utf-8') as f:
            html_content = f.read()
        self.wfile.write(bytes(html_content, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")