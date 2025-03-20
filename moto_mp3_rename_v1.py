import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

# 変更ルール（ここを編集することで変更可能）
rename_rules = {
    "aaaa": "hoge",
    "bbbb": "fuga",
}

def rename_file(filepath):
    directory, filename = os.path.split(filepath)
    new_filename = filename
    for old, new in rename_rules.items():
        new_filename = new_filename.replace(old, new)

    if new_filename != filename:
        new_path = os.path.join(directory, new_filename)
        os.rename(filepath, new_path)
        print(f"Renamed: {filename} -> {new_filename}")

def rename_files_in_directory(directory):
    if not os.path.isdir(directory):
        messagebox.showerror("エラー", f"指定されたパスはフォルダではありません: {directory}")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            rename_file(filepath)
        elif os.path.isdir(filepath):
            rename_files_in_directory(filepath)
    messagebox.showinfo("完了", "フォルダ内のリネームが完了しました！")

def rename_mp3_file(filepath):
    if filepath.endswith(".mp3"):
        dirname, filename = os.path.split(filepath)
        match = re.match(r"(.*)_(\d{8})(\(\d+\))?\.mp3", filename)
        if match:
            date = match.group(2)
            optional_part = match.group(3) if match.group(3) else ""
            new_filename = f"{date}{optional_part}_{match.group(1)}.mp3"
            new_path = os.path.join(dirname, new_filename)
            os.rename(filepath, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

def rename_mp3_files_in_directory(directory):
    if not os.path.isdir(directory):
        messagebox.showerror("エラー", f"指定されたパスはフォルダではありません: {directory}")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith(".mp3"):
            rename_mp3_file(filepath)
        elif os.path.isdir(filepath):
            rename_mp3_files_in_directory(filepath)

def on_drop(event):
    files = root.tk.splitlist(event.data)
    for filepath in files:
        if os.path.isfile(filepath):
            if filepath.endswith(".mp3"):
                rename_mp3_file(filepath)
            else:
                rename_file(filepath)
        elif os.path.isdir(filepath):
            rename_files_in_directory(filepath)
            rename_mp3_files_in_directory(filepath)

def create_gui():
    global root
    try:
        root = TkinterDnD.Tk()
        root.title("リネームアプリ")
        root.geometry("400x200")  # ウィンドウサイズを設定

        # ドラッグ＆ドロップ用のラベル作成
        label = tk.Label(root, text="ここにファイルをドロップ", width=40, height=10, relief="ridge", bg="lightgray")
        label.pack(pady=20)
        label.drop_target_register(DND_FILES)
        label.dnd_bind('<<Drop>>', on_drop)

        root.mainloop()

    except ImportError:
        messagebox.showerror("エラー", "tkinterdnd2 パッケージが必要です。\nインストールしてください: pip install tkinterdnd2")

if __name__ == "__main__":
    create_gui()
