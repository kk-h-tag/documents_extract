import json
class make_json:
    def __init__(self):
        self._image_list = { "image_list" : []}
        self._data ={
            "image_id" : "",
            "data_type" : "",
            "caption": {
                "index_1": "",
                "title_1": "",
                "index_2": "",
                "title_2": ""
            },
            "page" : "",
            "file_name": "",
            "doi" : "",
            "coordinate" : []
        }

        self._full_text = {"body" : []}
        self._data2 = {
            "Page" : "",
            "Content" : []
        }

    def caption_parsing(self, caption_list):

        for caption_data in caption_list:
            tmp_data = self._data.copy()
            tmp_caption = self._data["caption"].copy()

            tmp_data["image_id"] = caption_data[0]
            tmp_data["data_type"] = caption_data[1]
            tmp_caption["index_1"] = caption_data[2]
            tmp_caption["title_1"] = caption_data[3]
            tmp_caption["index_2"] = caption_data[4]
            tmp_caption["title_2"] = caption_data[5]
            tmp_data["caption"] = tmp_caption
            tmp_data["page"] = caption_data[6]
            tmp_data["file_name"] = caption_data[7]
            tmp_data["coordinate"] = caption_data[8]

            self._image_list['image_list'].append(tmp_data)

        return self._image_list


    def full_text_parsing(self, full_text_list):

        for c , i in enumerate(full_text_list):
            tmp_data = self._data2.copy()
            tmp_data["Page"] = c + 1
            tmp_data["Content"] = i

            self._full_text["body"].append(tmp_data)

        return self._full_text



