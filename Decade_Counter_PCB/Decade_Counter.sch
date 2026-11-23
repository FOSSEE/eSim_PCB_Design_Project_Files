EESchema Schematic File Version 2
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:power
LIBS:eSim_Plot
LIBS:transistors
LIBS:conn
LIBS:eSim_User
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:eSim_Analog
LIBS:eSim_Devices
LIBS:eSim_Digital
LIBS:eSim_Hybrid
LIBS:eSim_Miscellaneous
LIBS:eSim_Power
LIBS:eSim_Sources
LIBS:eSim_Subckt
LIBS:eSim_Nghdl
LIBS:eSim_Ngveri
LIBS:eSim_SKY130
LIBS:eSim_SKY130_Subckts
LIBS:Decade_Counter-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Decade Counter "
Date "2026-11-21"
Rev ""
Comp "Aitihya Mondal"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Lm_7805 X1
U 1 1 6AF98A76
P 3900 3950
F 0 "X1" H 3900 3950 60  0000 C CNN
F 1 "Lm_7805" H 3950 4100 60  0000 C CNN
F 2 "TO_SOT_Packages_THT:TO-220-3_Vertical" H 3900 3950 60  0001 C CNN
F 3 "" H 3900 3950 60  0001 C CNN
	1    3900 3950
	1    0    0    -1  
$EndComp
$Comp
L eSim_Diode D3
U 1 1 6AF98AED
P 2700 4250
F 0 "D3" H 2700 4350 50  0000 C CNN
F 1 "eSim_Diode" H 2700 4150 50  0000 C CNN
F 2 "Diodes_THT:D_T-1_P5.08mm_Horizontal" H 2700 4250 60  0001 C CNN
F 3 "" H 2700 4250 60  0000 C CNN
	1    2700 4250
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D4
U 1 1 6AF98B12
P 2700 5000
F 0 "D4" H 2700 5100 50  0000 C CNN
F 1 "eSim_Diode" H 2700 4900 50  0000 C CNN
F 2 "Diodes_THT:D_T-1_P5.08mm_Horizontal" H 2700 5000 60  0001 C CNN
F 3 "" H 2700 5000 60  0000 C CNN
	1    2700 5000
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D2
U 1 1 6AF98B45
P 2200 5000
F 0 "D2" H 2200 5100 50  0000 C CNN
F 1 "eSim_Diode" H 2200 4900 50  0000 C CNN
F 2 "Diodes_THT:D_T-1_P5.08mm_Horizontal" H 2200 5000 60  0001 C CNN
F 3 "" H 2200 5000 60  0000 C CNN
	1    2200 5000
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D1
U 1 1 6AF98B6E
P 2200 4250
F 0 "D1" H 2200 4350 50  0000 C CNN
F 1 "eSim_Diode" H 2200 4150 50  0000 C CNN
F 2 "Diodes_THT:D_T-1_P5.08mm_Horizontal" H 2200 4250 60  0001 C CNN
F 3 "" H 2200 4250 60  0000 C CNN
	1    2200 4250
	0    -1   -1   0   
$EndComp
$Comp
L eSim_Diode D5
U 1 1 6AF99518
P 5050 4600
F 0 "D5" H 5050 4700 50  0000 C CNN
F 1 "eSim_Diode" H 5050 4500 50  0000 C CNN
F 2 "Diodes_THT:D_T-1_P5.08mm_Horizontal" H 5050 4600 60  0001 C CNN
F 3 "" H 5050 4600 60  0000 C CNN
	1    5050 4600
	0    -1   -1   0   
$EndComp
$Comp
L resistor R1
U 1 1 6AF99557
P 5500 4600
F 0 "R1" H 5550 4730 50  0000 C CNN
F 1 "1k" H 5550 4550 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 5550 4580 30  0001 C CNN
F 3 "" V 5550 4650 30  0000 C CNN
	1    5500 4600
	0    1    1    0   
$EndComp
$Comp
L GND #PWR01
U 1 1 6AF9BEBD
P 3900 5700
F 0 "#PWR01" H 3900 5450 50  0001 C CNN
F 1 "GND" H 3900 5550 50  0000 C CNN
F 2 "" H 3900 5700 50  0001 C CNN
F 3 "" H 3900 5700 50  0001 C CNN
	1    3900 5700
	1    0    0    -1  
