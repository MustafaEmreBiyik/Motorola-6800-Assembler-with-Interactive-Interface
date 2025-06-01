import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from assembler import assemble_code
from simulator import CPU6800


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
def launch_simulator():
    asm_code = asm_text.get("1.0", tk.END).strip()
    if not asm_code:
        messagebox.showwarning("Uyarı", "Önce kodu girin ve çevirin.")
        return

    lines = asm_code.split('\n')
    machine = assemble_code(lines)

    sim = CPU6800()
    sim.load_code(machine)

    sim_window = tk.Toplevel(window)
    sim_window.title("6800 Simulator")
    sim_window.geometry("400x300")

    reg_labels = {}
    tk.Label(sim_window, text="Kayıtlar (Registers):").pack()

    frame = tk.Frame(sim_window)
    frame.pack()

    for i, reg in enumerate(['A', 'B', 'X', 'PC', 'CCR']):
        tk.Label(frame, text=f"{reg}:").grid(row=0, column=2*i)
        reg_labels[reg] = tk.Label(frame, text="00")
        reg_labels[reg].grid(row=0, column=2*i + 1)

    def update_ui():
        regs = sim.get_registers()
        for k in reg_labels:
            reg_labels[k].config(text=regs[k])

    def step_cpu():
        sim.step()
        update_ui()

    tk.Button(sim_window, text="Adım (Step)", command=step_cpu).pack(pady=10)
    update_ui()


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

sim_btn = tk.Button(window, text="Simülasyonu Başlat", command=launch_simulator)
sim_btn.pack(pady=5)

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
