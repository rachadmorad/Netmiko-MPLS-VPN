# By morad rachad
from netmiko import ConnectHandler
import data, time, getpass

print ('############################# MPLS BACKBONE CONFIGURATION ############################\n')

def config_interface(interface, address, ospf):
	return ['int '+ interface, 'ip add '+ address +' 255.255.255.0', 'ip ospf '+ ospf + ' area 0', 'no shut', 'exit']

def config_interface_l0(address, ospf):
	return ['int l0', 'ip add '+ address +' 255.255.255.255', 'ip ospf '+ ospf + ' area 0', 'no shut', 'exit']

def config_ospf(ospf_id, router_id):
	return ['router ospf '+  ospf_id, 'router-id '+ router_id, 'mpls ldp autoconfig area 0', 'exit']

def config_mpls():
	return ['mpls ip', 'ip cef']

def configure_routers(ROUTERS):
	idx = 0
	ssh_user = input ("\t +++ Please enter the ssh username: ")
	ssh_pass = getpass.getpass("\t +++ Please enter the ssh password: ")
	ospf_id = input ("\t +++ Please enter the OSPF autonomous system inside the backbone connectivity (1-65535): ")
	for ROUTER in ROUTERS:
		idx += 1
		print("\n\t ++++++ Applying the configuration to ROUTER " + str(idx)+"\n")
		ROUTER[0]['username'] = str(ssh_user)
		ROUTER[0]['password'] = str(ssh_pass)
		net_connect = ConnectHandler(**ROUTER[0])
		start_time = time.time()
		config_commands = []
		for router_id, interface in ROUTER[1].items():
			min_value, max_value = min(idx, int(router_id)), max(idx, int(router_id))
			config_commands += config_interface(interface, '10.0.'+ str(min_value) + str(max_value) +'.'+ str(idx), str(ospf_id))
		config_commands += config_interface_l0(str(idx)+'.'+str(idx)+'.'+str(idx)+'.'+str(idx), str(ospf_id))
		config_commands += config_mpls()
		config_commands += config_ospf(str(ospf_id), str(idx)+'.'+str(idx)+'.'+str(idx)+'.'+str(idx))
		output = net_connect.send_config_set(config_commands)
		print(output+'\n')
		net_connect.disconnect()
		print('\t\t########## Router '+ str(idx) +' has been configured! ##########')
		print('#######################################################################\n')
	print ("\n\n+++ The process take %.2f seconds. \n" % (time.time() - start_time))

ROUTERS = [data.R1, data.R2, data.R3, data.R4, data.R5, data.R6]

configure_routers(ROUTERS)
input('Type ENTER to quit')