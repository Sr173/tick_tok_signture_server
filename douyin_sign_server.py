from selenium import webdriver
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import threading

data = {'result': 'this is a test'}
host = ('0.0.0.0', 777)

opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.headless = True
opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36");
drive = webdriver.Chrome(options=opt)

lock = threading.Lock()

class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            lock.acquire()
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            f = open("./tac.js", "w")
            f.write(bytes.decode(post_body))
            f.close()
            drive.get("file:///" + os.getcwd() + "/get_sign.html")

            sign = drive.find_element_by_xpath("/html/body").text

            self.send_response(200)
            self.end_headers()
            self.wfile.write(str.encode(sign))
        except:
            self.wfile.write(str.encode(""))
        finally:
            lock.release()

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