$EndComp
$Comp
L capacitor C2
U 1 1 6B0140E1
P 3650 4650
F 0 "C2" H 3675 4750 50  0000 L CNN
F 1 "0.1u" H 3675 4550 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D3.0mm_W2.0mm_P2.50mm" H 3688 4500 30  0001 C CNN
F 3 "" H 3650 4650 60  0000 C CNN
	1    3650 4650
	1    0    0    -1  
$EndComp
$Comp
L LM555N X2
U 1 1 6B014A1E
P 5100 2100
F 0 "X2" H 5100 2050 60  0000 C CNN
F 1 "LM555N" H 5100 2200 60  0000 C CNN
F 2 "Housings_DIP:DIP-8_W7.62mm" H 5050 2100 60  0001 C CNN
F 3 "" H 5050 2100 60  0000 C CNN
	1    5100 2100
	1    0    0    -1  
$EndComp
$Comp
L eSim_LED D6
U 1 1 6B014A77
P 9950 2850
F 0 "D6" H 9950 2950 50  0000 C CNN
F 1 "eSim_LED" H 10000 2750 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 2850 50  0001 C CNN
F 3 "" H 9950 2850 50  0001 C CNN
	1    9950 2850
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D7
U 1 1 6B014B06
P 9950 3150
F 0 "D7" H 9950 3250 50  0000 C CNN
F 1 "eSim_LED" H 10000 3050 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 3150 50  0001 C CNN
F 3 "" H 9950 3150 50  0001 C CNN
	1    9950 3150
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D8
U 1 1 6B014B83
P 9950 3450
F 0 "D8" H 9950 3550 50  0000 C CNN
F 1 "eSim_LED" H 10000 3350 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 3450 50  0001 C CNN
F 3 "" H 9950 3450 50  0001 C CNN
	1    9950 3450
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D9
U 1 1 6B014BEC
P 9950 3750
F 0 "D9" H 9950 3850 50  0000 C CNN
F 1 "eSim_LED" H 10000 3650 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 3750 50  0001 C CNN
F 3 "" H 9950 3750 50  0001 C CNN
	1    9950 3750
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D10
U 1 1 6B014C39
P 9950 4050
F 0 "D10" H 9950 4150 50  0000 C CNN
F 1 "eSim_LED" H 10000 3950 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 4050 50  0001 C CNN
F 3 "" H 9950 4050 50  0001 C CNN
	1    9950 4050
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D11
U 1 1 6B014C92
P 9950 4350
F 0 "D11" H 9950 4450 50  0000 C CNN
F 1 "eSim_LED" H 10000 4250 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 4350 50  0001 C CNN
F 3 "" H 9950 4350 50  0001 C CNN
	1    9950 4350
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D14
U 1 1 6B014CE1
P 9950 5250
F 0 "D14" H 9950 5350 50  0000 C CNN
F 1 "eSim_LED" H 10000 5150 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 5250 50  0001 C CNN
F 3 "" H 9950 5250 50  0001 C CNN
	1    9950 5250
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D12
U 1 1 6B014D3A
P 9950 4650
F 0 "D12" H 9950 4750 50  0000 C CNN
F 1 "eSim_LED" H 10000 4550 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 4650 50  0001 C CNN
F 3 "" H 9950 4650 50  0001 C CNN
	1    9950 4650
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D15
U 1 1 6B014D7F
P 9950 5550
F 0 "D15" H 9950 5650 50  0000 C CNN
F 1 "eSim_LED" H 10000 5450 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 5550 50  0001 C CNN
F 3 "" H 9950 5550 50  0001 C CNN
	1    9950 5550
	-1   0    0    1   
$EndComp
$Comp
L eSim_LED D13
U 1 1 6B014E0E
P 9950 4950
F 0 "D13" H 9950 5050 50  0000 C CNN
F 1 "eSim_LED" H 10000 4850 31  0000 C CNN
F 2 "LEDs:LED_D5.0mm" H 9950 4950 50  0001 C CNN
F 3 "" H 9950 4950 50  0001 C CNN
	1    9950 4950
	-1   0    0    1   
$EndComp
$Comp
L resistor R4
U 1 1 6B014E7B
P 10300 5650
F 0 "R4" H 10350 5780 50  0000 C CNN
F 1 "220" H 10350 5600 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 10350 5630 30  0001 C CNN
F 3 "" V 10350 5700 30  0000 C CNN
	1    10300 5650
	0    1    1    0   
$EndComp
$Comp
L GND #PWR02
U 1 1 6B01DA6A
P 7250 4450
F 0 "#PWR02" H 7250 4200 50  0001 C CNN
F 1 "GND" H 7250 4300 50  0000 C CNN
F 2 "" H 7250 4450 50  0001 C CNN
F 3 "" H 7250 4450 50  0001 C CNN
	1    7250 4450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 6B021196
