import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from assembler import assemble_code

def translate_code():
    asm_code = asm_text.get("1.0", tk.END).strip()
    if not asm_code:
        messagebox.showwarning("Uyarı", "Lütfen assembly kodunu giriniz!")
        return

    lines = asm_code.split('\n')
    result = assemble_code(lines)

    # Clear previous table content
    for row in output_table.get_children():
        output_table.delete(row)

    # Populate table with new result
    for idx, line in enumerate(result):
        if line.startswith("HATA"):
            asm_part = line
            obj_part = ""
        else:
            parts = line.split("    ")
            obj_part = parts[0].strip()
            asm_part = parts[1].strip() if len(parts) > 1 else ""
        output_table.insert("", tk.END, values=(idx + 1, asm_part, obj_part))


# Pencere oluştur
window = tk.Tk()
window.title("Motorola 6800 Assembler")
window.geometry("700x500")

# Assembly kodu girişi
tk.Label(window, text="Assembly Kodu Girin:").pack()
asm_text = scrolledtext.ScrolledText(window, width=80, height=10)
asm_text.pack(pady=5)

# Çevir butonu
translate_btn = tk.Button(window, text="Çevir", command=translate_code)
translate_btn.pack(pady=5)

# Tablo başlıkları
tk.Label(window, text="Assembly ⇄ Makine Kodu Eşlemesi:").pack(pady=5)

# Treeview tablosu
columns = ("line", "assembly", "machine")
output_table = ttk.Treeview(window, columns=columns, show="headings", height=15)
output_table.heading("line", text="Satır")
output_table.heading("assembly", text="Assembly Kodu")
output_table.heading("machine", text="Makine Kodu")

# Sütun genişlikleri
output_table.column("line", width=50, anchor="center")
output_table.column("assembly", width=300)
output_table.column("machine", width=150)

output_table.pack(fill=tk.BOTH, expand=True, padx=10)

window.mainloop()
