#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro

#include <stdio.h>
#include <math.h>
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

void readUART1(char * string, int maxLength);
void writeUART1(const char * string);

void initSPI();
unsigned char spi_io(unsigned char o);
void spi_dac(unsigned char channel, unsigned short voltage);


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
    
    //Setting the UART stuff
    U1RXRbits.U1RXR = 0b0001;   //U1RX is B6
    RPB7Rbits.RPB7R = 0b0001;   //U1TX is B7
    
    // turn on UART3 without an interrupt
    U1MODEbits.BRGH = 0; // set baud to NU32_DESIRED_BAUD
    U1BRG = ((48000000 / 115200) / 16) - 1;

     // 8 bit, no parity bit, and 1 stop bit (8N1 setup)
    U1MODEbits.PDSEL = 0;
    U1MODEbits.STSEL = 0;

    // configure TX & RX pins as output & input pins
    U1STAbits.UTXEN = 1;
    U1STAbits.URXEN = 1;

    // enable the uart
    U1MODEbits.ON = 1;
    
    initSPI();
    i2c_master_setup();
    setPin(0b0100000, 0x00, 0x00);
    setPin(0b0100000, 0x01, 0xFF);
    __builtin_enable_interrupts();
    int count = 0;
    unsigned char buttonPressed = 0;
    _CP0_SET_COUNT(0);
           LATAbits.LATA4 = 1;
           while(1)
           {
               if (_CP0_GET_COUNT() > 4000000)
               {
                   LATAbits.LATA4 = !LATAbits.LATA4;
                   count += 1;
                   _CP0_SET_COUNT(0);
               }
               if (count == 4)
               {
                   LATAbits.LATA4 = 0;
                   count = 0;
               }
               buttonPressed = readPin(0b0100000,0x13);
               //GOAL: read from GPB0, turn on GPA7 if the button is pushed
               if(!buttonPressed)
               {
                setPin(0b0100000, 0x14, 0xFF);
               }
               else
               {
                setPin(0b0100000,0x14,0x00);
               }
           }
}

void initSPI() {
    //Pin B14 becomes SCK1
    //Turn off analog pins
    ANSELA = 0;
    // Make A0 the output pin for CS
    TRISAbits.TRISA0 = 0;
    LATAbits.LATA0 = 1;
    //Make A1 SDO1
    RPA1Rbits.RPA1R = 0b0011;
    // Make B5 SDI1
    SDI1Rbits.SDI1R = 0b0001;
    
    // setup SPI1
    SPI1CON = 0;
    SPI1BUF;
    SPI1BRG = 1000;
    SPI1STATbits.SPIROV = 0;
    SPI1CONbits.CKE = 1;
    SPI1CONbits.MSTEN = 1;
    SPI1CONbits.ON = 1;
    
    
    
}

unsigned char spi_io(unsigned char o) {
    SPI1BUF = o;
    while (!SPI1STATbits.SPIRBF) {
        ;
    }
    return SPI1BUF;
}

void spi_dac(unsigned char channel, unsigned short voltage)
{
    unsigned short output;
    output = channel << 15;
    output = output | (0b111 << 12);
    output = output | voltage;
    spi_io(output >> 8);
    spi_io(output);
}

void readUART1(char * message, int maxLength) {
  char data = 0;
  int complete = 0, num_bytes = 0;
  // loop until you get a '\r' or '\n'
  while (!complete) {
    if (U1STAbits.URXDA) { // if data is available
      data = U1RXREG;      // read the data
      if ((data == '\n') || (data == '\r')) {
        complete = 1;
      } else {
        message[num_bytes] = data;
        ++num_bytes;
        // roll over if the array is too small
        if (num_bytes >= maxLength) {
          num_bytes = 0;
        }
      }
    }
  }
  // end the string
  message[num_bytes] = '\0';
}

void writeUART1(const char * string) {
  while (*string != '\0') {
    while (U1STAbits.UTXBF) {
      ; // wait until tx buffer isn't full
    }
    U1TXREG = *string;
    ++string;
  }
}