P 10350 6050
F 0 "#PWR03" H 10350 5800 50  0001 C CNN
F 1 "GND" H 10350 5900 50  0000 C CNN
F 2 "" H 10350 6050 50  0001 C CNN
F 3 "" H 10350 6050 50  0001 C CNN
	1    10350 6050
	1    0    0    -1  
$EndComp
$Comp
L resistor R2
U 1 1 6B014B4D
P 6150 1900
F 0 "R2" H 6200 2030 50  0000 C CNN
F 1 "22k" H 6200 1850 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 6200 1880 30  0001 C CNN
F 3 "" V 6200 1950 30  0000 C CNN
	1    6150 1900
	0    1    1    0   
$EndComp
$Comp
L resistor R3
U 1 1 6B014C14
P 6150 2200
F 0 "R3" H 6200 2330 50  0000 C CNN
F 1 "22k" H 6200 2150 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 6200 2180 30  0001 C CNN
F 3 "" V 6200 2250 30  0000 C CNN
	1    6150 2200
	0    1    1    0   
$EndComp
$Comp
L GND #PWR04
U 1 1 6B0151E0
P 5100 2800
F 0 "#PWR04" H 5100 2550 50  0001 C CNN
F 1 "GND" H 5100 2650 50  0000 C CNN
F 2 "" H 5100 2800 50  0001 C CNN
F 3 "" H 5100 2800 50  0001 C CNN
	1    5100 2800
	1    0    0    -1  
$EndComp
$Comp
L capacitor C3
U 1 1 6B018632
P 4500 2600
F 0 "C3" H 4525 2700 50  0000 L CNN
F 1 "0.1u" H 4525 2500 50  0000 L CNN
F 2 "Capacitors_THT:C_Disc_D3.0mm_W2.0mm_P2.50mm" H 4538 2450 30  0001 C CNN
F 3 "" H 4500 2600 60  0000 C CNN
	1    4500 2600
	-1   0    0    1   
$EndComp
Text Label 5750 1850 0    60   ~ 0
CLK
Text Label 5550 3850 0    60   ~ 0
+5v
Text Label 5100 1200 0    60   ~ 0
+5v
Text Label 4550 1850 2    60   ~ 0
Trig
Text Label 5850 2400 3    60   ~ 0
Trig
Text Label 7400 3650 2    60   ~ 0
CLK
$Comp
L GND #PWR05
U 1 1 6B01A2EB
P 8050 4900
F 0 "#PWR05" H 8050 4650 50  0001 C CNN
F 1 "GND" H 8050 4750 50  0000 C CNN
F 2 "" H 8050 4900 50  0001 C CNN
F 3 "" H 8050 4900 50  0001 C CNN
	1    8050 4900
	1    0    0    -1  
$EndComp
Text Label 8050 3450 0    60   ~ 0
+5v
NoConn ~ 8700 4750
$Comp
L PWR_FLAG #FLG06
U 1 1 6B01C3FC
P 7100 3850
F 0 "#FLG06" H 7100 3925 50  0001 C CNN
F 1 "PWR_FLAG" H 7100 4000 50  0000 C CNN
F 2 "" H 7100 3850 50  0001 C CNN
F 3 "" H 7100 3850 50  0001 C CNN
	1    7100 3850
	0    -1   -1   0   
$EndComp
$Comp
L 4017 U5
U 1 1 6B019A5D
P 8050 4200
F 0 "U5" H 7950 4050 50  0000 C CNN
F 1 "4017" H 7950 3900 50  0000 C CNN
F 2 "Housings_DIP:DIP-16_W7.62mm" H 8050 4200 60  0001 C CNN
F 3 "" H 8050 4200 60  0001 C CNN
	1    8050 4200
	1    0    0    -1  
$EndComp
$Comp
L Conn_01x02 J2
U 1 1 6B01D268
P 6100 4500
F 0 "J2" H 6100 4600 50  0000 C CNN
F 1 "Conn_01x02" H 6100 4300 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 6100 4500 50  0001 C CNN
F 3 "" H 6100 4500 50  0001 C CNN
	1    6100 4500
	1    0    0    -1  
