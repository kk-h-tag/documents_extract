from definition_func.def_func import *
from definition_func.make_json import *
from detectron_func.detectron_func import *
import shutil
from pdf2image import convert_from_path
import re

import cv2 as cv

class extract_img_table:
    def __init__(self):
        self.caption_list = ['fig', '그림', 'table', '표']
        self.img_to_text = img_to_text()
        self.colum_set = colum_set()
        self.make_json = make_json()
        self._detectron2 = detectron2_configuration()
        self._caption = []
        self._full_page = []


    def extraction(self, pdf_path):
        tmp_path = './tmp/'

        os.mkdir(tmp_path)

        trim_p = 1
        image_counter = 1

        infile = open(pdf_path, "rb")

        try:
            pages = convert_from_path(pdf_path)

            for page in pages:
                text_region = []
                caption_region = []
                detectron2_list = []
                page_text = ''
                page_caption = []

                filename = tmp_path + "_page_" + str(image_counter) + ".jpg"
                page.save(filename, "JPEG")

                self._detectron2.args['input'] = filename
                self._detectron2.args['output'] = tmp_path + "_detectron_" + str(image_counter) + '.jpg'

                point_tmp, tag_tmp, = self._detectron2.main()

                for p, t in zip(point_tmp, tag_tmp):
                    tmp = (p, t)
                    detectron2_list.append(tmp)

                frame = cv.imread(filename)
                detectron2_list = self.colum_set.find_column(detectron2_list, frame.shape)


                for p, c, in detectron2_list:
                    width_alpha = 0
                    caption_index = ""
                    cpation_title = ""
                    caption_index2 = ""
                    cpation_title2= ""
                    image_id = ""
                    data_type = ""

                    if c == 3 or c == 4:
                        near_p, near_tc, caption_name, caption_type = self.img_to_text.find_near(infile, image_counter, frame.shape, detectron2_list, p, c)
                        tmp_cr = (near_p.tolist(), near_tc)
                        caption_region.append(tmp_cr)

                        if caption_name :
                            str_i = int(re.findall('\d+', caption_name)[0])
                            index_num = caption_name.find(str(str_i))
                            caption_index = caption_name[:index_num + 2]
                            cpation_title = caption_name[index_num + 2:]

                        for i in self.caption_list:
                            if i in cpation_title.lower():
                                index_cap_title = cpation_title.lower().find(i)
                                tmp_caption2 = cpation_title[index_cap_title:]
                                cpation_title = cpation_title[:index_cap_title]

                                str_i = int(re.findall('\d+', tmp_caption2)[0])
                                index_num = tmp_caption2.find(str(str_i))
                                caption_index2 = tmp_caption2[:index_num + 2]
                                cpation_title2 = tmp_caption2[index_num + 2:]
                                break

                        if c == 4:
                            image_id = "f" + str(trim_p).zfill(3)
                            data_type = "FIGURE"

                        elif c == 3:
                            image_id = "t" + str(trim_p).zfill(3)
                            data_type = "TABLE"

                        caption_file_name = pdf_path.split('/')[-1].replace('.pdf', image_id + '.jpg')

                        caption_tmp = (image_id, data_type, caption_index, cpation_title,caption_index2, cpation_title2, image_counter, caption_file_name, near_p.tolist())
                        page_caption.append(caption_tmp)
                        self._caption.append(caption_tmp)

                        trim_path = 'result/' + caption_file_name

                        if near_p[0] < p[0] - 10 or near_p[2] > p[0] + 10: width_alpha = abs(near_p[0] - p[0])

                        x = min(p[0], near_p[0])
                        y = min(p[1], near_p[1])
                        w = max(abs(p[0] - p[2]), abs(near_p[0] - near_p[2])) + width_alpha
                        h = abs(min(p[1], near_p[1]) - max(p[3], near_p[3]))

                        img_trim = frame[int(y):int(y + h), int(x):int(x + w)]
                        cv.imwrite(trim_path, img_trim)
                        trim_p += 1

                    elif c == 0 or c == 1 or c == 2:
                        tmp_tr = (p.tolist(), c)
                        text_region.append(tmp_tr)

                tmp = self.colum_set.find_column(text_region, frame.shape)

                for r, c in tmp:
                    flag = True
                    for i in page_caption:
                        if r in i:
                            page_text += str({
                                "image_id": i[0],
                                "caption": {
                                    "index_1": i[2],
                                    "title_1": i[3],
                                    "index_2": i[4],
                                    "title_2": i[5]
                                },
                                "file_name": i[7],
                            })
                            flag = False
                    if flag:
                        text_ = self.img_to_text.find_text(infile, image_counter, r, frame.shape)
                        page_text += text_.replace('\n', '')

                self._full_page.append(page_text)
                image_counter += 1

            caption_ = self.make_json.caption_parsing(self._caption)
            full_text_ = self.make_json.full_text_parsing(self._full_page)

            shutil.rmtree(tmp_path)
            return caption_, full_text_
        except Exception as e:
            print("Error : \t" + str(e))
            shutil.rmtree(tmp_path)