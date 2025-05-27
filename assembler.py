instruction_set = {
    'LDAA': '86',
    'STAA': '97',
    'LDAB': 'C6',
    'ADDA': '8B',
    'STAB': 'D7',
    'JMP':  '7E',
    'END':  None,
}

def assemble_code(lines):
    labels = {}
    pc = 0
    clean_lines = []

    # PASS 1: Etiketleri topla
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if ':' in line:
            label, rest = line.split(':', 1)
            labels[label.strip()] = pc
            line = rest.strip()
        if line and not line.startswith("END"):
            clean_lines.append((pc, line))
            pc += 2  # Her komut 2 byte

    # PASS 2: Kod üret
    result = []
    for addr, line in clean_lines:
        parts = line.split()
        mnemonic = parts[0].upper()
        operand = parts[1] if len(parts) > 1 else ""

        opcode = instruction_set.get(mnemonic)
        if not opcode:
            result.append(f"HATA: Geçersiz komut -> {line}")
            continue

        # Operand etiket mi?
        if operand in labels:
            operand_val = f"{labels[operand]:02X}"
        elif operand.startswith("#") or operand.startswith("$"):
            operand_val = operand.replace("#", "").replace("$", "")
        else:
            operand_val = operand

        result.append(f"${addr:02X}: {opcode} {operand_val:<2}    {mnemonic} {operand}")
    
    return result
