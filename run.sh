#####################################
########## START CHANGE CODE ########
#####################################
PATH_TEXT='input\phan_cong_5_ban\output_file_5.txt'
PATH_IMG='input\img'
PATH_EXCEL='output/output_file_5_no_space.xlsx'

# PATH_TEXT='input\demo_small_text.txt'
# PATH_IMG='input\img'
# PATH_EXCEL='output/output_file_demo.xlsx'

# Nếu có môi trường ảo, hãy chạy nó lên
source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate
####################################
########## END CHANGE CODE ########
####################################



FD_ROTATE=rotate_img
FD_DRAW_TEXT=draw_text

echo "########## Set up folder ############"
if [ ! -d $FD_ROTATE ]
then
    echo "Directory $FD_ROTATE DOES NOT exists!!!!" 
    mkdir -p $FD_ROTATE
else
    echo "Directory $FD_ROTATE exists. Detele all images in the directory!!!!" 
    rm $FD_ROTATE/*
fi

if [ ! -d $FD_DRAW_TEXT ]
then
    echo "Directory $FD_DRAW_TEXT DOES NOT exists!!!!" 
    mkdir -p $FD_DRAW_TEXT
else
    echo "Directory $FD_DRAW_TEXT exists. Detele all images in the directory!!!!!" 
    rm $FD_DRAW_TEXT/*
fi

echo "########## RUN CODE ############"
python main.py --path_text $PATH_TEXT --path_img $PATH_IMG --path_excel $PATH_EXCEL

echo Save successfully to $PATH_EXCEL !!!!
echo "########## THE END ############"