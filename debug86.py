import sys

# Definição de uma memória de 64k
MEM_SIZE = 0x10000
memory = [0] * MEM_SIZE

# Registos
registers = {
    "ax": 0,
    "bx": 0,
    "cx": 0,
    "dx": 0,
    "ip": 0x100  # Início do código em 0x100
}

# Lista de opcodes permitidos
valid_opcodes = {
    0xB8: "mov ax,",
    0xBB: "mov bx,",
    0xB9: "mov cx,",
    0xBA: "mov dx,",
    0x90: "nop",
    0x05: "add ax,",
    0x81: "add bx,",  # Note: normally `add` would use 03h, but simplifying for example
    0x2d: "sub ax,",  
    0xf7: "add dx,", 
    0xC3: "ret"
}

# Função para exibir o estado atual dos registradores
def print_state(instruction):
    print(f"IP: {registers['ip']:04X} | AX: {registers['ax']:04X} | BX: {registers['bx']:04X} | CX: {registers['cx']:04X} | DX: {registers['dx']:04X} | Executando: {instruction}")

# Função para carregar o programa na memória
def load_program(file_name):
    with open(file_name, "rb") as f:
        program = f.read()
    # Carregar programa na memória a partir do endereço 0x100
    for i, byte in enumerate(program):
        memory[0x100 + i] = byte

# Emulador simples que processa instrução por instrução
def emulate():
    while True:
        opcode=memory[registers['ip']]
        
        if opcode not in valid_opcodes:
            print(f"Erro: Opcode desconhecido {opcode:02X} em IP {registers['ip']:04X}")
            break

        if opcode == 0xC3:  # ret
            print_state("ret")
            print("Instrução 'ret' atingida. Saindo do programa.")
            break

        # MOV AX, BX, CX, DX
        if opcode in (0xB8, 0xBB, 0xB9, 0xBA):
            value = memory[registers['ip'] + 1] + (memory[registers['ip'] + 2] << 8)
            if opcode == 0xB8:
                registers['ax'] = value
                print_state(f"mov ax, {value:04X}")
            elif opcode == 0xBB:
                
                registers['bx'] = value
                print_state(f"mov bx, {value:04X}")
            elif opcode == 0xB9:
                registers['cx'] = value
                print_state(f"mov cx, {value:04X}")
            elif opcode == 0xBA:
                registers['dx'] = value
                print_state(f"mov dx, {value:04X}")
            registers['ip'] += 3
        
        # ADD AX, BX, CX, DX
        elif opcode in (0x05, 0x81):
            value = memory[registers['ip'] + 1] + (memory[registers['ip'] + 2] << 8)
            if opcode == 0x05:
                registers['ax'] += value
                print_state(f"add ax, {value:04X}")
                registers['ip'] += 3
            elif opcode == 0x81:
                if memory[registers['ip']+1] == 0xc3:
                    value = memory[registers['ip'] + 2] + (memory[registers['ip'] + 3] << 8)
                    registers['bx'] += value
                    
                    print_state(f"add bx, {value:04X}")
                    registers['ip'] += 4
                elif  memory[registers['ip']+1] == 0xc1:
                    value = memory[registers['ip'] + 2] + (memory[registers['ip'] + 3] << 8)
                    registers['cx'] += value
                    print_state(f"add cx, {value:04X}")
                    registers['ip'] += 4
                elif memory[registers['ip']+1] == 0xc2:
                    value = memory[registers['ip'] + 2] + (memory[registers['ip'] + 3] << 8)
                    registers['dx'] += value
                    print_state(f"add dx, {value:04X}")
                    registers['ip'] += 4
                elif memory[registers['ip']+1] == 0xeb:
                    value = memory[registers['ip'] + 2] + (memory[registers['ip'] + 3] << 8)
                    registers['bx'] -= value
                    print_state(f"sub bx, {value:04X}")
                    registers['ip'] += 4
                elif memory[registers['ip']+1] == 0xe9:
                    value = memory[registers['ip'] + 2] + (memory[registers['ip'] + 3] << 8)
                    registers['cx'] -= value
                    print_state(f"sub cx, {value:04X}")
                    registers['ip'] += 4
                elif memory[registers['ip']+1] == 0xea:
                    value = memory[registers['ip'] + 2] + (memory[registers['ip'] + 3] << 8)
                    registers['dx'] -= value
                    print_state(f"sub dx, {value:04X}")
                    registers['ip'] += 4
                
        elif opcode == 0x2d:
            value = memory[registers['ip'] + 1] + (memory[registers['ip'] + 2] << 8)
            registers['ax'] -= value
            print_state(f"sub ax, {value:04X}")
            registers['ip'] += 3
        elif opcode == 0xf7 and (memory[registers['ip'] + 1])==0xe0:
            
            registers['ax'] *= registers['ax']
            registers['ax'] =  registers['ax'] & 0xffff
            
            print_state(f"mul ax")
            registers['ip'] += 3
        # NOP
        elif opcode == 0x90:
            print_state("nop")
            registers['ip'] += 1

        # Espera o usuário pressionar Enter para continuar
        input("Pressione Enter para continuar...")

# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python emulador.py <ficheiro.com>")
        return

    file_name = sys.argv[1]

    # Carregar o programa para a memória
    load_program(file_name)

    # Iniciar a emulação
    emulate()

if __name__ == "__main__":
    main()
