from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextLine
from pdfminer.layout import LTTextBoxHorizontal, LTFigure, LTTextBox
from pdfminer.pdfpage import PDFPage


class img_to_text:
    def __init__(self):
        self.layout_list = []

    def parse_layout(self, layout):
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextLine):
                tmp = (lt_obj.bbox[0], lt_obj.bbox[1], lt_obj.bbox[2], lt_obj.bbox[3], lt_obj)
                self.layout_list.append(tmp)
            elif isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                self.parse_layout(lt_obj)
            elif isinstance(lt_obj, LTFigure):
                self.parse_layout(lt_obj)  # Recursive

    def find_text(self, infile_, page_num, text_point, fshape):
        self.layout_list.clear()

        cn = ''

        frame_height = fshape[0]

        tp_x = text_point[0] / 2.778
        tp_y = (frame_height - text_point[3]) / 2.778
        tp_x2 = text_point[2] / 2.778
        tp_y2 = (frame_height - text_point[1]) / 2.778

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interperter = PDFPageInterpreter(rsrcmgr, device)

        for pn, page in enumerate(PDFPage.get_pages(infile_)):
            if pn + 1 != page_num: continue

            try:
                interperter.process_page(page)
                layout = device.get_result()

                for element in layout:
                    if isinstance(element, LTTextBoxHorizontal) or isinstance(element, LTFigure):
                        self.parse_layout(element)
                break

            except:
                continue

        for element in self.layout_list:

            if tp_x - 10 <= element[0] and tp_y - 10 <= element[1] and tp_x2 + 10 >= element[2] and tp_y2 + 10 >= \
                    element[3]:
                cn += element[4].get_text()

        return cn

    def find_near(self, infile_, page_num, fshape, detectron_list, now_rect, now_tag):

        fig_table_list = ['fig', 'table', '표', '그림']
        caption_type = ''
        result_tmp = []
        result_point = []
        result_tag = None
        caption_t = ''
        flag = False

        mid_x1 = ((now_rect[0] + abs((now_rect[0] - now_rect[2]) / 2)))
        mid_y1 = ((now_rect[1] + abs((now_rect[1] - now_rect[3]) / 2)))

        for data, tc in detectron_list:

            mid_x2 = (data[0] + abs((data[0] - data[2]) / 2))
            mid_y2 = (data[1] + abs((data[1] - data[3]) / 2))

            length = ((((mid_x1 - mid_x2) ** 2) + ((mid_y1 - mid_y2) ** 2)) ** 0.5)

            if length == 0:
                tmp = (data, 100000, tc)
                result_tmp.append(tmp)
                continue
            tmp = (data, abs(length), tc)
            result_tmp.append(tmp)

        result_tmp = sorted(result_tmp, key=lambda x: x[1])

        for data, near, tc in result_tmp[:3]:
            if flag: break
            if tc == 0 or tc == 1:
                text_ = self.find_text(infile_, page_num, data, fshape).strip()
                for ft_ in fig_table_list:
                    if ft_ in text_[:5].lower():
                        caption_t = text_
                        result_point = data
                        result_tag = tc
                        caption_type = ft_
                        flag = True
                        break

        if not len(result_point): result_point = now_rect
        if not result_tag: result_tag = now_tag

        return result_point, result_tag, caption_t, caption_type


class colum_set:
    def _contain_rect(self, rect):
        result = rect.copy()

        for tmp, c in rect:
            for tmp2, c2 in rect:
                if tmp in tmp2: continue
                if (tmp[1] < tmp2[1] and tmp[3] + 10 > tmp2[1]) and (tmp[1] < tmp2[3] and tmp[3] + 10 > tmp2[3]):
                    if tmp2 in result:
                        tmp_t = (tmp2, c2)
                        result.remove(tmp_t)

        return result

    def find_column(self, rect, now_shape):
        colum_1 = []
        colum_2 = []
        colum_2_left = []
        colum_2_right = []

        tmp_return = []

        h_frame_width = now_shape[1] / 2

        for r, c in rect:

            if (r[0] < h_frame_width and r[2] < h_frame_width) or (r[0] > h_frame_width and r[2] > h_frame_width):
                tmp = (r, c)
                colum_2.append(tmp)
            else:
                tmp = (r, c)
                colum_1.append(tmp)


        for r, c in colum_2:
            if r[0] < h_frame_width and r[2] < h_frame_width:
                tmp = (r, c)
                colum_2_left.append(tmp)
            elif r[0] > h_frame_width and r[2] > h_frame_width:
                tmp = (r, c)
                colum_2_right.append(tmp)
            else:
                tmp = (r, c)
                colum_1.append(tmp)

        if len(colum_2_left) and len(colum_2_right):
            colum_2_left = sorted(colum_2_left, key=lambda y: y[0][3])
            colum_2_right = sorted(colum_2_right, key=lambda y: y[0][3])

        colum_1 = sorted(colum_1, key=lambda y: y[0][3])

        colum_1 = self._contain_rect(colum_1).copy()
        colum_2_left = self._contain_rect(colum_2_left).copy()
        colum_2_right = self._contain_rect(colum_2_right).copy()

        tmp_return.extend(colum_2_left)
        tmp_return.extend(colum_2_right)
        result = tmp_return.copy()

        if len(colum_1) and len(tmp_return):
            insert_num = 0
            for c_1, c in colum_1:
                if tmp_return[0][0][1] >= c_1[1]:
                    tmp = (c_1, c)
                    result.insert(insert_num, tmp)
                    insert_num += 1
                    continue
                elif tmp_return[len(tmp_return) - 1][0][1] <= c_1[1]:
                    tmp = (c_1, c)
                    result.insert(len(result), tmp)
                    continue
                for i in range(0, len(result) - 1, 2):
                    if result[i][0][1] <= c_1[1] and result[i + 1][0][1] >= c_1[1]:
                        tmp = (c_1, c)
                        result.insert(i + 1, tmp)

        else:
            result.extend(colum_1)

        return result





