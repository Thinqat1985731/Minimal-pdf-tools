# Standard Library
import os
import subprocess
from tkinter import (
    Button,
    Label,
    Radiobutton,
    StringVar,
    Tk,
    filedialog,
    messagebox,
)

# Third Party Library
from pypdf import PdfWriter
from send2trash import send2trash

dirname = os.path.dirname(__file__)
iDir = os.path.abspath(dirname)
root = Tk()
root.withdraw()


def merging(files_read):
    """
    結合の本体
    """
    pdf_file_merger = PdfWriter()
    for pdf in files_read:
        pdf_file_merger.append(pdf)

    file_name_save = filedialog.asksaveasfilename(
        title="結合したファイルを名前を付けて保存",
        filetypes=[("PDF file", "*.pdf")],
        initialdir=iDir,
    )

    if file_name_save.rfind(".pdf") == -1:
        file_name_save = file_name_save + ".pdf"
        # 右から検索して.pdfが無かったら勝手に付け足す

    pdf_file_merger.write(file_name_save)
    pdf_file_merger.close()  # writer を閉じる

    return file_name_save


def option(files_read, file_name_save):
    """
    結合後のオプション機能
    """
    delete = messagebox.askquestion(
        "Pdf-merger",
        "結合に使用したPDFをゴミ箱に移動しますか？",
    )

    if delete == "yes":
        for file_name in files_read:
            if file_name != file_name_save:  # 上書きの場合は本体を削除しない
                file_name_delete = file_name.replace("/", "\\")
                # send2trashで使われるget_short_path_name関数の仕様に合わせる
                send2trash(file_name_delete)

    compress = messagebox.askquestion(
        "Pdf-merger",
        "結合後のPDFを圧縮しますか？（GhostScriptが必要）",
    )

    if compress == "yes":
        root_s = Tk()
        root_s.geometry("250x240")
        root_s.title("pdf-merger")

        radio_var = StringVar(root_s)

        radio1 = Radiobutton(
            root_s, value="/default", variable=radio_var, text="/default"
        )
        radio1.pack()
        radio1.place(x=20, y=60)

        radio2 = Radiobutton(
            root_s, value="/screen", variable=radio_var, text="/screen"
        )
        radio2.pack()
        radio2.place(x=20, y=82)

        radio3 = Radiobutton(
            root_s, value="/ebook", variable=radio_var, text="/ebook"
        )
        radio3.pack()
        radio3.place(x=20, y=104)

        radio4 = Radiobutton(
            root_s, value="/printer", variable=radio_var, text="/printer"
        )
        radio4.pack()
        radio4.place(x=20, y=126)

        radio5 = Radiobutton(
            root_s, value="/prepress", variable=radio_var, text="/prepress"
        )
        radio5.pack()
        radio5.place(x=20, y=148)

        radio_var.set("/default")

        def btn_click():
            root_s.quit()
            root_s.destroy()

        label = Label(root_s, text="圧縮の設定を選んでください。")
        label.pack()
        label.place(x=20, y=10)

        button = Button(root_s, text="OK", command=btn_click)
        button.place(x=20, y=180)

        root_s.mainloop()

        file_name_temp = file_name_save.replace(".pdf", "_.pdf")
        subprocess.check_output(
            [
                "gswin64c",
                "-sDEVICE=pdfwrite",
                "-dPDFSETTINGS=%s" % (radio_var.get()),
                "-dBATCH",
                "-dNOPAUSE",
                "-dSAFER",
                "-sOUTPUTFILE=%s" % (file_name_temp,),
                file_name_save,
            ]
        )
        os.remove(file_name_save)
        os.rename(file_name_temp, file_name_save)

    messagebox.showinfo("Pdf-compressor", "処理が完了しました。")
    root.destroy()
    return