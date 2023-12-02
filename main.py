import os
import shutil
from typing import Dict, Text
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import PIL.Image
from typing import Text
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from src.draw_text import DrawText
from src.config import (
    PADDING,
    FD_DRAW_TEXT,
    FD_ROTATE,
    LOG
)
from datetime import datetime
from src.cli import get_cli
from tqdm import tqdm


class InsertImageToExcel(object):
    def __init__(
        self,
        path_img: Text,
        path_text: Text,
        path_excel: Text
    )->None:
        self.path_img = path_img
        self.path_text = path_text
        self.path_excel = path_excel

        self.lst_img = os.listdir(path = self.path_img)
        self.data :Dict = self.read_data()


        # region create workspace for excel
        self.wb = Workbook()
        self.ws = self.wb.active
        # endregion


    def read_data(self):
        with open(self.path_text, 'r', encoding='utf-8') as f:
            data = f.readlines()
        
        data = dict(list(map(lambda x: x.strip().split('\t'), data)))

        return data
    
    @staticmethod
    def rotate_image(
        path: Text
    )->Image:
        _img = PIL.Image.open(path).rotate(-90, expand=True)
        h , w = _img.height, _img.width

        name = os.path.basename(path)
        rotate_path  = os.path.join(FD_ROTATE, name)
        _img.save(
            fp = rotate_path
        )
        return Image(rotate_path), h, w

    def write_img_text(
        self,
        img_name: Text,
        text: Text,
        idx: int
    )->None:
        cell_location_img = f'A{idx+PADDING}'
        cell_location_draw_text = f'B{idx+PADDING}'
        cell_location_text = f'C{idx+PADDING}'

        path = os.path.join(
            self.path_img,
            img_name
        )

        img_rotate, h, w = self.rotate_image(path)

        img_draw_text = DrawText(text, path, h, w)()

        self.ws.add_image(img_rotate , cell_location_img)
        self.ws.add_image(img_draw_text, cell_location_draw_text )
        self.ws[cell_location_text] = text
        
        # Điều chỉnh chiều cao của dòng để phù hợp với kích thước ảnh
        self.ws.row_dimensions[idx+PADDING].height = h

    def change_size_text(self):
        pass

    def adjust_location(self):
        pass
        
    def process(self):

        # region Get title
        self.ws['A1'] = 'SRC_IMG'
        self.ws['B1'] = 'TEXT_PRED'
        self.ws['C1'] = 'TEXT'
        

        # endregion
        for idx, (img_name, text) in tqdm(enumerate(self.data.items()), desc = 'Progress: '):
            try:
                self.write_img_text(
                    img_name,
                    text, 
                    idx
                )
            except Exception as e:
                day_time = datetime.now()
                curr_time = day_time.strftime('%Y%m%d')
                with open(f'{LOG}/{curr_time}.log', 'a', encoding='utf-8') as f:
                    f.write(f'{img_name}\t{text}\n')
                continue

        self.wb.save(self.path_excel)

if __name__ == '__main__':
    args = get_cli()

    PATH_TEXT = args['path_text']
    PATH_IMG = args['path_img']
    PATH_EXCEL = args['path_excel']

    obj = InsertImageToExcel(
        path_img= PATH_IMG,
        path_text= PATH_TEXT,
        path_excel= PATH_EXCEL
    )

    obj.process()