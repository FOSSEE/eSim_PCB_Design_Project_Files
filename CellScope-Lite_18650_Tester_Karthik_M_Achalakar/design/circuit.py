"""
CellScope-Lite: single source of truth for the circuit.

Every part: ref, symbol lib_id, value, footprint, extra fields, {pin_number: net},
schematic block. The schematic (.kicad_sch) and PCB (.kicad_pcb) are generated
from this file, then opened, checked and finished in eSim 2.6 (KiCad), then saved in KiCad 6.0 format (tools/to_kicad6.py).

Nets that start with '+' or are 'GND' use power symbols in the schematic.
NC = no-connect flag on that pin.
"""

NC = None

R0603 = "Resistor_SMD:R_0603_1608Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
LED0603 = "LED_SMD:LED_0603_1608Metric"


def R(ref, val, a, b, block, fp=R0603, **f):
    return dict(ref=ref, lib="Device:R", value=val, fp=fp, pins={"1": a, "2": b}, block=block, fields=f)


def C(ref, val, a, b, block, fp=C0603, **f):
    return dict(ref=ref, lib="Device:C", value=val, fp=fp, pins={"1": a, "2": b}, block=block, fields=f)


def LED(ref, color, k, a, block):
    # Device:LED pin 1 = K, pin 2 = A
    return dict(ref=ref, lib="Device:LED", value=color, fp=LED0603, pins={"1": k, "2": a}, block=block, fields={})


def TP(ref, net, block):
    return dict(ref=ref, lib="Connector:TestPoint", value=net.lstrip("+"), fp="TestPoint:TestPoint_Pad_D1.5mm",
                pins={"1": net}, block=block, fields={})


BLOCKS = [
    ("USB", "1. USB-C 5 V input + protection"),
    ("CHG", "2. TP4056 1 A Li-ion charger"),
    ("BMS", "3. DW01A + FS8205A cell protection"),
    ("PWR", "4. 3.3 V rail + 2.048 V precision reference"),
    ("SET", "5. Load current set-point (trimmer / external DAC)"),
    ("CCL", "6. Constant-current electronic load (op-amp + MOSFET)"),
    ("MON", "7. INA226 16-bit power monitor (I2C)"),
    ("UVL", "8. Discharge cut-off comparator (3.0 V trip / 3.5 V release)"),
    ("IO", "9. Host interface, test points, mechanical"),
]

