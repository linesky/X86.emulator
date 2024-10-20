import os
import subprocess

# Lista de registradores
registers = ["0x10000000","0xff"]

# Lista de instruções
instructions = ["aaa","aas","nop","retf","ret","iret","aad","aam","clc","cld","cli","clts","cpuid","dda","das","emms","f2xm1","hlt","insb","insw","insd","int3","int1","icebp","int01","into","invd","iretw","iretd","lahf","leave","loadall","loadall286","lodb","lodw","lodd","movsb","movsw","movsd","outb","outw","outd","popa","popw","popd","popf","popfw","popfd","pusha","pushaw","pushad","pushf","pushfd","pushfw","rdmsr","rdmsc","mdtsd","sahf","rsm","salc","scasb","scasw","scasd","smi","stosb","stosw","stosd","wait","wbinvd","wrmsr","xlatb"]

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
def generate_assembly_and_test(instruction):
    # Gerar o conteúdo do arquivo .asm
    asm_content = f"org 0x100\n{instruction} \n"
    
    # Escrever o arquivo assembly
    with open(asm_file, "w") as asm:
        asm.write(asm_content)
    nasm_command = f'printf "{instruction} | " >> out.txt'
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
    print(instruction+" ")
    generate_assembly_and_test(instruction)

# Abrir o arquivo final com gedit
subprocess.run(f"gedit {output_file}", shell=True)

