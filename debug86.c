
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Definir tamanho da memória (64 KB)
#define MEM_SIZE 0x10000

// Definição dos registradores
uint16_t ax = 0, bx = 0, cx = 0, dx = 0;
uint16_t ip = 0x100; // Ponteiro de instrução começa em 0x100

// Memória de 64 KB
uint8_t memory[MEM_SIZE];

// Lista de opcodes válidos
enum opcodes {
    MOV_AX = 0xB8,
    MOV_BX = 0xBB,
    MOV_CX = 0xB9,
    MOV_DX = 0xBA,
    NOP = 0x90,
    ADD_AX = 0x05,
    ADDss = 0x81, // Opcodes simplificados
    
    RET = 0xC3
};

// Função para exibir o estado dos registradores
void print_state(const char* instruction,int i) {
    printf("IP: %04X | AX: %04X | BX: %04X | CX: %04X | DX: %04X | Executando: %s,%x\n", 
            ip, ax, bx, cx, dx, instruction,i);
}

// Função para carregar o programa na memória
void load_program(const char* filename) {
    FILE *file = fopen(filename, "rb");
    if (!file) {
        perror("Erro ao abrir o ficheiro");
        exit(1);
    }

    // Carregar programa a partir do endereço 0x100
    size_t bytes_read = fread(&memory[0x100], 1, MEM_SIZE - 0x100, file);
    fclose(file);

    if (bytes_read == 0) {
        fprintf(stderr, "Erro: ficheiro vazio ou leitura falhou\n");
        exit(1);
    }
}

// Emulador simples que processa instrução por instrução
void emulate() {
    while (1) {
        uint8_t opcode = memory[ip];

        if (opcode == RET) {
            print_state("ret",0);
            printf("Instrução 'ret' atingida. Saindo do programa.\n");
            break;
        }

        switch (opcode) {
            case MOV_AX: {
                uint16_t value = memory[ip + 1] | (memory[ip + 2] << 8);
                ax = value;
                print_state("mov ax",value);
                ip += 3;
                break;
            }
            case MOV_BX: {
                uint16_t value = memory[ip + 1] | (memory[ip + 2] << 8);
                bx = value;
                print_state("mov bx",value);
                ip += 3;
                break;
            }
            case MOV_CX: {
                uint16_t value = memory[ip + 1] | (memory[ip + 2] << 8);
                cx = value;
                print_state("mov cx",value);
                ip += 3;
                break;
            }
            case MOV_DX: {
                uint16_t value = memory[ip + 1] | (memory[ip + 2] << 8);
                dx = value;
                print_state("mov dx",value);
                ip += 3;
                break;
            }
            case ADD_AX: {
                uint16_t value = memory[ip + 1] | (memory[ip + 2] << 8);
                ax += value;
                print_state("add ax",value);
                ip += 3;
                break;
            }
            case ADDss: {
                switch (memory[ip + 1]){
                case  0xc3:{
                    uint16_t value = memory[ip + 2] | (memory[ip + 3] << 8);
                    bx += value;
                    print_state("add bx",value);
                    ip += 4;
                    break;
                }
                
            
                 case  0xc1: {
                    uint16_t value = memory[ip + 2] | (memory[ip + 3] << 8);
                    cx += value;
                    print_state("add cx",value);
                    ip += 4;
                    break;
                }
                case 0xc2:  {
                    uint16_t value = memory[ip + 2] | (memory[ip + 3] << 8);
                    dx += value;
                    print_state("add dx",value);
                    ip += 4;
                    break;
                }
                }
                break;

            }
            case NOP:
                print_state("nop",0);
                ip += 1;
                break;
            default:
                printf("Erro: Opcode desconhecido %02X em IP %04X\n", opcode, ip);
                exit(1);
        }

        // Espera o usuário pressionar Enter para continuar
        printf("Pressione Enter para continuar...\n");
        getchar();
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <ficheiro.com>\n", argv[0]);
        return 1;
    }

    // Carregar o programa para a memória
    load_program(argv[1]);

    // Iniciar a emulação
    emulate();

    return 0;
}
