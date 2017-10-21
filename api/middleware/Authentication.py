class Authentication:
    def process_request(self, req, resp):
        if 'AUTHORIZATION' in req.headers:
            auth_header = req.headers['AUTHORIZATION'].split()
            if auth_header[0] == 'Bearer' and len(auth_header) > 1:
                req.context['token'] = str(auth_header[1])

    def process_response(self, req, resp, resource, req_succeeded):
        pass
