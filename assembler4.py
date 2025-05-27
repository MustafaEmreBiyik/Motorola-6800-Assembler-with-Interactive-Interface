instruction_set = {
    'LDAA': '86',
    'STAA': '97',
    'LDAB': 'C6',
    'ADDA': '8B',
    'STAB': 'D7',
    'JMP':  '7E',
    'END':  None,
}

# Tek satır assembler (label bilgisi gerekli olabilir)
def assemble_line(line, labels=None, current_address=0):
    if labels is None:
        labels = {}

    line = line.strip()
    if not line or line.startswith(';'):
        return None

    if ':' in line:
        _, line = line.split(':', 1)
        line = line.strip()

    if not line or line.startswith('END'):
        return None

    parts = line.split()
    mnemonic = parts[0]
    operand = parts[1] if len(parts) > 1 else ''

    opcode = instruction_set.get(mnemonic)
    if not opcode:
        return f"HATA: Geçersiz komut -> {line}"

    if operand in labels:
        operand_value = f"${labels[operand]:02X}"
    else:
        operand_value = operand

    return f"{line:<20} => {opcode} {operand_value}"


# Tüm dosyayı işler
def assemble_file(file_path):
    with open(file_path, 'r') as f:
        assembly_lines = f.readlines()

    labels = {}
    address_counter = 0
    clean_lines = []

    # PASS 1 – Etiketleri bul
    for line in assembly_lines:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            label, rest = line.split(':', 1)
            labels[label.strip()] = address_counter
            line = rest.strip()
        if line and not line.startswith('END'):
            clean_lines.append((line, address_counter))
            address_counter += 2

    # PASS 2 – Kod üret
    result = []
    for line, addr in clean_lines:
        translated = assemble_line(line, labels, addr)
        if translated:
            result.append(translated)

    return result


# Doğrudan terminalden çalıştırıldığında
if __name__ == "__main__":
    output = assemble_file("example.asm")
    print("Assembly Code -> Object Code:")
    for line in output:
        print(line)
