import json

from conconnect.cc_data.tables import *


class TagCategoryController(object):
    def on_get(self, req, resp, tag_category_id=None):
        print("Tag Category ID", tag_category_id)
        db_session = req.context['session']
        tag_categories = db_session.query(TagCategory)
        if tag_category_id:
            tag_categories = tag_categories.filter(TagCategory.id == tag_category_id)
        ret = [tag_category.json() for tag_category in tag_categories]
        resp.body = json.dumps(ret)

    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