$EndComp
$Comp
L Screw_Terminal_01x02 J1
U 1 1 6B01E3E1
P 1250 4600
F 0 "J1" H 1250 4700 50  0000 C CNN
F 1 "Screw_Terminal_01x02" H 1250 4400 50  0000 C CNN
F 2 "Connectors_Terminal_Blocks:TerminalBlock_Altech_AK300-2_P5.00mm" H 1250 4600 50  0001 C CNN
F 3 "" H 1250 4600 50  0001 C CNN
	1    1250 4600
	-1   0    0    -1  
$EndComp
$Comp
L capacitor_polarised C1
U 1 1 6B01BCB6
P 3250 4650
F 0 "C1" H 3275 4750 50  0000 L CNN
F 1 "1000u" H 3275 4550 50  0000 L CNN
F 2 "Capacitors_THT:CP_Radial_D5.0mm_P2.50mm" H 3250 4650 50  0001 C CNN
F 3 "" H 3250 4650 50  0001 C CNN
	1    3250 4650
	1    0    0    -1  
$EndComp
$Comp
L capacitor_polarised C4
U 1 1 6B01BDC5
P 4550 4650
F 0 "C4" H 4575 4750 50  0000 L CNN
F 1 "100u" H 4575 4550 50  0000 L CNN
F 2 "Capacitors_THT:CP_Radial_D5.0mm_P2.50mm" H 4550 4650 50  0001 C CNN
F 3 "" H 4550 4650 50  0001 C CNN
	1    4550 4650
	1    0    0    -1  
$EndComp
$Comp
L capacitor_polarised C5
U 1 1 6B01F9FE
P 6200 2550
F 0 "C5" H 6225 2650 50  0000 L CNN
F 1 "47u" H 6225 2450 50  0000 L CNN
F 2 "Capacitors_THT:CP_Radial_D5.0mm_P2.50mm" H 6200 2550 50  0001 C CNN
F 3 "" H 6200 2550 50  0001 C CNN
	1    6200 2550
	1    0    0    -1  
$EndComp
$Comp
L PWR_FLAG #FLG07
U 1 1 6B01C7F8
P 4900 1250
F 0 "#FLG07" H 4900 1325 50  0001 C CNN
F 1 "PWR_FLAG" H 4900 1400 50  0000 C CNN
F 2 "" H 4900 1250 50  0001 C CNN
F 3 "" H 4900 1250 50  0001 C CNN
	1    4900 1250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	2200 5150 2200 5450
Wire Wire Line
	2700 5450 2700 5150
Wire Wire Line
	2200 4100 2200 3950
Wire Wire Line
	2200 3950 3350 3950
Wire Wire Line
	2700 3950 2700 4100
Wire Wire Line
	3250 3950 3250 4500
Connection ~ 2700 3950
Connection ~ 2700 5450
Connection ~ 3250 3950
Wire Wire Line
	3900 4350 3900 5700
Connection ~ 3250 5450
Wire Wire Line
	4550 5450 4550 4800
Connection ~ 3900 5450
Wire Wire Line
	5050 3950 5050 4450
Connection ~ 4550 3950
Wire Wire Line
	5050 5450 5050 4750
Connection ~ 4550 5450
Connection ~ 5050 3950
Wire Wire Line
	5550 5450 5550 4800
Connection ~ 5050 5450
Connection ~ 5550 3950
Connection ~ 3900 5650
Wire Wire Line
	5550 3850 5550 4500
Wire Wire Line
	2200 4400 2200 4850
Wire Wire Line
	2700 4400 2700 4850
Connection ~ 2700 4600
Connection ~ 2200 4700
Connection ~ 5550 5450
Wire Wire Line
	3250 5450 3250 4800
Wire Wire Line
	3650 4800 3650 5000
Wire Wire Line
	3650 5000 3250 5000
Connection ~ 3250 5000
Wire Wire Line
	3650 4500 3650 4350
Wire Wire Line
	3650 4350 3250 4350
Connection ~ 3250 4350
Connection ~ 2200 5450
Wire Wire Line
	8700 4050 9800 4050
Wire Wire Line
	8700 3950 9650 3950
Wire Wire Line
	9650 3950 9650 3750
Wire Wire Line
	9650 3750 9800 3750
Wire Wire Line
	8700 4150 9650 4150
Wire Wire Line
	9650 4150 9650 4350
Wire Wire Line
	9650 4350 9800 4350
Wire Wire Line
	8700 3850 9550 3850
Wire Wire Line
	9550 3850 9550 3450
Wire Wire Line
	9550 3450 9800 3450
Wire Wire Line
	8700 4250 9550 4250
