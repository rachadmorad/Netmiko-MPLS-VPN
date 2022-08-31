# By morad rachad
from netmiko import ConnectHandler
import data, time, getpass

print ('\n############################# IPsec VPN WIZARD ############################\n')

def isakmp_policy(Pre_shared_Key, peer_ip):
	return ['crypto isakmp policy 1','encryption aes 256', 'hash sha256', 'authentication pre-share', 'group 2', 'lifetime 3600', 'exit',
			'crypto isakmp key '+str(Pre_shared_Key)+' address '+ str(peer_ip)]

def ipsec_transform_set():
	return ['crypto ipsec transform-set NETMIKO-GRE-VPN esp-aes 256 esp-sha256-hmac', 'mode transport', 'exit']

def VPN_ACL(local_ip, peer_ip):
	return ['ip access-list extended NETMIKO-GRE-VPN-ACL','permit gre host '+str(local_ip)+' host '+str(peer_ip), 'exit']

def VPN_MAP(peer_ip, Incoming_Int):
	return ['crypto map NETMIKO-GRE-CMAP 10 ipsec-isakmp','match address NETMIKO-GRE-VPN-ACL', 'set transform-set NETMIKO-GRE-VPN', 'set peer '+str(peer_ip), 'exit',
			'int '+ str(Incoming_Int), 'crypto map NETMIKO-GRE-CMAP', 'exit']
def OSPF(ospf_id, router_id):
	return ['router ospf '+str(ospf_id), 'router-id '+str(router_id), 'exit']

def VPN_TUNNEL(idx, local_ip, peer_ip, ospf_id):
	return ['int tunnel1', 'ip address 172.16.254.'+str(idx)+' 255.255.255.252', 'ip mtu 1400', 'tunnel source '+str(local_ip),
			'tunnel destination '+ str(peer_ip), 'ip ospf '+str(ospf_id)+' ar 0', 'exit']

def configure_routers(ROUTERS):
	idx = 0
	for ROUTER in ROUTERS:
		idx += 1
		ssh_ip = input ("\t +++ Please enter the ipv4/hostname for ssh in ROUTER " + str(idx)+" : ")
		ssh_user = input ("\t +++ Please enter the ssh username in ROUTER " + str(idx)+" : ")
		ssh_pass = getpass.getpass("\t +++ Please enter the ssh password in ROUTER " + str(idx)+" : ")
		ROUTER['ip'] = str(ssh_ip)
		ROUTER['username'] = str(ssh_user)
		ROUTER['password'] = str(ssh_pass)
		net_connect = ConnectHandler(**ROUTER)
		start_time = time.time()
		config_commands = []
		print("\n\t +++ Applying the configuration to ROUTER " + str(idx))
		Incoming_Int = input ("\t ++++++ Please enter the name of Incoming Interface on the router"+str(idx)+"(ex:s0/0/0): ")
		peer_ip = input ("\t ++++++ Please enter the peer IPv4 address (remote site): ")
		local_ip = input ("\t ++++++ Please enter the IPv4 address in Incoming Interface (local site): ")
		Pre_shared_Key = input ("\t +++ Please enter the Pre-shared Key(strong_password): ")
		ospf_id = input ("\t ++++++ Please enter the OSPF autonomous system (1-65535): ")
		config_commands += isakmp_policy(str(Pre_shared_Key), str(peer_ip))
		config_commands += ipsec_transform_set()
		config_commands += VPN_ACL(str(local_ip), str(peer_ip))
		config_commands += VPN_MAP(str(peer_ip), str(Incoming_Int))
		config_commands += OSPF(str(ospf_id), str(idx)+'.'+str(idx)+'.'+str(idx)+'.'+str(idx))
		config_commands += VPN_TUNNEL(str(idx), str(local_ip), str(peer_ip), str(ospf_id))
		output = net_connect.send_config_set(config_commands)
		print(output+'\n')
		net_connect.disconnect()
		print('\t\t########## Router '+ str(idx) +' has been configured! ##########')
		print('#######################################################################\n\n')
	print ("\n\n+++ The process take %.2f seconds. \n" % (time.time() - start_time))
		

ROUTERS = [data.VPN1, data.VPN2]

configure_routers(ROUTERS)
input('Type ENTER to quit')
