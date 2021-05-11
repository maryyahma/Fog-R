# Decode decodes an array of bytes into an object=payload_dict.
#  - fPort contains the LoRaWAN fPort number
#  - bytes is an array of bytes, e.g. [255, 230, 255, 0]
# The function must return an object=payload_dict, e.g. {"temperature": 22.5}


def DecodeRAK7204(fPort, Bytes):
    decoded = {}
    hexString = bin2HexStr(Bytes)
    return rakSensorDataDecode(hexString)


# convert array of bytes to hex string.
# e.g: 0188053797109D5900DC140802017A0768580673256D0267011D040214AF0371FFFFFFDDFC2E

def bin2HexStr(bytesArr):
    string = ""
    for i in range(0, len(bytesArr)):
        tmp = format( bytesArr[i] & 0xff , 'x')

        if (len(tmp) == 1):
            tmp = "0" + tmp

        string = string + tmp

    return string


# convert string to short integer

def parseShort(string, base):
    n = int(string, base)
    return (n << 16) >> 16


# convert string to triple bytes integer

def parseTriple(string, base):
    n = int(string, base)
    return (n << 8) >> 8


# decode Hex sensor string data to object
def rakSensorDataDecode(hexStr):
    string = hexStr
    payload_dict = {}

    while ( len(string) > 4 ):
        flag = int(string[0:4], 16)

        if flag == 0x0768: # Humidity
            payload_dict['humidity'] = float(("{:.1f}".format(parseShort(string[4:6], 16) * 0.01 / 2) * 100)) + "%RH" # unit:%RH
            string = string[6:]
        elif flag == 0x0673: # Atmospheric pressure
            payload_dict['barometer'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.1))) + "hPa" # unit:hPa
            string = string[8:]
        elif flag == 0x0267: # Temperature
            payload_dict['temperature'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.1))) + u"\u2103" 
            string = string[8:]
        elif flag == 0x0188: # GPS
            payload_dict['latitude'] = float("{:.4f}".format((parseTriple(string[4:10], 16) * 0.0001))) + u"\u00b0" # unit:Degree
            payload_dict['longitude'] = float("{:.4f}".format((parseTriple(string[10:16], 16) * 0.0001))) + u"\u00b0" # unit:Degree
            payload_dict['altitude'] = float("{:.1f}".format((parseTriple(string[16:22], 16) * 0.01))) + "m" # unit:m
            string = string[22:]
        elif flag == 0x0371: # Triaxial acceleration
            payload_dict['acceleration_x'] = float("{:.3f}".format((parseShort(string[4:8], 16) * 0.001))) + "g" # unit:g
            payload_dict['acceleration_y'] = float("{:.3f}".format((parseShort(string[8:12], 16) * 0.001))) + "g" # unit:g
            payload_dict['acceleration_z'] = float("{:.3f}".format((parseShort(string[12:16], 16) * 0.001))) + "g" # unit:g
            string = string[16:]
        elif flag == 0x0402: # air resistance
            payload_dict['gasResistance'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01))) + "kiloohm" # unit:kiloohm
            string = string[8:]
        elif flag == 0x0802: # Battery Voltage
            payload_dict['battery'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01))) + "V" # unit:V
            string = string[8:]
        elif flag == 0x0586: # gyroscope
            payload_dict['gyroscope_x'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01))) + u"\u00b0" + "/s" # unit:Degree/s
            payload_dict['gyroscope_y'] = float("{:.2f}".format((parseShort(string[8:12], 16) * 0.01))) + u"\u00b0" + "/s" # unit:Degree/s
            payload_dict['gyroscope_z'] = float("{:.2f}".format((parseShort(string[12:16], 16) * 0.01))) + u"\u00b0" + "/s" # unit:Degree/s
            string = string[16:]
        elif flag == 0x0902: # magnetometer x
            payload_dict['magnetometer_x'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01))) + "Mu-Tesla" # unit:Mu-Tesla
            string = string[8:]
        elif flag == 0x0a02: # magnetometer y
            payload_dict['magnetometer_y'] = float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01))) + "Mu-Tesla" # unit:Mu-Tesla
            string = string[8:]
        elif flag == 0x0b02: # magnetometer z
            payload_dict['magnetometer_z'] = float("{:.2f}".format((parseShort(str.substring(4, 8), 16) * 0.01))) + "Mu-Tesla" # unit:Mu-Tesla
            string = string[8:]
        else:
            string = string[7:]

    return payload_dict
