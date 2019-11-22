from selenium import webdriver
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import threading

data = {'result': 'this is a test'}
host = ('localhost', 8888)

opt = webdriver.ChromeOptions()
#opt.headless = True
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