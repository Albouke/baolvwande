from mitmproxy import http
import re

class ModifyResponse:
    def request(self, flow: http.HTTPFlow) -> None:
        # 拦截指定的URL请求
        if re.match(r"https://leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js", flow.request.url):
            print(f"Intercepted URL: {flow.request.url}")
            # 你可以在这里修改请求数据
            # flow.request.headers["Custom-Header"] = "New-Value"
            # flow.request.query["param"] = "new_value"

    def response(self, flow: http.HTTPFlow) -> None:
        # 拦截指定的URL响应
        if re.match(r"https://leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js", flow.request.url):
            print(f"Modifying response for URL: {flow.request.url}")

            # 获取响应内容
            original_body = flow.response.text

            # 查找需要替换的函数名
            funname = re.search(r"(?<=isRight:)[^,]*?\(.*?\).*?(?=\|)", original_body)
            if funname:
                print(f"Found function name: {funname.group(0)}")
                # 替换函数名
                modified_body = original_body.replace(funname.group(0), f"{funname.group(0)}||true")
                flow.response.text = modified_body
                print("Modified response body")

            # 修改响应状态码或头部（可选）
            # flow.response.status_code = 200
            # flow.response.headers["Custom-Header"] = "New-Value"

addons = [
    ModifyResponse()
]
