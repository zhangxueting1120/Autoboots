import requests
import json
import jsonpath


class BodyType:
    URL_ENCODE = 'URL_ENCODE'
    JSON = 'JSON'
    FILE = 'FILE'


class Method:
    GET = 'GET'
    POST = 'POST'


class Client:
    SESSION = requests.session()

    def __init__(self, url, method='GET', body_type=None, timeout=5):
        self.url = url
        self.method = method
        self.params = {}
        self.body_type = body_type
        self.headers = {}
        self.timeout = timeout
        self.body = {}
        self.res = None
        self.flag = 0
        self.result = []
        self.only_session = False

    def set_header(self, key, value):
        self.headers[key] = value

    def set_headers(self, headers):
        if isinstance(headers, dict):
            self.headers = headers
        else:
            raise Exception('请求头信息请以字典形式填写!')

    def set_cookie(self, key, value):
        cookie = self.headers.get('Cookie')
        if not cookie:
            self.headers['Cookie'] = '{key}={value};'.format(key=key, value=value)
        else:
            self.headers['Cookie'] = cookie + '{key}={value};'.format(key=key, value=value)

    def set_body(self, data):
        if isinstance(data, dict):
            if self.body_type == BodyType.FILE:
                for name, filename in data:
                    self.body[filename] = open(filename, 'rb')
            else:
                self.body = data
        else:
            raise Exception('请求体请以字典形式填写!')

    def set_params(self, params):
        if isinstance(params, dict):
            self.params = params
        else:
            raise Exception('URL参数请以字典形式填写!')

    def send(self):
        if self.method == 'GET':
            try:
                if self.only_session:
                    self.res = Client.SESSION.get(url=self.url, params=self.params,
                                        headers=self.headers, timeout=self.timeout)
                else:
                    self.res = requests.get(url=self.url, params=self.params,
                                        headers=self.headers, timeout=self.timeout)
            except:
                raise Exception('服务器无响应或请求超时:get, url = {url} ]'.format(url=self.url))

        elif self.method == 'POST':
            if self.body_type == BodyType.URL_ENCODE:
                self.set_header('Content-Type', 'application/x-www-form-urlencoded')
                try:
                    if self.only_session:
                        self.res = Client.SESSION.post(url=self.url, headers=self.headers, data=self.body)
                    else:
                        self.res = requests.post(url=self.url, headers=self.headers, data=self.body)
                except:
                    raise Exception('服务器无响应或请求超时:post, url = {url}, data = {body}]'
                                    .format(url=self.url, body=self.body))

            elif self.body_type == BodyType.JSON:
                self.set_header('Content-Type', 'application/json')
                try:
                    if self.only_session:
                        self.res = Client.SESSION.post(url=self.url, headers=self.headers, json=self.body)
                    else:
                        self.res = requests.post(url=self.url, headers=self.headers, json=self.body)
                except:
                    raise Exception('服务器无响应或请求超时:post, url = {url}, json = {body}]'
                                    .format(url=self.url, body=self.body))

            elif self.body_type == BodyType.FILE:
                self.set_header('Content-Type', 'multipart/form-data')
                try:
                    if self.only_session:
                        self.res = Client.SESSION.post(url=self.url, headers=self.headers, files=self.body)
                    else:
                        self.res = requests.post(url=self.url, headers=self.headers, files=self.body)
                except:
                    raise Exception('服务器无响应或请求超时:post, url = {url}, files = {body}]'
                                    .format(url=self.url, body=self.body))
        else:
            raise Exception('不支持的请求方法类型!')

    @property
    def status_code(self):
        if self.res:
            return self.res.status_code
        else:
            return None

    @property
    def response_times(self):
        if self.res:
            return round(self.res.elapsed.total_seconds()*1000)
        else:
            return None

    @property
    def response_body(self):
        if self.res:
            return self.res.text
        else:
            return None

    @property
    def response_cookie(self):
        if self.res:
            return self.res.cookies
        else:
            return None

    def res_to_json(self):
        if self.res:
            try:
                return self.res.json()
            except:
                return None
        else:
            return None

    def json_value(self, path):
        if self.res:
            object = jsonpath.jsonpath(self.res_to_json(), path)
            if object:
                return object[0]
        return None

    def check_status_code(self, exp):
        try:
            assert self.status_code == exp
            self.result.append('响应状态码验证成功！')
        except:
            self.result.append('响应状态码验证失败！预期结果[{a}]，实际结果[{b}]'.format(
                a=exp, b=self.status_code
            ))
            self.flag += 1

    def check_response_less_than(self, exp):
        try:
            assert self.response_times <= exp
            self.result.append('响应时间验证成功！')
        except:
            self.result.append('响应时间验证失败！预期结果小于 [{a}] ms，实际结果 [{b}] ms'.format(
                a=exp, b=self.response_times
            ))
            self.flag += 1

    def check_response_body_equal(self, exp):
        try:
            assert exp == self.response_body
            self.result.append('响应内容验证成功！')
        except:
            self.result.append('响应内容验证失败！预期响应内容 {a}，实际响应内容 {b}'.format(
                a=exp, b=self.response_body
            ))
            self.flag += 1

    def check_response_body_contains(self, exp):
        try:
            assert exp in self.response_body
            self.result.append('响应内容验证成功！')
        except:
            self.result.append('响应内容验证失败！预期响应内容包含 [{a}]，实际响应内容 {b}'.format(
                a=exp, b=self.response_body
            ))
            self.flag += 1

    def check_json_value(self, node_name, exp):
        try:
            j = json.loads(self.response_body)
            try:
                assert j[node_name] == exp
                self.result.append('响应Json值验证成功！')
            except:
                self.result.append('响应Json值验证失败！预期{node}字段，值等于[{a}]，实际值等于 {b}'.format(
                    node=node_name, a=exp, b=j[node_name]
                ))
                self.flag += 1
        except:
            self.result.append('响应内容不是有效的Json格式')
            self.flag += 1

    def check_json_path_value(self, path, exp):
        node = self.json_value(path)
        if node is not None:
            try:
                assert node == exp
                self.result.append('响应Json值验证成功！')
            except:
                self.result.append('响应Json值验证失败！预期{path}字段，值等于[{a}]，实际值等于 {b}'.format(
                    path=path, a=exp, b=node
                ))
                self.flag += 1
        else:
            self.result.append('json节点{path}不存在'.format(path=path))
            self.flag += 1
