def assemble_code(lines):
    labels = {}
    clean_lines = []
    pc = 0
    started = False

    # Instruction set with addressing mode hints
    instruction_set = {
        'LDAA': ('86', 'immediate'),
        'LDAB': ('C6', 'immediate'),
        'STAA': ('97', 'direct'),
        'STAB': ('D7', 'direct'),
        'ADDA': ('8B', 'immediate'),
        'JMP':  ('7E', 'extended'),
        'BRA':  ('20', 'relative'),
        'BNE':  ('26', 'relative'),
        'BEQ':  ('27', 'relative'),
        'END':  (None, None),
    }

    # PASS 1: Collect labels and ORG
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            continue

        if line.upper().startswith("ORG"):
            try:
                pc = int(line.split()[1].replace("$", ""), 16)
            except Exception:
                clean_lines.append((pc, f"HATA: Geçersiz ORG -> {line}"))
                continue
            continue

        if ':' in line:
            label, rest = line.split(':', 1)
            labels[label.strip()] = pc
            line = rest.strip()

        if line.upper().startswith("END"):
            break

        if line:
            clean_lines.append((pc, line))
            pc += 2  # Simplified size handling

    # PASS 2: Generate machine code
    result = []
    for addr, line in clean_lines:
        if line.startswith("HATA:"):
            result.append(line)
            continue

        parts = line.split()
        if not parts:
            continue

        mnemonic = parts[0].upper()
        operand = parts[1] if len(parts) > 1 else ""

        if mnemonic not in instruction_set:
            result.append(f"HATA: Geçersiz komut -> {line}")
            continue

        opcode, mode = instruction_set[mnemonic]

        # Immediate value
        if mode == 'immediate':
            if not operand.startswith('#'):
                result.append(f"HATA: {mnemonic} için '#' ile başlayan immediat değer bekleniyor -> {line}")
                continue
            operand_val = operand.replace('#', '').replace('$', '')

        # Direct or Extended Address
        elif mode in ['direct', 'extended']:
            if operand in labels:
                operand_val = f"{labels[operand]:02X}"
            elif operand.startswith('$'):
                operand_val = operand.replace('$', '')
            else:
                result.append(f"HATA: {mnemonic} için geçersiz adresleme -> {line}")
                continue

        # Relative branch
        elif mode == 'relative':
            if operand in labels:
                offset = labels[operand] - (addr + 2)
                if not -128 <= offset <= 127:
                    result.append(f"HATA: {mnemonic} için uzak hedef -> {line}")
                    continue
                operand_val = f"{offset & 0xFF:02X}"
            else:
                result.append(f"HATA: {mnemonic} için etiket bulunamadı -> {line}")
                continue
        else:
            operand_val = ''

        result.append(f"${addr:04X}: {opcode} {operand_val:<2}    {mnemonic} {operand}")

    return result
