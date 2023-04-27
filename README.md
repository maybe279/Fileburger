# Fileburger

基于python http.server 用于接受内网回传的文件，用curl发送http

**使用curl反传文件至服务器**

现在，使用以下curl命令将`example.txt`文件上传到服务器，并将其保存为`destfilename.txt` ，并在Cookie中加入用户名密码：

```shell
curl -X POST -H "Content-Type: application/octet-stream" -H "Content-Disposition: attachment; filename=destfilename.txt" -H "Cookie: user=alice:abc123;" --data-binary "@example.txt" http:x.x.x.x:8000/
```