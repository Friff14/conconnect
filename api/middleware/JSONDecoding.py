import json

import falcon


class JSONDecoding:
    def process_request(self, req, resp):
        stream = req.stream
        body = stream.read().decode('utf-8')
        if body and not req.params:
            try:
                req.params.update(json.loads(body))
            except ValueError as e:
                raise falcon.HTTPBadRequest("JSON not valid.", "Please send a valid JSON object.")

    def process_response(self, req, resp, resource, req_succeeded):
        pass
        # print(req_succeeded)
        # if not req_succeeded:
        #     resp.body = "there was an error"