PARTS = [
    # ---------------- 1. USB-C input ----------------
    dict(ref="J1", lib="Connector:USB_C_Receptacle_USB2.0_16P", value="USB-C 5V",
         fp="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
         pins={"A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND",
               "A4": "VBUS_IN", "A9": "VBUS_IN", "B4": "VBUS_IN", "B9": "VBUS_IN",
               "A5": "CC1", "B5": "CC2", "A6": NC, "B6": NC, "A7": NC, "B7": NC,
               "A8": NC, "B8": NC, "S1": "GND"},
         block="USB", fields={"MPN": "HRO TYPE-C-31-M-12", "LCSC": "C165948"}),
    R("R1", "5.1k", "CC1", "GND", "USB", Note="UFP CC pull-down (USB-C sink)"),
    R("R2", "5.1k", "CC2", "GND", "USB", Note="UFP CC pull-down (USB-C sink)"),
    dict(ref="F1", lib="Device:Polyfuse", value="1.5A hold", fp="Fuse:Fuse_1206_3216Metric",
         pins={"1": "VBUS_IN", "2": "+5V"}, block="USB", fields={"MPN": "SMD1206P150TF"}),
    dict(ref="D1", lib="Device:D_TVS", value="SMAJ5.0A", fp="Diode_SMD:D_SMA",
         pins={"1": "+5V", "2": "GND"}, block="USB", fields={"MPN": "SMAJ5.0A"}),
    C("C1", "10uF", "+5V", "GND", "USB", fp=C0805),
    R("R25", "2k", "+5V", "LED_PWR", "USB"),
    LED("D2", "GREEN PWR", "GND", "LED_PWR", "USB"),

    # ---------------- 2. TP4056 charger ----------------
    dict(ref="U1", lib="CellScopeLite:TP4056", value="TP4056",
         fp="Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3mm",
         pins={"1": "GND", "2": "PROG", "3": "GND", "4": "+5V", "5": "VBAT",
               "6": "STDBY_N", "7": "CHRG_N", "8": "+5V", "9": "GND"},
         block="CHG", fields={"MPN": "TP4056 (ESOP-8)", "LCSC": "C16581",
                              "Note": "TEMP tied to GND = NTC disabled"}),
    R("R3", "1.2k", "PROG", "GND", "CHG", Note="I_CHG = 1200/R_PROG = 1.0 A"),
    C("C2", "10uF", "+5V", "GND", "CHG", fp=C0805),
    C("C3", "10uF", "VBAT", "GND", "CHG", fp=C0805),
    R("R4", "1k", "+5V", "LED_CHRG", "CHG"),
    LED("D3", "RED CHRG", "CHRG_N", "LED_CHRG", "CHG"),
    R("R5", "1k", "+5V", "LED_STDBY", "CHG"),
    LED("D4", "BLUE FULL", "STDBY_N", "LED_STDBY", "CHG"),

    # ---------------- 3. Cell + protection ----------------
    dict(ref="BT1", lib="Device:Battery_Cell", value="18650 Li-ion",
         fp="Battery:BatteryHolder_Keystone_1042_1x18650",
         pins={"1": "VBAT", "2": "BAT_N"}, block="BMS", fields={"MPN": "Keystone 1042"}),
    dict(ref="U2", lib="CellScopeLite:DW01A", value="DW01A", fp="Package_TO_SOT_SMD:SOT-23-6",
         pins={"1": "DW_OD", "2": "DW_CS", "3": "DW_OC", "4": NC, "5": "DW_VCC", "6": "BAT_N"},
         block="BMS", fields={"MPN": "DW01A", "LCSC": "C351410"}),
    R("R6", "100", "VBAT", "DW_VCC", "BMS"),
    C("C4", "100nF", "DW_VCC", "BAT_N", "BMS"),
    R("R7", "2k", "DW_CS", "GND", "BMS"),
    dict(ref="Q1", lib="CellScopeLite:FS8205A", value="FS8205A", fp="Package_SO:TSSOP-8_4.4x3mm_P0.65mm",
         pins={"1": "FET_D", "8": "FET_D", "2": "BAT_N", "3": "BAT_N", "4": "DW_OD",
               "5": "DW_OC", "6": "GND", "7": "GND"},
         block="BMS", fields={"MPN": "FS8205A", "LCSC": "C32254"}),
    C("C11", "22uF", "VBAT", "GND", "BMS", fp=C0805),

    # ---------------- 4. 3.3 V + reference ----------------
    dict(ref="U3", lib="Regulator_Linear:AP2112K-3.3", value="AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5",
         pins={"1": "+5V", "2": "GND", "3": "+5V", "4": NC, "5": "+3V3"},
         block="PWR", fields={"MPN": "AP2112K-3.3TRG1", "LCSC": "C51118"}),
    C("C5", "1uF", "+5V", "GND", "PWR"),
    C("C6", "1uF", "+3V3", "GND", "PWR"),
    R("R8", "2.2k", "+3V3", "VREF", "PWR", Note="I_Z = (3.3-2.048)/2.2k = 0.57 mA"),
    dict(ref="U4", lib="Reference_Voltage:LM4040DBZ-2.0", value="LM4040-2.048", fp="Package_TO_SOT_SMD:SOT-23",
         pins={"1": "VREF", "2": "GND", "3": NC},
         block="PWR", fields={"MPN": "LM4040AIM3-2.0", "Note": "0.1 % shunt reference"}),
    C("C7", "100nF", "VREF", "GND", "PWR"),

    # ---------------- 5. Set-point ----------------
    R("R9", "200k", "VREF", "POT_TOP", "SET", Note="0-97.5 mV full scale = 0-0.975 A"),
    dict(ref="RV1", lib="Device:R_Potentiometer_Trim", value="10k",
         fp="Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical",
         pins={"1": "POT_TOP", "2": "SET_POT", "3": "GND"}, block="SET", fields={"MPN": "Bourns 3296W-1-103"}),
    R("R10", "330k", "EXT_SET", "EXT_DIV", "SET", Note="3.3 V DAC -> 97 mV"),
    R("R11", "10k", "EXT_DIV", "GND", "SET"),
    dict(ref="JP1", lib="Jumper:Jumper_3_Open", value="SET SRC", fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
         pins={"1": "SET_POT", "2": "SETPOINT", "3": "EXT_DIV"}, block="SET",
         fields={"Note": "1-2 = trimmer, 2-3 = external DAC"}),
    R("R12", "10k", "SETPOINT", "SET_FILT", "SET"),
    C("C8", "1uF", "SET_FILT", "GND", "SET", Note="tau = 10 ms soft start"),
    dict(ref="SW1", lib="Switch:SW_SPDT", value="LOAD ON/OFF", fp="Button_Switch_SMD:SW_SPDT_PCM12",
         pins={"1": NC, "2": "SET_FILT", "3": "GND"}, block="SET", fields={"MPN": "C&K PCM12SMTR"}),
    dict(ref="Q2", lib="Transistor_FET:2N7002", value="2N7002", fp="Package_TO_SOT_SMD:SOT-23",
         pins={"1": "UVLO_G", "2": "GND", "3": "SET_FILT"}, block="SET", fields={"LCSC": "C8545"}),

    # ---------------- 6. CC load ----------------
    dict(ref="U5", lib="Amplifier_Operational:MCP6002-xSN", value="MCP6002", fp="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
         pins={"1": "OA_OUT", "2": "OA_FB", "3": "SET_FILT",
               "7": "UVLO", "6": "VBAT_DIV", "5": "CMP_P",
               "8": "+3V3", "4": "GND"},
         block="CCL", fields={"MPN": "MCP6002T-I/SN", "Note": "A = CC loop, B = UVLO comparator"}),
    C("C10", "100nF", "+3V3", "GND", "CCL"),
    R("R13", "1k", "SENSE_HI", "OA_FB", "CCL"),
    C("C9", "10nF", "OA_FB", "OA_OUT", "CCL", Note="loop compensation"),
    R("R14", "100", "OA_OUT", "GATE", "CCL", Note="gate stopper"),
    R("R15", "100k", "GATE", "GND", "CCL"),
    dict(ref="Q3", lib="Transistor_FET:IRLZ44N", value="IRLZ44N", fp="Package_TO_SOT_THT:TO-220-3_Vertical",
         pins={"1": "GATE", "2": "VBAT", "3": "SENSE_HI"}, block="CCL",
         fields={"MPN": "IRLZ44NPBF", "Note": "logic-level; needs TO-220 heatsink >2 W"}),
    R("R16", "0.1 1%", "SENSE_HI", "GND", "CCL", fp="Resistor_SMD:R_2512_6332Metric",
      MPN="2512 0.1R 1% 2W", Note="I = V_SET / 0.1 ohm"),
    dict(ref="NT1", lib="Device:NetTie_2", value="Kelvin", fp="NetTie:NetTie-2_SMD_Pad0.5mm",
         pins={"1": "GND", "2": "SENSE_LO"}, block="CCL", fields={"Note": "Kelvin sense tie at R16"}),

    # ---------------- 7. INA226 ----------------
    dict(ref="U6", lib="Sensor_Energy:INA226", value="INA226", fp="Package_SO:MSOP-10_3x3mm_P0.5mm",
         pins={"1": "GND", "2": "GND", "3": "ALERT", "4": "SDA", "5": "SCL", "6": "+3V3",
               "7": "GND", "8": "VBAT", "9": "SENSE_LO", "10": "SENSE_HI"},
         block="MON", fields={"MPN": "INA226AIDGSR", "LCSC": "C49851", "Note": "I2C address 0x40"}),
    C("C12", "100nF", "+3V3", "GND", "MON"),
    R("R17", "4.7k", "+3V3", "SDA", "MON"),
    R("R18", "4.7k", "+3V3", "SCL", "MON"),
    R("R19", "10k", "+3V3", "ALERT", "MON"),

    # ---------------- 8. UVLO comparator ----------------
    R("R20", "619k 1%", "VBAT", "VBAT_DIV", "UVL", Note="k = 1M/1.619M = 0.6177"),
    R("R21", "1M 1%", "VBAT_DIV", "GND", "UVL"),
    C("C13", "100nF", "VBAT_DIV", "GND", "UVL", Note="noise filter, tau 38 ms"),
    R("R22", "10k", "VREF", "CMP_P", "UVL"),
    R("R23", "100k", "UVLO", "CMP_P", "UVL", Note="trip 3.01 V falling, release 3.50 V (near-latching)"),
    R("R24", "1k", "UVLO", "UVLO_G", "UVL"),
    R("R26", "1k", "UVLO", "LED_UVLO", "UVL"),
    LED("D5", "AMBER CUTOFF", "GND", "LED_UVLO", "UVL"),

    # ---------------- 9. Interface / mech ----------------
    dict(ref="J2", lib="Connector_Generic:Conn_01x06", value="HOST", fp="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical",
         pins={"1": "+3V3", "2": "SDA", "3": "SCL", "4": "ALERT", "5": "EXT_SET", "6": "GND"}, block="IO", fields={}),
    dict(ref="J3", lib="Connector_Generic:Conn_01x04", value="Qwiic", fp="Connector_JST:JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal",
         pins={"1": "GND", "2": "+3V3", "3": "SDA", "4": "SCL"}, block="IO", fields={"MPN": "JST SM04B-SRSS-TB"}),
    TP("TP1", "VBAT", "IO"), TP("TP2", "SENSE_HI", "IO"), TP("TP3", "SET_FILT", "IO"),
    TP("TP4", "GATE", "IO"), TP("TP5", "+3V3", "IO"), TP("TP6", "+5V", "IO"), TP("TP7", "GND", "IO"),
]

for i in range(1, 5):
    PARTS.append(dict(ref="H%d" % i, lib="Mechanical:MountingHole", value="M3", fp="MountingHole:MountingHole_3.2mm_M3",
                      pins={}, block="IO", fields={}))
for i in range(1, 4):
    PARTS.append(dict(ref="FID%d" % i, lib="Mechanical:Fiducial", value="Fiducial", fp="Fiducial:Fiducial_1mm_Mask2mm",
                      pins={}, block="IO", fields={}))


def nets():
    out = {}
    for p in PARTS:
        for pin, n in p["pins"].items():
            if n is not None:
                out.setdefault(n, []).append((p["ref"], pin))
    return out


if __name__ == "__main__":
    ns = nets()
    print(len(PARTS), "parts,", len(ns), "nets")
    for n, m in sorted(ns.items()):
        flag = "  <-- single pin!" if len(m) < 2 else ""
        print("%-10s %s%s" % (n, " ".join("%s.%s" % x for x in m), flag))
