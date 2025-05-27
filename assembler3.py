instruction_set = {
    'LDAA': '86',
    'STAA': '97',
    'LDAB': 'C6',
    'ADDA': '8B',
    'STAB': 'D7',
    'JMP':  '7E',
    'END':  None,
}

def assemble_with_labels(assembly_lines):
    labels = {}
    address_counter = 0
    clean_lines = []

    # 1. PASS – Etiketleri topla
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
            address_counter += 2  # Her komut 2 byte

    # 2. PASS – Kod üret
    result = []
    for line, addr in clean_lines:
        parts = line.split()
        if len(parts) == 1 and parts[0] == 'END':
            break
        mnemonic = parts[0]
        operand = parts[1] if len(parts) > 1 else ''

        opcode = instruction_set.get(mnemonic)
        if not opcode:
            result.append(f"HATA: Geçersiz komut -> {line}")
            continue

        # Eğer operand bir label ise, adresini al
        if operand in labels:
            operand_value = f"${labels[operand]:02X}"
        else:
            operand_value = operand

        result.append(f"{line:<20} => {opcode} {operand_value}")
    
    return result


# Örnek kullanım
if __name__ == "__main__":
    with open("example.asm", "r") as f:
        lines = f.readlines()

    output = assemble_with_labels(lines)
    print("Assembly Code -> Object Code:")
    for line in output:
        print(line)
