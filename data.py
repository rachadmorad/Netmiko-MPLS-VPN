R1_details = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.60.101',
}

R2_details = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.60.102',
}


R3_details = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.60.103',
}

R4_details = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.60.104',
}

R5_details = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.60.105',
}

R6_details = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.60.106',
}

VPN1 = {
    'device_type': 'cisco_ios',
}


VPN2 = {
    'device_type': 'cisco_ios',
}

R1_interfaces = {
    '2': 'g0/0',
    '3': 'g1/0',
}

R2_interfaces = {
    '1': 'g0/0',
    '3': 'g3/0',
    '4': 'g1/0',
    '5': 'g2/0',
}


R3_interfaces = {
    '1': 'g1/0',
    '2': 'g3/0',
    '4': 'g2/0',
    '5': 'g0/0',
}

R4_interfaces = {
    '6': 'g0/0',
    '2': 'g1/0',
    '3': 'g2/0',
    '5': 'g3/0',
}

R5_interfaces = {
    '6': 'g1/0',
    '2': 'g2/0',
    '3': 'g0/0',
    '4': 'g3/0',
}

R6_interfaces = {
    '4': 'g0/0',
    '5': 'g1/0',
}

R1 = (R1_details, R1_interfaces)
R2 = (R2_details, R2_interfaces)
R3 = (R3_details, R3_interfaces)
R4 = (R4_details, R4_interfaces)
R5 = (R5_details, R5_interfaces)
R6 = (R6_details, R6_interfaces)