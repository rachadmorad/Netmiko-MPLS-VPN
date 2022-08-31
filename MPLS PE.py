# By morad rachad
from netmiko import ConnectHandler
import data, time, getpass

print ('\n############################# MPLS Provider Edge VPN CONFIGURATION ############################\n')

def config_interface(interface, address, vrf_name):
	return ['int '+ str(interface), 'no shut', 'ip vrf forwarding ' + str(vrf_name), 'ip add '+ str(address) +' 255.255.255.0', 'exit']

def config_vrf(name, rd, rt):
	return ['ip vrf '+  name, 'rd '+ rd, 'route-target both '+ rt, 'exit']

def config_bgp(bgp_id, neighbor_id, vrf_name, eigrp_id):
	return ['router bgp '+ bgp_id, 'neighbor '+ neighbor_id + ' remote-as '+bgp_id, 'neighbor '+ neighbor_id + ' update-source l0', 'address-family vpnv4',
            'neighbor '+ neighbor_id + ' activate', 'neighbor '+ neighbor_id + ' send-community both', 'address-family ipv4 vrf ' + str(vrf_name),
			'redistribute eigrp '+ str(eigrp_id) + ' metric 10', 'exit']

def config_eigrp(eigrp_id, bgp_id, vrf_name):
	return ['router eigrp 1', 'address-family ipv4 vrf '+ str(vrf_name), 'autonomous-system  ' + str(eigrp_id), 'no auto-summary ',
			'network 0.0.0.0 0.0.0.0', 'redistribute bgp '+str(bgp_id)+ ' metric 10000 1 255 1 1500', 'exit']
def configure_routers(ROUTERS):
	idx = 0
	ssh_user = input ("\t +++ Please enter the ssh username: ")
	ssh_pass = getpass.getpass("\t +++ Please enter the ssh password: ")
	cmd = [input ("\t +++ Please enter the router's ID number for the first PE (1-1000):"),
	       input ("\t +++ Please enter the router's ID number for the second PE (1-1000): "),
           input ("\t +++ Please enter the BGP autonomous system : "),
           input ("\t +++ Please enter the vrf name : "),
           input ("\t +++ Please enter the vrf route distinguishers : "),
           input ("\t +++ Please enter the vrf route target : ")
           ]
	cmd1 = [
           input ("\t +++ Please enter the interface name in the PE" +cmd[0]+ " directly connected to the CE: "),
           input ("\t +++ Please enter the IPv4 address between PE-CE in the PE" +cmd[0]+ " : "),
           input ("\t +++ Please enter the interface name in the PE" +cmd[1]+ " directly connected to the CE: "),
           input ("\t +++ Please enter the IPv4 address between PE-CE in the PE" +cmd[1]+ " : "),
           input ("\t +++ Please enter the EIGRP autonomous system for PE-CE connection : ")
		   ]
	for ROUTER in ROUTERS:
		idx += 1
		if int(idx) == int(cmd[0]):
			ROUTER[0]['username'] = str(ssh_user)
			ROUTER[0]['password'] = str(ssh_pass)
			print("\n\t ++++++ Applying the configuration to ROUTER " + str(idx)+"\n")
			net_connect = ConnectHandler(**ROUTER[0])
			start_time = time.time()
			config_commands = []
			config_commands += config_vrf(str(cmd[3]), str(cmd[4]), str(cmd[5]))
			config_commands += config_interface(str(cmd1[0]), str(cmd1[1]), str(cmd[3]))
			config_commands += config_eigrp(str(cmd1[4]), str(cmd[2]), str(cmd[3]))
			config_commands += config_bgp(str(cmd[2]), str(cmd[1])+'.'+str(cmd[1])+'.'+str(cmd[1])+'.'+str(cmd[1]), str(cmd[3]), str(cmd1[4]))
			output = net_connect.send_config_set(config_commands)
			print(output+'\n')
			net_connect.disconnect()
			print('\t\t########## Router '+ str(idx) +' has been configured! ##########')
			print('#######################################################################\n')
		elif int(idx) == int(cmd[1]):
			ROUTER[0]['username'] = str(ssh_user)
			ROUTER[0]['password'] = str(ssh_pass)
			print("\n\t ++++++ Applying the configuration to ROUTER " + str(idx)+"\n")
			net_connect = ConnectHandler(**ROUTER[0])
			start_time = time.time()
			config_commands = []
			config_commands += config_vrf(str(cmd[3]), str(cmd[4]), str(cmd[5]))
			config_commands += config_interface(str(cmd1[2]), str(cmd1[3]), str(cmd[3]))
			config_commands += config_eigrp(str(cmd1[4]), str(cmd[2]), str(cmd[3]))
			config_commands += config_bgp(str(cmd[2]), str(cmd[0])+'.'+str(cmd[0])+'.'+str(cmd[0])+'.'+str(cmd[0]), str(cmd[3]), str(cmd1[4]))
			output = net_connect.send_config_set(config_commands)
			print(output+'\n')
			net_connect.disconnect()
			print('\t\t########## Router '+ str(idx) +' has been configured! ##########')
			print('#######################################################################\n')
	print ("\n\n+++ The process take %.2f seconds. \n" % (time.time() - start_time))
		

ROUTERS = [data.R1, data.R2, data.R3, data.R4, data.R5, data.R6]

configure_routers(ROUTERS)
input('Type ENTER to quit')
