global main: function

extern putchar                                          ; near
extern __printf_chk                                     ; near


SECTION .text


SECTION .data


SECTION .bss


SECTION .rodata

message:
        db 25H, 64H, 20H, 00H                           ; "%d "


SECTION .text

main:   ; Function begin
        push    rbp                                     ; 0004 _ 55
        lea     rbp, message                            ; 0005 _ 48: 8D. 2D, 00000000(rel)
        push    rbx                                     ; 000C _ 53
        xor     ebx, ebx                                ; 000D _ 31. DB
        sub     rsp, 8                                  ; 000F _ 48: 83. EC, 08
loops:  mov     edx, ebx                                ; 0018 _ 89. DA
        mov     rsi, rbp                                ; 001A _ 48: 89. EE
        mov     edi, 1                                  ; 001D _ BF, 00000001
        xor     eax, eax                                ; 0022 _ 31. C0
        call    __printf_chk                            ; 0024 _ E8, 00000000(PLT r)
        add     ebx, 1                                  ; 0029 _ 83. C3, 01
        cmp     ebx, 10                                 ; 002C _ 83. FB, 0A
        jnz     loops                                   ; 002F _ 75, E7
        mov     edi, 10                                 ; 0031 _ BF, 0000000A
        call    putchar                                 ; 0036 _ E8, 00000000(PLT r)
        add     rsp, 8                                  ; 003B _ 48: 83. C4, 08
        xor     eax, eax                                ; 003F _ 31. C0
        pop     rbx                                     ; 0041 _ 5B
        pop     rbp                                     ; 0042 _ 5D
        ret  
                                                        ; 0043 _ C3


