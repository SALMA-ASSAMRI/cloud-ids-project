import http.server
import webbrowser
import os

os.chdir('frontend')
PORT = 8080

handler = http.server.SimpleHTTPRequestHandler
with http.server.HTTPServer(("", PORT), handler) as httpd:
    print(f"Serveur démarré sur http://localhost:{PORT}")
    print("Ouvre ton navigateur sur http://localhost:8080")
    webbrowser.open(f"http://localhost:{PORT}")
    httpd.serve_forever()