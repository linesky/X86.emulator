import os
import subprocess

# Lista de registradores
registers = ["ah","al", "bh","bl", "ch","cl", "dh","dl","ax", "bx", "cx","dx", "si", "di","sp", "[bx]", "[si]", "[di]","[sp]","bp","[bp]","[0x1000]","eax", "ebx", "ecx","edx", "esi", "edi","esp","[ebx]", "[esi]", "[edi]","[esp]","ebp","[ebp]","0x10000000"]

# Lista de instruções
instructions = ["int","inc","dec"]

# Valor para a operação
value = "0xff"

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
    asm_content = f"org 0x100\n{instruction} {register}\n"
    
    # Escrever o arquivo assembly
    with open(asm_file, "w") as asm:
        asm.write(asm_content)
    nasm_command = f'printf "{instruction} {register} | " >> out.txt'
    nasm_result = subprocess.run(nasm_command, shell=True)
    # Executar o NASM e redirecionar saída para out.txt
    nasm_command = f"nasm {asm_file} -o {bin_file} >> {output_file} 2>&1"
    nasm_result = subprocess.run(nasm_command, shell=True)

 # Verificar se houve erro no NASM
    if nasm_result.returncode == 0:
        # Se compilou corretamente, gerar o hexdump do binário com xxd
        f1=open(f"{bin_file}","rb")
        sss=f1.read()
        f1.close()
        s=""
        for b in sss:
            s=s+f"{b:02x}"
        s=s+"\n"
        with open(output_file, "a") as asm:
            asm.write(s)

# Testar todas as combinações de instruções e registradores
for instruction in instructions:
    for register in registers:
        print(instruction+" "+register+"")
        generate_assembly_and_test(instruction, register,value)

# Abrir o arquivo final com gedit
subprocess.run(f"gedit {output_file}", shell=True)

