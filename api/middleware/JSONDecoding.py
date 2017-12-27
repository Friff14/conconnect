import json

import falcon


class JSONDecoding:
    requested_individual = False

    def process_request(self, req, resp):
        stream = req.stream
        body = stream.read().decode('utf-8')
        if body and not req.params:
            try:
                req.params.update(json.loads(body))
            except ValueError as e:
                raise falcon.HTTPBadRequest("JSON not valid.", "Please send a valid JSON object.")

    def process_resource(self, req, resp, resource, params):
        print("Processing resource with params: ", params)
        req.context['requested_individual'] = len(params) > 0


    def process_response(self, req, resp, resource, req_succeeded):

        if req.context['requested_individual']:
            if resp.body:
                resp_obj = json.loads(resp.body)
                if type(resp_obj) is list:
                    if len(resp_obj) > 0:
                        resp.body = json.dumps(resp_obj[0])
                    else:
                        raise falcon.HTTPNotFound(
                            title="Not found",
                            description="The requested resource was not found. It either doesn't"
                                        "exist, or you're not authorized to see it. I'm sorry."
                        )
        # print(req_succeeded)
        # if not req_succeeded:
        #     resp.body = "there was an error"
