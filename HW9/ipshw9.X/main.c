#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro

#include <stdio.h>
#include <math.h>
#include "ST7789.h"
#include "spi.h"

// DEVCFG0
#pragma config DEBUG = OFF // disable debugging
#pragma config JTAGEN = OFF // disable jtag
#pragma config ICESEL = ICS_PGx1 // use PGED1 and PGEC1
#pragma config PWP = OFF // disable flash write protect
#pragma config BWP = OFF // disable boot write protect
#pragma config CP = OFF // disable code protect

// DEVCFG1
#pragma config FNOSC = FRCPLL // use internal oscillator with pll
#pragma config FSOSCEN = OFF // disable secondary oscillator
#pragma config IESO = OFF // disable switching clocks
#pragma config POSCMOD = OFF // internal RC
#pragma config OSCIOFNC = OFF // disable clock output
#pragma config FPBDIV = DIV_1 // divide sysclk freq by 1 for peripheral bus clock
#pragma config FCKSM = CSDCMD // disable clock switch and FSCM
#pragma config WDTPS = PS1048576 // use largest wdt
#pragma config WINDIS = OFF // use non-window mode wdt
#pragma config FWDTEN = OFF // wdt disabled
#pragma config FWDTWINSZ = WINSZ_25 // wdt window at 25%

// DEVCFG2 - get the sysclk clock to 48MHz from the 8MHz crystal
#pragma config FPLLIDIV = DIV_2 // divide input clock to be in range 4-5MHz
#pragma config FPLLMUL = MUL_24 // multiply clock after FPLLIDIV
#pragma config FPLLODIV = DIV_2 // divide clock after FPLLMUL to get 48MHz

// DEVCFG3
#pragma config USERID = 00000001 // some 16bit userid, doesn't matter what
#pragma config PMDL1WAY = OFF // allow multiple reconfigurations
#pragma config IOL1WAY = OFF // allow multiple reconfigurations



int main() {

    __builtin_disable_interrupts(); // disable interrupts while initializing things

    // set the CP0 CONFIG register to indicate that kseg0 is cacheable (0x3)
    __builtin_mtc0(_CP0_CONFIG, _CP0_CONFIG_SELECT, 0xa4210583);

    // 0 data RAM access wait states
    BMXCONbits.BMXWSDRM = 0x0;

    // enable multi vector interrupts
    INTCONbits.MVEC = 0x1;

    // disable JTAG to get pins back
    DDPCONbits.JTAGEN = 0;

    // do your TRIS and LAT commands here
    TRISBbits.TRISB4 = 1;
    TRISAbits.TRISA4 = 0;
    LATAbits.LATA4 = 0;
    
    
    initSPI();
    LCD_init();
    __builtin_enable_interrupts();
    _CP0_SET_COUNT(0);
    LCD_clearScreen(BLACK);
    char* hellow[50];
    char* number[50];
    char* fpscount[50];
    int delay = 0;
    int ii = 0;
    int timestart;
    
    
    LCD_drawProgressBar(28,50,200,RED);
    while(1)
    {
        
        for (ii = 0; ii < 100; ii++) {
        timestart = _CP0_GET_COUNT();
        delay = 0;
        sprintf(hellow, "Hello World! %d", ii);
        sprintf(number, "%d", ii);
        LCD_drawString(28, 32, CYAN, hellow);
        while (delay < 500000) {
            delay++;
        }
        LCD_drawString(28 + 13 * 6, 32, BLACK, number);
        LCD_drawProgressBar(28,50,ii*2,BLUE);
        if (ii == 99)
        {
            LCD_drawProgressBar(28,50,200,RED);
        }
        LCD_drawString(28+6*8, 82, BLACK, fpscount);
        sprintf(hellow,"FPS: ");
        LCD_drawString(28, 82, CYAN, hellow);
        sprintf(fpscount, "%d", 24000000/(_CP0_GET_COUNT()-timestart));
        LCD_drawString(28+6*8, 82, CYAN, fpscount);
        
    }
    }
    
}