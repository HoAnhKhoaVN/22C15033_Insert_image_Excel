import os
from typing import List, Text, Tuple
from openpyxl.drawing.image import Image
from PIL import ImageFont, ImageDraw
import PIL.Image
import numpy as np
import math
from .config import (
    FONT_PATH,
    FD_DRAW_TEXT,
    PADDING_IMG
)

class DrawText:
    def __init__(
        self,
        text: Text,
        path: Text,
        height: int,
        width: int,
    )->None:
        self.text = text
        self.height = height
        self.width = width
        self.path = path
        self.image = PIL.Image.new(
            mode = "RGB",
            size=(self.width, self.height),
            color='white'
        )

    @staticmethod
    def get_para_in_line(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        a = (y1-y2)/(x1-x2-1e-9)
        b = y1-a*x1

        return a, b
    
    @staticmethod
    def get_point_in_line_y_axis(
        len_text: int,
        a_line: float,
        b_line: float,
        size : float,
        first_point: List,
        padding : int = 3
    )->List:
        kc = size // len_text
        _first_point = [
            first_point[0], #x
            first_point[1]+ padding, #y
        ]
        res = [_first_point]
        point = first_point
        for _ in range(len_text-1):
            _ , y = point

            res_y = int(y + kc)
            _res_y = int(y + kc) - padding

            if int(abs(a_line)) == 0:
                res_x = 0
            else:
                res_x = int((_res_y - b_line)//a_line)

            res_point  = [res_x, res_y]
            _res_point  = [res_x, _res_y]

            res.append(_res_point)
            point = res_point
        return res

    @staticmethod
    def get_text_dimensions(
        text_string: str,
        font: ImageFont
        ):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)
    

    def get_center_point(
        self,
        bbox: list,
        text_str: str,
        font: ImageFont,
    )-> List:
        _tl, _tr, _br, _bl = bbox
        a, b = self.get_para_in_line(_tl, _br)
        _a, _b = self.get_para_in_line(_tr, _bl)

        x_center = int((_b-b)//(a - _a))
        y_center = int(a*x_center + b)


        #region get text size
        text_size = self.get_text_dimensions(
            text_string= text_str,
            font= font
        )
        #endregion

        # region get position
        x_center -= text_size[0]//2
        y_center -= text_size[1]//2

        # endregion

        return [x_center , y_center], text_size
    
    @staticmethod
    def euclidean_distance(
        a : list,
        b : list
    )-> float:
        """Calculates the Euclidean distance between two vectors.

        Args:
            a: A numpy array representing the first vector.
            b: A numpy array representing the second vector.

        Returns:
            A float representing the Euclidean distance between the two vectors.
        """
        a =  np.array(a)
        b =  np.array(b)
        return np.sqrt(np.sum((a - b)**2))

    @staticmethod
    def get_rotated_text_size(
        text_size: List,
        angle: float
    )-> List:
        W, H = text_size
        radian_angle = math.radians(angle)
        tan_a = math.tan(radian_angle)
        w_1 = (H*tan_a - W)/(tan_a**2 - 1)
        w_2 = W - w_1
        h_1 = w_1 * tan_a
        h_2 = H - h_1
        X = np.sqrt(w_1**2 + h_1**2)
        Y = np.sqrt(w_2**2 + h_2**2)
        return X, Y
    
    def check_text_size(
        self,
        text_string: Text,
        bbox: List,
        angle: float,
        font_path: Text = FONT_PATH
    )-> Tuple:
        # region get height and width of bounding box
        tl, tr, br, bl = bbox
        width = self.euclidean_distance(tl, tr)
        height = self.euclidean_distance(tl, bl)
        # endregion
        font_size = 10
        while True:
            pil_font = ImageFont.truetype(font_path, font_size)
            text_size = self.get_text_dimensions(
                    text_string= text_string,
                    font= pil_font
                )
            # region Mapping rotated image
            rotated_text_width, rotated_text_height = self.get_rotated_text_size(
                text_size= text_size,
                angle = angle
            )

            # endregion

            width_x = (width - rotated_text_width ) // 2 # mở rộng kích thước ra xíu -> Để lúc nào cũng vẽ đủ chữ
            height_y = (height - rotated_text_height) // 2

            if width_x < 0 or height_y < 0:
                # Return font size before
                pil_font = ImageFont.truetype(font_path, font_size - 1)
                text_size = self.get_text_dimensions(
                        text_string= text_string,
                        font= pil_font
                    )
                return font_size
            else:
                font_size+=1
    
    def draw_text_vertical(
        self,
        fg_color: Tuple =(0,0,0),
        bg_color: Tuple = (255,255,255),
        font_path : Text = FONT_PATH,
    ):
        tl, tr, br, bl = (0,0), (self.width, 0), (self.width, self.height), (0, self.height)
        # region 1: Xác định bbox cho mỗi chữ trong văn bản
        # region 1.1: Viết phương trình đường thẳng của top-left và bottom-left
        a_line_left, b_line_left = self.get_para_in_line(tl,bl)
        
        # endregion

        # region 1.2: Viết phương trình đường thẳng của top-right và bottom-right
        a_line_right, b_line_right = self.get_para_in_line(tr,br)

        # endregion
        # region 2: Tính toán trung điểm cho mỗi từ
        len_text  = len(list(self.text))

        # region 2.1: Lấy các điểm trên đường thẳng top-left và bottom-left
        lst_point_in_top_left = self.get_point_in_line_y_axis(
            len_text = len_text,
            a_line = a_line_left,
            b_line = b_line_left,
            size  = self.height,
            first_point = tl,
            padding= PADDING_IMG
        )

        lst_point_in_top_left.append(bl)
        # endregion

        # region 2.2: Lấy các điểm trên đường thẳng top-right và bottom-right
        lst_point_in_top_right = self.get_point_in_line_y_axis(
            len_text = len_text,
            a_line = a_line_right,
            b_line = b_line_right,
            size  = self.height,
            first_point = tr,
            padding= PADDING_IMG
            )
        lst_point_in_top_right.append(br)
        # endregion

        # region 2.3: Xác định bbox cho mỗi chữ
        lst_bbox = []
        for idx in range(len(lst_point_in_top_left)-1):
            tl = lst_point_in_top_left[idx]
            tr = lst_point_in_top_right[idx]
            br = lst_point_in_top_right[idx+1]
            bl = lst_point_in_top_left[idx+1]
            lst_bbox.append([tl, tr, br, bl])
        # print(f'lst_bbox: {lst_bbox}')
        # endregion

        # endregion

        # region 3: Tính toán kích thước của mỗi chữ
        lst_size = []
        for w, _bbox in zip(list(self.text), lst_bbox):
            font_size = self.check_text_size(
            text_string= w,
            bbox = _bbox,
            angle= 0,
            )
            lst_size.append(font_size)
        max_font_size = min(lst_size)
        # endregion

        # region 4: Viết và xoay chữ
        font = ImageFont.truetype( font_path , max_font_size)
        for w , _bbox in zip(list(self.text), lst_bbox):
            p_center, text_size = self.get_center_point(_bbox, w, font)

            w_text, h_text = text_size
            # region 4.1: Create temporary image
            tmp_img = PIL.Image.new(
                mode = 'RGB',
                size = (w_text, h_text),
                color = bg_color
            )
            # endregion

            # region 4.2: Draw text
            tmp_draw = ImageDraw.Draw(tmp_img)
            tmp_draw.text(
                xy= (0,0),
                text = w,
                align= 'center',
                font= font,
                fill= fg_color
            )
            

            # endregion

            # region 4.3: Rotate text
            tmp_img = tmp_img.rotate(
                angle= 0,
                expand= True,
                fillcolor= bg_color,
            )
            # endregion

            # region 4.4: Paste text
            self.image.paste(
                im = tmp_img,
                box= p_center
            )
        # endregion
        # endregion
        return self.image

    def __call__(self):
        image_pil = self.draw_text_vertical()

        name = os.path.basename(self.path)
        draw_text_path = os.path.join(FD_DRAW_TEXT, name)

        image_pil.save(
            fp = draw_text_path
        )

        return Image(draw_text_path)

if __name__ == '__main__':
    obj = DrawText(
        text= '天興運',
        path = 'test.jpg',
        height= 100,
        width= 40
    )

    obj()