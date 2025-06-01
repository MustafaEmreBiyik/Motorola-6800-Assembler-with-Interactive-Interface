class CPU6800:
    def __init__(self):
        self.reset()

    def reset(self):
        self.memory = bytearray(0x10000)  # 64KB
        self.reg = {
            'A': 0,
            'B': 0,
            'X': 0,
            'PC': 0,
            'CCR': 0,
        }
        self.running = False

    def load_code(self, machine_lines):
        for line in machine_lines:
            if line.startswith("HATA") or not line.startswith("$"):
                continue
            parts = line.split(":")
            addr = int(parts[0].replace("$", ""), 16)
            opcode_parts = parts[1].strip().split()[0:2]  # e.g., ['86', '10']
            for i, byte in enumerate(opcode_parts):
                self.memory[addr + i] = int(byte, 16)
        self.reg['PC'] = self._find_start_address(machine_lines)

    def _find_start_address(self, lines):
        for line in lines:
            if line.startswith("$"):
                return int(line.split(":")[0].replace("$", ""), 16)
        return 0

    def step(self):
        pc = self.reg['PC']
        opcode = self.memory[pc]

        # Handle a few instructions (example subset)
        if opcode == 0x86:  # LDAA #imm
            self.reg['A'] = self.memory[pc + 1]
            self.reg['PC'] += 2

        elif opcode == 0xC6:  # LDAB #imm
            self.reg['B'] = self.memory[pc + 1]
            self.reg['PC'] += 2

        elif opcode == 0x8B:  # ADDA #imm
            self.reg['A'] = (self.reg['A'] + self.memory[pc + 1]) & 0xFF
            self.reg['PC'] += 2

        elif opcode == 0x97:  # STAA $addr
            addr = self.memory[pc + 1]
            self.memory[addr] = self.reg['A']
            self.reg['PC'] += 2

        elif opcode == 0xD7:  # STAB $addr
            addr = self.memory[pc + 1]
            self.memory[addr] = self.reg['B']
            self.reg['PC'] += 2

        elif opcode == 0x7E:  # JMP $addr
            addr = self.memory[pc + 1]
            self.reg['PC'] = addr

        else:
            print(f"HATA: Bilinmeyen opcode {opcode:02X} @ PC=${pc:04X}")
            self.running = False

    def get_registers(self):
        return {k: f"{v:02X}" for k, v in self.reg.items()}

    def get_memory_slice(self, start, size=16):
        return [f"{self.memory[start + i]:02X}" for i in range(size)]
