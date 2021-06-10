#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro

#include <stdio.h>
#include <math.h>
#include "ST7789.h"
#include "spi.h"
#include "i2c_master_noint.h"

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
    i2c_master_setup();
    __builtin_enable_interrupts();
    _CP0_SET_COUNT(0);
    
    //Reading the WHO_AM_I register
    if (readPin(0b1101010, 0x0F) != 0b01101001)
    {
        LATAbits.LATA4=1;
        while(1)
        {
            
        }
    }
    //Setting the IMU Registers for initialization
    setPin(0b1101010,0x10,0b10000010); //init CTRL_X1
    setPin(0b1101010,0x11,0b10001000); //init CTRL2_G
    setPin(0b1101010,0x12,0b00000100); //init CTRL3_C
    
    
    
    
    LCD_clearScreen(BLACK);
    char* hellow[50];
    char* number[50];
    char* imudata1[200];
    char* imudata2[50];
    char* fpscount[50];
    unsigned char imudata[14];
    signed short* imudataadj[7];
    int delay = 0;
    int ii = 0;
    int timestart;
    int count = 0;
    
    //LCD_drawProgressBar(28,50,200,RED);
    while (1) {
        for (ii = 0; ii < 100; ii++) {
            if (_CP0_GET_COUNT() > 4000000) {
                LATAbits.LATA4 = !LATAbits.LATA4;
                count += 1;
                _CP0_SET_COUNT(0);
            }
            if (count == 4) {
                LATAbits.LATA4 = 0;
                count = 0;
            }
            timestart = _CP0_GET_COUNT();
            delay = 0;
            int jj = 0;
            
            
            i2c_read_multiple(0b1101010, 0x20, imudata, 14);
            
            for (jj = 0; jj < 7; jj++) {
                imudataadj[jj] = (short)((imudata[jj*2+1] << 8) | imudata[jj*2]);
                //imudataadj[jj] = (signed short) ((imudata[jj*2] << 8) | imudata[jj+1]);
            }
            
            sprintf(imudata1, "%d  ", (short) imudataadj[0]);
            LCD_drawString(28, 32, CYAN, imudata1);
            sprintf(imudata1, "%d  ", imudataadj[1]);
            LCD_drawString(28, 38+6, CYAN, imudata1);
            sprintf(imudata1, "%d  ", imudataadj[2]);
            LCD_drawString(28, 44+12, CYAN, imudata1);
            sprintf(imudata1, "%d  ", imudataadj[3]);
            LCD_drawString(28, 50+18, CYAN, imudata1);
            sprintf(imudata1, "%d  ", imudataadj[4]);
            LCD_drawString(28, 56+24, CYAN, imudata1);
            sprintf(imudata1, "%d  ", imudataadj[5]);
            LCD_drawString(28, 62+30, CYAN, imudata1);
            sprintf(imudata1, "%d  ", imudataadj[6]);
            LCD_drawString(28, 68+36, CYAN, imudata1);
            
//
//            int jj = 0;
//            for (jj = 0; jj < 7; jj++) {
//                LCD_drawString(28, 32 + 5 * jj, CYAN, imudataadj[jj]);
//            }
            //Hello World
//            sprintf(hellow, "Hello World! %d", ii);
//            sprintf(number, "%d", ii);
//            LCD_drawString(28, 32, CYAN, hellow);
            
            LCD_drawVProgressBar(28, 150, abs(imudataadj[4])/100, BLUE);
            LCD_drawHProgressBar(28, 150, abs(imudataadj[5])/100, BLUE);
            while (delay < 1000) {
                delay++;
            }
            
            LCD_drawVProgressBar(28, 150, abs(imudataadj[4])/100, BLACK);
            LCD_drawHProgressBar(28, 150, abs(imudataadj[5])/100, BLACK);
           // LCD_clearScreen(BLACK);
            
            //Progress Bar
//            LCD_drawProgressBar(28, 50, ii * 2, BLUE);
//            if (ii == 99) {
//                LCD_drawProgressBar(28, 50, 200, RED);
//            }
            
            //FPS
//            sprintf(hellow, "FPS: ");
//            LCD_drawString(28, 182, CYAN, hellow);
//            sprintf(fpscount, "%d", 24000000 / (_CP0_GET_COUNT() - timestart));
//            LCD_drawString(28 + 6 * 8, 182, CYAN, fpscount);

        }
    }
    
}