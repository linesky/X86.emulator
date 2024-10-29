import sys

# Definição de uma memória de 64k
MEM_SIZE = 0x10002
memory = [0] * MEM_SIZE

# Registos
registers = {
    "ax": 0,
    "bx": 0,
    "cx": 0,
    "dx": 0,
    "sp":0xffff,
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
    0x68: "push 0x1000",
    0x58: "pop ax",
    0x5b: "pop bx",
    0x59: "pop cx",
    0x5a: "pop dx",
    0x50: "push ax",
    0x53: "push bx",
    0x51: "push cx",
    0x52: "push dx",
    0x89: "mov ax,bx",
    0xC3: "ret"
}

# Função para exibir o estado atual dos registradores
def print_state(instruction):
    print(f"IP: {registers['ip']:04X} | SP: {registers['sp']:04X} | AX: {registers['ax']:04X} | BX: {registers['bx']:04X} \n CX: {registers['cx']:04X} | DX: {registers['dx']:04X} | Executando: {instruction}")

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
        elif opcode == 0xf7:
            if (memory[registers['ip'] + 1])==0xe0:
            
                registers['ax'] =registers['ax'] * registers['ax']
                registers['ax'] =  registers['ax'] & 0xffff
                
                print_state(f"mul ax")
                registers['ip'] += 2
            elif (memory[registers['ip'] + 1])==0xe3:
            
                registers['ax'] =registers['ax'] * registers['bx']
                registers['ax'] =  registers['ax'] & 0xffff
                
                print_state(f"mul bx")
                registers['ip'] += 2
            elif (memory[registers['ip'] + 1])==0xe1:
            
                registers['ax'] =registers['ax'] * registers['cx']
                registers['ax'] =  registers['ax'] & 0xffff
                
                print_state(f"mul cx")
                registers['ip'] += 2
            elif (memory[registers['ip'] + 1])==0xe2:
            
                registers['ax'] =registers['ax'] * registers['dx']
                registers['ax'] =  registers['ax'] & 0xffff
                
                print_state(f"mul dx")
                registers['ip'] += 2
        elif opcode == 0x68:
            value = memory[registers['ip'] + 1] + (memory[registers['ip'] + 2] << 8)
            memory[registers['sp'] -1]=memory[registers['ip'] + 1]
            memory[registers['sp'] -0]=memory[registers['ip'] + 2]
            
            registers['sp'] -= 2
            
            print_state("push "+hex(value))
            
            registers['ip'] += 3
        elif opcode == 0x58:
            
            value = memory[registers['sp'] +1] + (memory[registers['sp'] + 2] << 8)
            
            registers['ax']=value
            
            
            registers['sp'] += 2
            print_state("pop ax")
            registers['ip'] += 1
        elif opcode == 0x5b:
            
            value = memory[registers['sp'] +1] + (memory[registers['sp'] + 2] << 8)
            
            registers['bx']=value
            
            
            registers['sp'] += 2
            print_state("pop bx")
            registers['ip'] += 1
        elif opcode == 0x59:
            
            value = memory[registers['sp'] +1] + (memory[registers['sp'] + 2] << 8)
            
            registers['cx']=value
            
            
            registers['sp'] += 2
            print_state("pop cx")
            registers['ip'] += 1
        elif opcode == 0x5a:
            
            value = memory[registers['sp'] +1] + (memory[registers['sp'] + 2] << 8)
            
            registers['dx']=value
            
            
            registers['sp'] += 2
            print_state("pop dx")
            registers['ip'] += 1
        elif opcode == 0x50:
            
            memory[registers['sp'] -1]=registers['ax'] & 0xff
            memory[registers['sp'] -0]=registers['ax']>>8 & 0xff
            
            registers['sp'] -= 2
            
            print_state("push ax")
            
            registers['ip'] += 1
        elif opcode == 0x53:
           
            memory[registers['sp'] -1]=registers['bx'] & 0xff
            memory[registers['sp'] -0]=registers['bx']>>8 & 0xff
            
            registers['sp'] -= 2
            
            print_state("push bx")
            
            registers['ip'] += 1
        elif opcode == 0x51:
           
            memory[registers['sp'] -1]=registers['cx'] & 0xff
            memory[registers['sp'] -0]=registers['cx']>>8 & 0xff
            
            registers['sp'] -= 2
            
            print_state("push cx")
            
            registers['ip'] += 1
        elif opcode == 0x52:
           
            memory[registers['sp'] -1]=registers['dx'] & 0xff
            memory[registers['sp'] -0]=registers['dx']>>8 & 0xff
            
            registers['sp'] -= 2
            
            print_state("push dx")
            
            registers['ip'] += 1
        elif opcode ==0x89:
            
            if memory[registers['ip'] + 1] == 0xc0:
                registers['ax'] = registers['ax']
                print_state(f"mov ax,ax")
            elif memory[registers['ip'] + 1] == 0xd8:
                
                registers['ax'] = registers['bx']
                print_state(f"mov ax,bx")
            elif memory[registers['ip'] + 1] == 0xc8:
                registers['ax'] = registers['cx']
                print_state(f"mov ax,cx")
            elif memory[registers['ip'] + 1] == 0xd0:
                registers['ax'] = registers['dx']
                print_state(f"mov ax,dx")
            elif memory[registers['ip'] + 1] == 0xc3:
                registers['bx'] = registers['ax']
                print_state(f"mov bx,ax")
            elif memory[registers['ip'] + 1] == 0xdb:
                
                registers['bx'] = registers['bx']
                print_state(f"mov bx,bx")
            elif memory[registers['ip'] + 1] == 0xcb:
                registers['bx'] = registers['cx']
                print_state(f"mov bx,cx")
            elif memory[registers['ip'] + 1] == 0xd3:
                registers['bx'] = registers['dx']
                print_state(f"mov bx,dx")
            elif memory[registers['ip'] + 1] == 0xc1:
                registers['cx'] = registers['ax']
                print_state(f"mov cx,ax")
            elif memory[registers['ip'] + 1] == 0xd9:
                
                registers['cx'] = registers['bx']
                print_state(f"mov cx,bx")
            elif memory[registers['ip'] + 1] == 0xc9:
                registers['cx'] = registers['cx']
                print_state(f"mov cx,cx")
            elif memory[registers['ip'] + 1] == 0xd1:
                registers['cx'] = registers['dx']
                print_state(f"mov cx,dx")
            elif memory[registers['ip'] + 1] == 0xc2:
                registers['dx'] = registers['ax']
                print_state(f"mov dx,ax")
            elif memory[registers['ip'] + 1] == 0xda:
                
                registers['dx'] = registers['bx']
                print_state(f"mov dx,bx")
            elif memory[registers['ip'] + 1] == 0xca:
                registers['dx'] = registers['cx']
                print_state(f"mov dx,cx")
            elif memory[registers['ip'] + 1] == 0xd2:
                registers['dx'] = registers['dx']
                print_state(f"mov dx,dx")
            elif memory[registers['ip'] + 1] == 0xe0:
                registers['ax'] = registers['sp']
                print_state(f"mov ax,sp")
            elif memory[registers['ip'] + 1] == 0xe3:
                
                registers['bx'] = registers['sp']
                print_state(f"mov bx,sp")
            elif memory[registers['ip'] + 1] == 0xe1:
                registers['cx'] = registers['sp']
                print_state(f"mov cx,sp")
            elif memory[registers['ip'] + 1] == 0xe2:
                registers['dx'] = registers['sp']
                print_state(f"mov dx,sp")
            registers['ip'] += 2
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
