# Chèn ảnh vào file excel để kiểm tra dữ liệu nhận dạng sắc phong

## Các cài đặt
1. Cài đặt môi trường
```sh
pip install -r requirements.txt
```

2. Cài thêm cái thư viện nếu có báo lỗi :v

## Cách chạy
1. Thay thế đường dẫn trong 3 biến:
    - `PATH_TEXT`: Đường dẫn để file .txt chứa dữ liệu đã gán nhãn nhận dạng.
    - `PATH_IMG`: Đường dẫn đến thư mục chứa ảnh.
    - `PATH_EXCEL`: Đường dẫn đến Excel để lưu kết quả lại
2. Thay đổi đường dẫn đến môi trường (nếu có). Nếu bạn chạy không cần môi trường ảo. Hãy đóng bình luận (#comment) và dòng `source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate` để tránh xảy ra lỗi.

## Todo:
1. Tăng kích thước của hình ảnh lên nếu quá nhỏ. (Resize)
2. Code để lấy độ dài văn bản sau khi tăng kích thước chữ.
3. Code để tách 100 ảnh vào 1 sheet name.
4. Nhờ Phúc chia ra 5 file cần thiết để chạy.
5. Chuyển giao code (nếu cần).

