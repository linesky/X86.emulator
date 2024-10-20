import os
import subprocess

# Lista de registradores
registers = ["ax", "bx", "cx","dx", "si", "di","sp", "[bx]", "[si]", "[di]","[sp]","bp","[bp]","0x1000","0xff","0x10000000","ah","al", "bh","bl", "ch","cl", "dh","dl","[0x1000]","[0xff]","[0x10000000]","eax", "ebx", "ecx", "esi", "edi", "ebp", "esp", "[ebx]", "[esi]", "[edi]", "[ebp]", "[esp]"]

# Lista de instruções
instructions = ["adc","arpl","bound","bsf","bswap","bt","btc","btr","bts","call","cmovcc","cmp","mov", "add","cmpsxchg" ,"cmpsxchg486","cmpsxchg","sub", "and", "or","xor","enter","in","out","int","jcxz","jecxz","jmp","jcc","jcc near", "lds", "les","lfs","lgs","lss","lea","lgdt","lgdt","lidt","lldt","lmsw","loop","loope","loopz","loopne","loopnz","lsl","ltr","movd","movq","movzx","neg","not","packssdw","packsswb","packuswb","paddb","paddw","paddd", "paddsb","paddsw" ,"paddusb","paddusw","paddsiw","pand","pandn","paveb","pcmpeqb","pcmpeqw","pcmpeqd","pcmgtb","pcmgtw","pcmgtd","pdistib","pmaddwd","pmagw","pmulhw","pmullw","pmvzb","pmvnzb","pmvlzb","pmvgezb","pop","por","psllw","pslld","psllq","psraw","psrad","psrlw","psrld","psrlq","psubsiw","pumpckhbw","pumpckhbd","pumpckhdq","pumpcklbw","pumpcklbd","pumpckldq","push","rcl","rcr","rol","sal","sar","sbb","set","sgdt","sidt","sldt","shl","shr","shld","shrd","str","sub","test","umov","verr","verw","xadd","xbts","xchg","xor"]

# Valor para a operação
value = "0x10"

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
    nasm_command = f'printf "{instruction} {register},{value}|" >> out.txt'
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
        for register2 in registers:
            print(instruction+" "+register+","+register2)
            generate_assembly_and_test(instruction, register,register2)

# Abrir o arquivo final com gedit
subprocess.run(f"gedit {output_file}", shell=True)

