import http.server, socketserver, os
os.chdir(r"C:/Users/Anton/Desktop/HyperPartner/_deploy")
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self): self.send_header("Cache-Control","no-store"); super().end_headers()
    def log_message(self,*a): pass
class T(socketserver.ThreadingMixIn, socketserver.TCPServer): allow_reuse_address=True
print("serving on 5185"); T(("127.0.0.1",5185),H).serve_forever()
