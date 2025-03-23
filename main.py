import tkinter as tk
from tkinter import filedialog, messagebox
from analysis.item_analysis import ItemAnalysis
import os

class EvalBeeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("EvalBee Item Analysis")
        self.geometry("400x300")
        self.configure(bg="#f4f4f4")

        # Title Label
        title_label = tk.Label(self, text="EvalBee Item Analysis", font=("Arial", 16, "bold"), bg="#f4f4f4")
        title_label.pack(pady=20)

        # Buttons
        self.import_button = tk.Button(self, text="Import File", command=self.import_file, font=("Arial", 12),
                                       bg="#3498db", fg="white", width=20, height=2, border=0)
        self.import_button.pack(pady=10)

        self.export_button = tk.Button(self, text="Export File", command=self.export_file, font=("Arial", 12),
                                       bg="#2ecc71", fg="white", width=20, height=2, border=0)
        self.export_button.pack(pady=10)

        self.open_button = tk.Button(self, text="Open Processed File", command=self.open_file, font=("Arial", 12),
                                     bg="#e74c3c", fg="white", width=20, height=2, border=0, state=tk.DISABLED)
        self.open_button.pack(pady=10)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if file_path:
            messagebox.showinfo("File Imported", f"Imported: {file_path}")
            self.input_path = file_path

    def export_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx *.xls")])
        if file_path:
            messagebox.showinfo("File Exported", f"Saved to: {file_path}")
            self.output_path = file_path
        
        try:
            item_analysis = ItemAnalysis(self.input_path, self.output_path)
            item_analysis.run_calculation(item_analysis.df)
            item_analysis.export()
            messagebox.showinfo("Success!", f"File saved at: {self.output_path}")
            self.open_button.config(state=tk.NORMAL)
        
        except Exception as e:
            messagebox.showerror("Error", e)
            
    def open_file(self):
        messagebox.showinfo("Open File", "Opening processed file...")
        os.startfile(self.output_path)


if __name__ == "__main__":
    app = EvalBeeApp()
    app.mainloop()
