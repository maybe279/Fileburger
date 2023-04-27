import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer

# 定义用户信息
user_database = {
    'alice': {'password': 'abc123'},
    'bob': {'password': 'passw0rd'}
}

# 验证函数
def authenticate(username, password):
    # 获取用户的凭据
    user_credentials = user_database.get(username)
    if user_credentials:
        # 对密码进行哈希处理
        # hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # # 比较哈希值
        # if hashed_password == user_credentials['password']:
        return True
    # 如果未找到用户或密码不匹配，则返回 False
    return False

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # 获取用户名和密码的 cookie
        cookie = self.headers.get('Cookie')
        if not cookie:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Login required"')
            self.end_headers()
            self.wfile.write(b'Authentication required')
            return
        
        # 解析用户名和密码
        username_password = cookie.split(';')[0].split('=')[1]
        username, password = username_password.split(':')
        
        # 验证用户
        if not authenticate(username, password):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Login required"')
            self.end_headers()
            self.wfile.write(b'Authentication failed')
            return

        # 获取上传的文件名
        content_disposition = self.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = 'uploaded_file.bin'  # 如果无法获取文件名，则使用默认值
        
        # 读取上传的文件内容并保存到服务器
        content_length = int(self.headers.get('Content-Length'))
        file_content = self.rfile.read(content_length)
        with open(filename, 'wb') as f:
            f.write(file_content)
        
        # 返回成功状态码和消息
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File uploaded successfully')


# 启动 HTTP 服务器
httpd = HTTPServer(('localhost', 8000), RequestHandler)
httpd.serve_forever()
