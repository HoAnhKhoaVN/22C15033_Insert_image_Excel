import argparse

def get_cli():
    # region Input
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--path_text", required=True,
        help = "Path to .txt file for recognition.")
    
    ap.add_argument("-i", "--path_img", required=True,
        help="Path to .jpg file for recognition.")

    ap.add_argument("-e", "--path_excel", required=True,
        help="Output file (Excel).")
    
    args = vars(ap.parse_args())
    return args