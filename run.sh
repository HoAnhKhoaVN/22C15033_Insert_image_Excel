#####################################
########## START CHANGE CODE ########
#####################################
# PATH_TEXT='D:\\Master\\OCR_Nom\\fulllow_ocr_temple\\dataset\\final_data\\decree\\hannom\\reg_han_nom_10_anh\\sac\\rec_gt_demo.txt'
# PATH_IMG='D:\\Master\\OCR_Nom\\fulllow_ocr_temple\\dataset\\final_data\\decree\\hannom\\reg_han_nom_10_anh\\sac\\img'
# PATH_EXCEL='/d/Master/OCR_Nom/experiments/insert_img/output/demo_2.xlsx'

PATH_TEXT='input/demo_v4.txt'
PATH_IMG='D:\Master\OCR_Nom\fulllow_ocr_temple\dataset\final_data\decree\v3\data_sac_phong_reg_v3\reg_v4\img'
PATH_EXCEL='output/demo_v4.xlsx'

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
python main.py --path_text $PATH_TEXT \
               --path_img $PATH_IMG \
               --path_excel $PATH_EXCEL

echo Save successfully to $PATH_EXCEL !!!!
echo "########## THE END ############"