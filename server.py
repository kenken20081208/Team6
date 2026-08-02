from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import mimetypes
import os


# このserver.pyが置かれているフォルダ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# サーバーを起動するポート番号
PORT = 8000


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """ブラウザからページを開かれた時の処理"""

        # URLを解析してパスだけ取得
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # CSS・JavaScript・画像などを返す
        if path.startswith("/static/"):
            self.serve_static(path)
            return

        # URLごとに表示するHTMLを切り替える
        routes = {
            "/": "index.html",
            "/quiz": "quiz.html",
            "/result": "result.html",
        }

        filename = routes.get(path)

        # 対応するページがなければ404
        if filename is None:
            self.send_404()
            return

        self.render_template(filename)

    def render_template(self, filename):
        """templatesフォルダのHTMLを読み込んで表示する"""

        filepath = os.path.join(
            BASE_DIR,
            "templates",
            filename,
        )

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8",
            )
            self.end_headers()

            self.wfile.write(
                content.encode("utf-8")
            )

        except FileNotFoundError:
            self.send_404()

    def serve_static(self, path):
        """staticフォルダのCSS・JS・画像などを返す"""

        relative_path = path.lstrip("/")

        filepath = os.path.abspath(
            os.path.join(BASE_DIR, relative_path)
        )

        static_directory = os.path.abspath(
            os.path.join(BASE_DIR, "static")
        )

        # staticフォルダ外へアクセスされるのを防止
        if not filepath.startswith(static_directory):
            self.send_404()
            return

        try:
            with open(filepath, "rb") as file:
                content = file.read()

            # ファイルの種類を自動判定
            content_type, _ = mimetypes.guess_type(filepath)

            if content_type is None:
                content_type = "application/octet-stream"

            self.send_response(200)
            self.send_header(
                "Content-Type",
                content_type,
            )
            self.end_headers()

            self.wfile.write(content)

        except FileNotFoundError:
            self.send_404()

    def send_404(self):
        """存在しないURLの処理"""

        content = "<h1>404 Not Found</h1>"

        self.send_response(404)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.end_headers()

        self.wfile.write(
            content.encode("utf-8")
        )


def run():
    """Webサーバーを起動する"""

    server_address = ("", PORT)

    server = HTTPServer(
        server_address,
        MyHandler,
    )

    print("サーバーを起動しました")
    print(f"http://localhost:{PORT}")
    print("終了する場合は Ctrl + C")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nサーバーを停止しました")

    finally:
        server.server_close()


if __name__ == "__main__":
    run()