Wire Wire Line
	9550 4250 9550 4650
Wire Wire Line
	9550 4650 9800 4650
Wire Wire Line
	8700 3750 9450 3750
Wire Wire Line
	9450 3750 9450 3150
Wire Wire Line
	9450 3150 9800 3150
Wire Wire Line
	8700 4350 9450 4350
Wire Wire Line
	9450 4350 9450 4950
Wire Wire Line
	9450 4950 9800 4950
Wire Wire Line
	8700 3650 9350 3650
Wire Wire Line
	9350 3650 9350 2850
Wire Wire Line
	9350 2850 9800 2850
Wire Wire Line
	8700 4450 9350 4450
Wire Wire Line
	9350 4450 9350 5250
Wire Wire Line
	9350 5250 9800 5250
Wire Wire Line
	8700 4550 9250 4550
Wire Wire Line
	9250 4550 9250 5550
Wire Wire Line
	9250 5550 9800 5550
Wire Wire Line
	7400 3750 7400 3950
Wire Wire Line
	7250 4450 7250 3850
Wire Wire Line
	7100 3850 7400 3850
Connection ~ 7400 3850
Wire Wire Line
	10100 2850 10350 2850
Wire Wire Line
	10350 2850 10350 5550
Wire Wire Line
	10350 5550 10100 5550
Wire Wire Line
	10100 5250 10350 5250
Connection ~ 10350 5250
Wire Wire Line
	10100 4950 10350 4950
Connection ~ 10350 4950
Wire Wire Line
	10100 4650 10350 4650
Connection ~ 10350 4650
Wire Wire Line
	10100 4350 10350 4350
Connection ~ 10350 4350
Wire Wire Line
	10100 4050 10350 4050
Connection ~ 10350 4050
Wire Wire Line
	10100 3750 10350 3750
Connection ~ 10350 3750
Wire Wire Line
	10100 3450 10350 3450
Connection ~ 10350 3450
Wire Wire Line
	10100 3150 10350 3150
Connection ~ 10350 3150
Wire Wire Line
	10350 6050 10350 5850
Wire Wire Line
	5100 1200 5100 1500
Wire Wire Line
	4350 1450 6200 1450
Wire Wire Line
	5100 2700 5100 2800
Connection ~ 5100 2750
Wire Wire Line
	5650 2100 6200 2100
Wire Wire Line
	6200 1450 6200 1800
Wire Wire Line
	5650 2350 5850 2350
Wire Wire Line
	5850 2350 5850 2400
Wire Wire Line
	5850 2400 6200 2400
Connection ~ 5850 2400
Wire Wire Line
	4500 2450 4500 2100
Wire Wire Line
	4500 2100 4550 2100
Wire Wire Line
	4500 2750 6200 2750
Wire Wire Line
	4550 2350 4350 2350
Wire Wire Line
	4350 2350 4350 1450
Connection ~ 5100 1450
Wire Wire Line
	6200 2750 6200 2700
Wire Wire Line
	4550 4500 4550 3950
Wire Wire Line
	8050 4900 8050 4800
Wire Wire Line
	8050 3600 8050 3450
Connection ~ 7250 3850
Connection ~ 5100 1250
Wire Wire Line
	1450 4600 2700 4600
Wire Wire Line
	1450 4700 2200 4700
Wire Wire Line
	2200 5450 5900 5450
Wire Wire Line
	4450 3950 5900 3950
Wire Wire Line
	5900 3950 5900 4500
Wire Wire Line
	5900 5450 5900 4600
Wire Wire Line
	5750 1850 5650 1850
Wire Wire Line
	4900 1250 5100 1250
Wire Notes Line
	700  3300 700  6100
Wire Notes Line
	700  6100 6400 6100
Wire Notes Line
	6400 6100 6400 3300
Wire Notes Line
	6400 3300 700  3300
Wire Notes Line
	10600 2500 6750 2500
Wire Notes Line
	6750 2500 6750 6400
Wire Notes Line
	6750 6400 10600 6400
Wire Notes Line
	10600 6400 10600 2500
Wire Notes Line
	3800 750  3800 3100
Wire Notes Line
	3800 3100 6450 3100
Wire Notes Line
	6450 3100 6450 750 
Wire Notes Line
	6450 750  3800 750 
Text Notes 3150 3450 0    60   ~ 0
Voltage Regulator
Text Notes 5000 900  0    60   ~ 0
Clock
Text Notes 8600 2650 0    60   ~ 0
Counter
$EndSCHEMATC
