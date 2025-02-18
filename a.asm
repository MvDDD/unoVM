var _16 counter 	; compile-time: allocate variable
var _16 loop_end	; compile-time: allocate variable

mov counter, 0      ; init the counter as 0
mov loop_end, 0xFF     ;init the loop end as 255







/*
var _16 counter 	; compile-time: allocate variable
var _16 loop_end	; compile-time: allocate variable
;the alloc() function in the compiler optimizes ram usage (but doesnt defragment)
;also doesn't handle dynamic allocations ("buffer" not yet implemented)

//setting up RAM
mov counter, 0      ; init the counter as 0
mov loop_end, 0xFF     ;init the loop end as 255
;2 times mov8 gets optimized to mov16. irrelevant here, but the program builder handles that
;more optimizations to be added
//END setting up RAM

LOOPSTART:				;program.target
	add counter, 1
	push counter
	push 10
	call print ;print reads values from the stack: push value, then push base
	;call pushes the current osition to the callstack, and then pops it at return. 

	cmp counter < loop_end			;string that the compiler turns into CMP.LT()
	jmi LOOPSTART	;jump to target if result

jmp LIBEND 	;MAKE SURE RET IS NOT ACCESSIBLE WITHOUT ANY CALL
;so before the lib starts, jump to its end
;tip: make all internal vars start with a special char.
;that way you avoid overwriting any var used before

PRINTNUMBER:
	var _16 TMPA
	var _16 TMPB
	var _16 __val
	mov TMPA, A
	mov TMPB, B
	pop B ;get the base
	pop A ;get the value
	mov __val, A
	__loop:
		mod A, B  ;get remainder
		add A, 48 ;add offset: "0"
		print A
		mov A, __val
		div A, B
		mov __val, A
		cmp A != 0
	jmi __loop
	mov A, TMPA
	mov B, TMPB
	free TMPA
	free TMPB
	free __val
	ret
LIBEND:

;END:
free counter
free loop_end
exit 0          ;exit code 0

*/
