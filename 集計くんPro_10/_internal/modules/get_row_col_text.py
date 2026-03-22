import gradio as gr
from openpyxl.utils import get_column_letter

import modules.excel_utils_gui as eu

# セルの値を取り出す関数: これをC化すると動的な引数解析に失敗するので python のまま提供する
def get_row_col_text(evt: gr.SelectData, row_col_dropdown):
    # evt.value : クリックしたセルの値
    # evt.index : (行番号, 列番号) のタプル
    # print(f"(行番号, 列番号) :{evt.index}")   # pandas の(行番号, 列番号)
    if row_col_dropdown.endswith("キーワード項目行"):
        text_candidate = str(evt.index[0]+1) + "行"
    elif row_col_dropdown.endswith("キーワード項目列"):
         text_candidate = get_column_letter(evt.index[1]+1) + "列"
    else:
        # 改行文字を\n表記に変換
        formatted_cell = eu.normalize_string(repr(evt.value).replace("'", ""))
        # 行番号・列記号は None に設定
        text_candidate = formatted_cell

    return (
        None,
        gr.update(value=text_candidate),
        gr.update(interactive=True),
        gr.update(value=None)
    )
