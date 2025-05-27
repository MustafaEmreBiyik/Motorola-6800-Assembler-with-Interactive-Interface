import tkinter as tk
from tkinter import scrolledtext, messagebox

# Komut seti (hex opcode)
instruction_set = {
    'LDAA': '86',
    'STAA': '97',
    'LDAB': 'C6',
    'ADDA': '8B',
    'STAB': 'D7',
    'JMP':  '7E',
    'END':  None,
}

def assemble_line(line, label_addresses):
    line = line.strip()
    if not line or line.startswith(";"):  # Yorum veya boş satır
        return ""
    if ":" in line:
        # Etiket varsa sadece komut kısmını al
        _, line = line.split(":", 1)
    parts = line.strip().split()
    if not parts:
        return ""
    instr = parts[0].upper()
    operand = parts[1] if len(parts) > 1 else ""

    if instr not in instruction_set:
        return f"HATA: Geçersiz komut -> {instr}"

    opcode = instruction_set[instr]
    if opcode is None:  # END gibi pseudo-instruction
        return "END"

    # Operand bir label ise adresini al
    if operand in label_addresses:
        operand_value = label_addresses[operand]
    else:
        operand_value = operand

    return f"{instr} {operand_value} => {opcode} {operand_value}"

def assemble_file(assembly_code):
    lines = assembly_code.split('\n')

    # 1. Pass: Etiket adreslerini bul (her komut 2 byte)
    label_addresses = {}
    pc = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if ':' in line:
            label, _ = line.split(':', 1)
            label_addresses[label.strip()] = f"${pc:02X}"
        if line and not line.startswith(";") and not line.upper().startswith("END"):
            pc += 2

    # 2. Pass: Her satırı assembler'a ver, makine kodunu al
    result = []
    for line in lines:
        code = assemble_line(line, label_addresses)
        if code:
            result.append(code)
    return result


def translate_code():
    asm_code = asm_text.get("1.0", tk.END).strip()
    if not asm_code:
        messagebox.showwarning("Uyarı", "Lütfen assembly kodunu giriniz!")
        return

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)

    output_lines = assemble_file(asm_code)
    output_text.insert(tk.END, "\n".join(output_lines))

    output_text.config(state=tk.DISABLED)

# Pencere oluştur
window = tk.Tk()
window.title("Motorola 6800 Assembler")

tk.Label(window, text="Assembly Kodu Girin:").pack()
asm_text = scrolledtext.ScrolledText(window, width=50, height=10)
asm_text.pack()

translate_btn = tk.Button(window, text="Çevir", command=translate_code)
translate_btn.pack(pady=5)

tk.Label(window, text="Makine Kodu Çıktısı:").pack()
output_text = scrolledtext.ScrolledText(window, width=50, height=10, state=tk.DISABLED)
output_text.pack()

window.mainloop()
