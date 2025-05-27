import tkinter as tk
from tkinter import scrolledtext, messagebox
from assembler import assemble_code

def translate_code():
    asm_code = asm_text.get("1.0", tk.END).strip()
    if not asm_code:
        messagebox.showwarning("Uyarı", "Lütfen assembly kodunu giriniz!")
        return

    lines = asm_code.split('\n')
    result = assemble_code(lines)

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(result))
    output_text.config(state=tk.DISABLED)

# Pencere oluştur
window = tk.Tk()
window.title("Motorola 6800 Assembler")

# Assembly kodu girişi
tk.Label(window, text="Assembly Kodu Girin:").pack()
asm_text = scrolledtext.ScrolledText(window, width=50, height=10)
asm_text.pack()

# Çevir butonu
translate_btn = tk.Button(window, text="Çevir", command=translate_code)
translate_btn.pack(pady=5)

# Makine kodu çıktısı
tk.Label(window, text="Makine Kodu Çıktısı:").pack()
output_text = scrolledtext.ScrolledText(window, width=50, height=10, state=tk.DISABLED)
output_text.pack()

window.mainloop()
