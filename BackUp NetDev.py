# By morad rachad
import netdev, asyncio
import getpass, datetime, os, time
import backup_data

print ('############################# NETDEV LIBRARY #############################\n')
print ('############################### '+ str((datetime.datetime.now()).date()) +' ###############################\n')

async def task(devices, passwd):
    for param in devices:
        # The main folder it should be already created 
        os.chdir('C:\Backup')
        backupDirName = str((datetime.datetime.now()).date())
        x = os.path.isdir(backupDirName)
        # The script will create a folder with today's date name and if the folder already exists, it will skip this row.
        if x == False:
            os.mkdir(backupDirName)
        os.chdir(backupDirName)
        # Inside the folder that was created befor it will be create another folder with name of device and if the folder already exists, it will skip this row.        
        z = os.path.isdir(param[1])
        if z == False:
            os.mkdir(param[1])
        os.chdir(param[1])
        # In the device folder, it will create a file with the name "running-config.cfg" and if the file already exists, it will erase the previous backup with the new backup.
        f = open("C:\Backup/"+ backupDirName +"/"+ param[1] +"/running-config.cfg", "w")
        # Connecting to the devices  
        param[0]['password'] = str(passwd)
        async with netdev.create(**param[0]) as ios:
            # moment of start process with this device        
            start_time = time.time()
            print ('+++ Getting the backup from device " '+ str(param[1]) +' " :')
            # the script will send this 2 command into the device.       
            await ios.send_command("terminal length 1000")
            output = await ios.send_command("show run")
            # save the run config into the file that was created for this device.         
            print(output, file=f)
            print ("\t--- %.2f seconds. " % (time.time() - start_time))
            print ('\t--- The backup has been successfully completed. \n')
            # moment of end process with this device.

async def run():
    # import devices information from file " backup_data_amanys.py "    
    devices = [backup_data.R1, backup_data.R2, backup_data.R3, backup_data.R4, backup_data.R5, backup_data.R6]
    passwd = getpass.getpass('Please enter the SSH password: ')
    start_time = time.time()
    tasks = [task(devices, passwd)]
    # run the function " task "
    await asyncio.wait(tasks)
    print ("\n\n+++ The process take %.2f seconds. \n" % (time.time() - start_time))
    input("- Press ENTER to EXIT !!!")
    # moment of end the script

# run the function " run "
loop = asyncio.get_event_loop()
loop.run_until_complete(run())