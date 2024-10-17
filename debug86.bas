
' Tamanho da memória (64 KB)
const MEM_SIZE = &H10000

' Definir registradores de 16 bits
dim shared as ushort ax = 0, bx = 0, cx = 0, dx = 0
dim shared as ushort ip = &H100  ' Ponteiro de instrução começa em 0x100
dim shared as string dummy
' Memória de 64 KB
dim shared as ubyte memory(MEM_SIZE - 1)

' Lista de opcodes permitidos
enum Opcodes
    MOV_AX = &HB8
    MOV_BX = &HBB
    MOV_CX = &HB9
    MOV_DX = &HBA
    NOP    = &H90
    ADD_AX = &H05
    ADD_BX = &H81
    ADD_CX = &H03
    ADD_DX = &H02
    RET    = &HC3
end enum

' Função para exibir o estado dos registradores
sub print_state(instruction as string)
    print "IP:" + hex(ip, 4) + " | AX:" & hex(ax, 4) + " | BX:" & hex(bx, 4) + " | CX:" & hex(cx, 4) + " | DX:" + hex(dx, 4) + " | Executando: " + instruction
end sub

' Função para carregar o programa na memória
sub load_program(file_name as string)
    dim as integer file = freefile
    if open(file_name for binary access read as #file) <> 0 then
        print "Erro ao abrir o ficheiro"
        end 1
    end if

    ' Carregar o programa a partir do endereço 0x100
    dim as integer index = &H100
    while not eof(file) and index < MEM_SIZE
        get #file, , memory(index)
        index += 1
    wend
    close #file
end sub

' Emulador que processa instrução por instrução
sub emulate()
    while true
        dim as ubyte opcode = memory(ip)

        select case opcode
            case RET
                print_state("ret")
                print "Instrução 'ret' atingida. Saindo do programa."
                exit while

            case MOV_AX
                ax = memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("mov ax")
                ip += 3

            case MOV_BX
                bx = memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("mov bx")
                ip += 3

            case MOV_CX
                cx = memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("mov cx")
                ip += 3

            case MOV_DX
                dx = memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("mov dx")
                ip += 3

            case ADD_AX
                ax += memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("add ax")
                ip += 3

            case ADD_BX
                bx += memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("add bx")
                ip += 3

            case ADD_CX
                cx += memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("add cx")
                ip += 3

            case ADD_DX
                dx += memory(ip + 1) or (memory(ip + 2) shl 8)
                print_state("add dx")
                ip += 3

            case NOP
                print_state("nop")
                ip += 1

            case else
                print "Erro: Opcode desconhecido " & hex(opcode, 2) & " em IP " & hex(ip, 4)
                end 1
        end select

        ' Espera o usuário pressionar Enter para continuar
        input "Pressione Enter para continuar...", dummy
    wend
end sub

' Função principal
sub main()
    if command(1) = "" then
        print "Uso: emulador <ficheiro.com>"
        end 1
    end if

    ' Carregar o programa na memória
    load_program(command(1))

    ' Iniciar a emulação
    emulate()
end sub

' Iniciar o programa
main()
