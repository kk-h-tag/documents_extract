from extract_fig_table import extract_img_table
import argparse
import json
import os

def main(pdf_path):
    _extract_img_table = extract_img_table()

    if not os.path.exists(pdf_path) :
        print('PDF 파일이 존재하지 않습니다.')
        exit(1)

    caption_, full_text_ = _extract_img_table.extraction(pdf_path=pdf_path)

    with open("./result/caption.json", "w") as json_file:
        json.dump(caption_, json_file, ensure_ascii=False)

    with open("./result/full_text.json", "w") as json_file:
        json.dump(full_text_, json_file, ensure_ascii=False)

if __name__ == '__main__':
    # 외부 변수 수용
    parser = argparse.ArgumentParser()

    # 각 변수 선언
    parser.add_argument(
        '-i',
        type=str,
        default='',
        help="학술문헌 원문 PDF 파일 경로"
    )
    # 외부 변수에 대한 파싱 처리
    FLAGS, unparsed = parser.parse_known_args()

    # 메인 함수 활용
    main(FLAGS.i)
