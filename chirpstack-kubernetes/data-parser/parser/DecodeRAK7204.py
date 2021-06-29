
# convert string to short integer

def parseShort(string, base):
    n = int(string, base)
    return (n << 16) >> 16


# convert string to triple bytes integer

def parseTriple(string, base):
    n = int(string, base)
    return (n << 8) >> 8


# decode Hex sensor string data to object
def DecodeRAK7204(hexStr):
    string = hexStr
    payload_dict = {}

    while ( len(string) > 4 ):
        flag = int(string[0:4], 16)

        if flag == 0x0768: # Humidity
            payload_dict['humidity'] = str(float(("{:.1f}".format(parseShort(string[4:6], 16) * 0.01 / 2))) * 100) + "%RH" # unit:%RH
            string = string[6:]
        elif flag == 0x0673: # Atmospheric pressure
            payload_dict['barometer'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.1)))) + "hPa" # unit:hPa
            string = string[8:]
        elif flag == 0x0267: # Temperature
            payload_dict['temperature'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.1)))) + u"\u2103" 
            string = string[8:]
        elif flag == 0x0188: # GPS
            payload_dict['latitude'] = str(float("{:.4f}".format((parseTriple(string[4:10], 16) * 0.0001)))) + u"\u00b0" # unit:Degree
            payload_dict['longitude'] = str(float("{:.4f}".format((parseTriple(string[10:16], 16) * 0.0001)))) + u"\u00b0" # unit:Degree
            payload_dict['altitude'] = str(float("{:.1f}".format((parseTriple(string[16:22], 16) * 0.01)))) + "m" # unit:m
            string = string[22:]
        elif flag == 0x0371: # Triaxial acceleration
            payload_dict['acceleration_x'] = str(float("{:.3f}".format((parseShort(string[4:8], 16) * 0.001)))) + "g" # unit:g
            payload_dict['acceleration_y'] = str(float("{:.3f}".format((parseShort(string[8:12], 16) * 0.001)))) + "g" # unit:g
            payload_dict['acceleration_z'] = str(float("{:.3f}".format((parseShort(string[12:16], 16) * 0.001)))) + "g" # unit:g
            string = string[16:]
        elif flag == 0x0402: # air resistance
            payload_dict['gasResistance'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01)))) + "kiloohm" # unit:kiloohm
            string = string[8:]
        elif flag == 0x0802: # Battery Voltage
            payload_dict['battery'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01)))) + "V" # unit:V
            string = string[8:]
        elif flag == 0x0586: # gyroscope
            payload_dict['gyroscope_x'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01)))) + u"\u00b0" + "/s" # unit:Degree/s
            payload_dict['gyroscope_y'] = str(float("{:.2f}".format((parseShort(string[8:12], 16) * 0.01)))) + u"\u00b0" + "/s" # unit:Degree/s
            payload_dict['gyroscope_z'] = str(float("{:.2f}".format((parseShort(string[12:16], 16) * 0.01)))) + u"\u00b0" + "/s" # unit:Degree/s
            string = string[16:]
        elif flag == 0x0902: # magnetometer x
            payload_dict['magnetometer_x'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01)))) + "Mu-Tesla" # unit:Mu-Tesla
            string = string[8:]
        elif flag == 0x0a02: # magnetometer y
            payload_dict['magnetometer_y'] = str(float("{:.2f}".format((parseShort(string[4:8], 16) * 0.01)))) + "Mu-Tesla" # unit:Mu-Tesla
            string = string[8:]
        elif flag == 0x0b02: # magnetometer z
            payload_dict['magnetometer_z'] = str(float("{:.2f}".format((parseShort(str.substring(4, 8), 16) * 0.01)))) + "Mu-Tesla" # unit:Mu-Tesla
            string = string[8:]
        else:
            string = string[7:]

    return payload_dict
