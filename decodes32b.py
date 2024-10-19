import os
import subprocess

# Lista de registradores
registers = ["eax", "ebx", "ecx","edx", "esi", "edi","esp"]

# Lista de instruções
instructions = ["mov", "add", "sub", "and", "or","xor"]

# Valor para a operação
value = "0x10000000"

# Caminho dos arquivos temporários
asm_file = "/tmp/out.asm"
bin_file = "/tmp/out"
output_file = "out.txt"

# Limpar o arquivo de saída
with open(output_file, "w") as f:
    f.write("")

# Função para gerar o arquivo assembly, compilar e testar
def generate_assembly_and_test(instruction, register, value):
    # Gerar o conteúdo do arquivo .asm
    asm_content = f"org 0x100\n{instruction} {register},{value}\n"
    
    # Escrever o arquivo assembly
    with open(asm_file, "w") as asm:
        asm.write(asm_content)
    nasm_command = f'printf "{instruction} {register},{value} | " >> out.txt'
    nasm_result = subprocess.run(nasm_command, shell=True)
    # Executar o NASM e redirecionar saída para out.txt
    nasm_command = f"nasm {asm_file} -o {bin_file} >> {output_file} 2>&1"
    nasm_result = subprocess.run(nasm_command, shell=True)

    # Verificar se houve erro no NASM
    if nasm_result.returncode == 0:
        # Se compilou corretamente, gerar o hexdump do binário com xxd
        xxd_command = f"xxd {bin_file} >> {output_file}"
        subprocess.run(xxd_command, shell=True)
    else:
        # Escrever no arquivo que houve um erro
        with open(output_file, "a") as f:
            f.write(f"\nErro ao compilar {instruction} {register},{value}\n")

# Testar todas as combinações de instruções e registradores
for instruction in instructions:
    for register in registers:
        for register2 in registers:
            print(instruction+" "+register+","+register2)
            generate_assembly_and_test(instruction, register,register2)

# Abrir o arquivo final com gedit
subprocess.run(f"gedit {output_file}", shell=True)

