## Project Title
- Documents Figure Table Extraction.

## Project Abstract
- 논문 PDF에서 Figure, Table, Caption, 전문을 추출하기 위한 모듈입니다.
- 한글논문 기준이며 detectron_func/model/의 model을 영어논문에 맞는 PubLayNet과 같은 모델로 변경하시면 사용이 가능합니다.
- Figure, Table은 이미지의 형태로 저장이 되며, Caption은 각 Figure, Table에 맵핑이 되어 JSON으로 저장됩니다. 전문또한 JSON파일로 저장이 됩니다.

## Requirement
- opencv-python == 4.1.0.25
- tqdm == 4.35.0
- pdf2image == 1.12.1
- detectron2 == 0.1.3
- Pillow == 7.0.0
- pdfminer.six == 20181108
- easydict==1.9
- numpy==1.18.1


## 실행방법
- Git에서 코드를 clone.
- Requirement 있는 package 설치(detectron2는 https://detectron2.readthedocs.io/en/latest/tutorials/install.html 참고하여 설치)
- GPU의 메모리가 최소 12GB 이상 있어야함(pdf가 너무 클경우에 GPU 메모리에 따라 처리가 불가능 할 경우도 생김)
- 사용 방법은 아래 명령으로 사용가능 하고, pdf 경로는 절대 경로 혹은 상대 경로 모두 사용가능합니다.
```c
python main.py -i pdf_path
```
- 현재 코드는 input으로 하나의 PDF 파일만 입력이 가능하며 다중파일의 처리를 원할 경우 main.py의 def main을 수정하여 처리 가능.
- Figure와 Table은 result의 디렉터리에 저장이되며 caption과 full-text의 json 또한 result 디렉터리에 저장됨.

## Todo List
- main의 인자를 확인해 단일 파일 다중파일 관계 없이 실행 가능하도록 변경.
- 한글 논문 뿐 아니라 외국 논문까지 처리가 가능하도록 모델의 다양성 추가.
- Pdfminer에 의존하지 않고 OCR 모델을 추가하여 이미지 PDF도 처리가 가능하도록 추가.
- Mask-RCNN 모델보다 성능이 좋은 모델을 사용하여 학습 후 평가.

## Credit
- [Detectron2](https://github.com/facebookresearch/detectron2) Detectron2 프레임워크를 사용해 학습하였습니다.
- [PubLayNet](https://github.com/ibm-aur-nlp/PubLayNet) PubLayNet으로 Pretrained된 모델을 사용해 Fine-Tuning 하였습니다.
- [PDF-Miner](https://github.com/pdfminer/pdfminer.six) 모델을 통해 찾아진 영역을 Pdfminer를 통해 Text로 추출하였습니다.
