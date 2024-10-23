.global _lens
@ arm-linux-gnueabihf-as -o len.o len.s
_lens:
	push {fp,lr}
	add fp,sp,#4
	sub sp,sp,#16
	mov r3,r0
	mov r0,#0
	
	lenss:
		ldrb r1,[r3]
		cmp r1,#0
		beq lensss
		add r3,r3,#1
		add r0,r0,#1
		b lenss 
	lensss:
	sub sp,fp,#4
	pop {fp,pc}
