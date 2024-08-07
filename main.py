import tkinter as tk
import utils.constants as const
from utils.utils import System
import os


class Window(tk.Tk):
    text_disabled_position = "1.0"
    si = System()
    home_folder = si.get_home()
    def __init__(self, *args, **kwargs):
        self.row = 1
        self.cwd = self.home_folder
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title(const.TITLE)
        self.geometry(const.RES)
        self.input_frame()

    def input_frame(self):
        self.textarea = tk.Text(self, borderwidth=0, highlightbackground=const.BG,
        bg=const.BG, fg=const.FG, insertbackground=const.FG, insertwidth=4)
        self.focus_force()
        self.textarea.pack(expand=True, fill=tk.BOTH)
        self.new_line_input()
        self.textarea.bind("<BackSpace>", self.on_backspace)

    def on_backspace(self, event):
        pos = self.textarea.index(tk.INSERT).split(".")
        row = int(pos[0])
        column = int(pos[1])
        pos_disabled = self.text_disabled_position.split(".")
        row_disabled = int(pos_disabled[0])
        column_disabled = int(pos_disabled[1])
        if row < row_disabled or (row == row_disabled and column <= column_disabled):
            return "break"

    def new_line_input(self):
        display_text = self.get_display_text()
        self.len_display_text = len(display_text)
        self.textarea.insert(f"{self.row}.0", display_text + "\t\t")
        self.text_disabled_position = self.textarea.index("end-1c")
        self.text_disabled_position = self.textarea.index("end-1c")
        self.textarea.tag_add("prompt", f"{self.row}.0", f"{self.row}.{self.len_display_text}")
        self.textarea.tag_config("prompt", font=const.FONT_BOLD)
        self.textarea.bind("<Return>", self.run_command)

    def get_display_text(self):
        symbol = "#" if self.si.is_admin() else "$"
        if self.cwd.startswith(self.home_folder):
            cwd_display = self.cwd[0:len(self.home_folder)+1].replace(self.home_folder, "~") + self.cwd[len(self.home_folder)+1::]
        else:
            cwd_display = self.cwd
        return self.si.get_username() + "@" + self.si.get_hostname() + ":" + cwd_display + symbol
    
    def run_command(self, event):
        command = self.textarea.get(f"{self.row}.{self.len_display_text + 2}", "end-1c").split()
        if command[0] == "clear":
            self.textarea.delete("1.0", tk.END)
            self.row = 1
        elif command[0] == "cd":
            path = os.path.expanduser(command[1])
            self.cwd = self.si.run_cd(path)
            self.textarea.insert(tk.END, '\n')
            self.row += 1
        elif command[0] == "quit" or command[0] == "exit":
            self.destroy()
        else:
            output = self.si.run(command) 
            self.textarea.insert(tk.END, '\n'+output)
            self.row += len(output.split('\n'))
        self.text_disabled_position = self.textarea.index("end-1c")
        self.new_line_input()
        self.textarea.see(tk.END)
        return "break"

if __name__ == '__main__':
    app = Window()
    os.chdir(app.cwd)
    app.mainloop()
