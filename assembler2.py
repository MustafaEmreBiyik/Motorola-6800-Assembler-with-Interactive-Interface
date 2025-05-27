# assembler.py

# Basit bir Motorola 6800 komut tablosu (örnek)
instruction_set = {
    'LDAA': '86',  # Load Accumulator A
    'LDAB': 'C6',  # Load Accumulator B
    'STAA': '97',  # Store Accumulator A
    'STAB': 'D7',  # Store Accumulator B
    'ADDA': '8B',  # Add to Accumulator A
    'SUBA': '80',  # Subtract from Accumulator A
    'JMP' : '7E',  # Jump
    'BRA' : '20',  # Branch Always
    'NOP' : '01',  # No Operation
    'END' : ''     # Pseudo-instruction
}

def assemble_line(line):
    parts = line.strip().split()
    if not parts:
        return '', ''
    
    label = ''
    if ':' in parts[0]:
        label = parts.pop(0).replace(':', '')

    mnemonic = parts[0].upper()
    operand = parts[1] if len(parts) > 1 else ''

    opcode = instruction_set.get(mnemonic, '??')
    return f"{mnemonic} {operand}", f"{opcode} {operand}"

def assemble_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    translation = []
    for line in lines:
        asm, obj = assemble_line(line)
        translation.append((asm, obj))
    return translation


if __name__ == '__main__':
    asm_file = 'example.asm'
    result = assemble_file(asm_file)

    print("Assembly Code -> Object Code:")
    for asm, obj in result:
        print(f"{asm:<20} => {obj}")
