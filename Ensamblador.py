class Instruction:
    def __init__(self, mnemonic, dest='', comp='', jump=''):
        self.mnemonic = mnemonic
        self.dest = dest
        self.comp = comp
        self.jump = jump

    def translate(self):
        if self.mnemonic.startswith('@'):
            return self.translate_A_instruction()
        else:
            return self.translate_C_instruction()

    def translate_A_instruction(self):
        address = self.mnemonic[1:]
        address_binary = format(int(address), '015b')
        return '0' + address_binary.zfill(15)

    def translate_C_instruction(self):
        dest_binary = dest_table[self.dest].zfill(3)
        comp_binary = comp_table[self.comp].zfill(7)
        jump_binary = jump_table[self.jump].zfill(3) if self.jump else '000'
        return '111' + comp_binary + dest_binary + jump_binary

# Tablas de traducción
comp_table = {
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

dest_table = {
    '':    '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'A':   '100',
    'AM':  '101',
    'AD':  '110',
    'AMD': '111',
}

jump_table = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

def assemble(source_code, output_file):
    binary_code = []

    for line in source_code:
        if not line or line.startswith('//'):
            continue

        instruction = Instruction(*tokenize(line))
        binary_code.append(instruction.translate().zfill(16))

    with open(output_file, 'w') as f:
        for instruction_binary in binary_code:
            f.write(instruction_binary + '\n')

def tokenize(line):
    line = line.strip()
    if line.startswith('@'):
        return (line,)
    elif '=' in line:
        dest, rest = line.split('=')
        if ';' in rest:
            comp, jump = rest.split(';')
            return ('', dest, comp, jump)
        else:
            return ('', dest, rest)
    else:
        comp, jump = line.split(';')
        return ('', comp, jump)

# Código fuente de ejemplo
source_code = [
    '@2',    # Nueva instrucción
    'D=A',   # Nueva instrucción
    '@3',    # Nueva instrucción
    'D=D+A', # Nueva instrucción
    '@0',    # Nueva instrucción
    'M=D'    # Nueva instrucción
]

# Ensamblar el código fuente y guardar el resultado
assemble(source_code, 'traducido.hack')
