import os
import sys
import time
"""The script allows installing and unistalling the packages. Example of the script call would be: 
"python adb_un_installer com.package.name path/to/the/file.apk". Script determine if the package 
or app is passed and uninstalls/installs the targets. This script is very useful if couple of the 
phones are used under test and the app is needed to be re-installed or removed. Make sure to have 
adb added to the path and USB debugging on your phones."""

def validate_path(path):
	if os.path.exists(path):
		pass
	else: raise SystemExit("The path {} is not found. Try again with correct path.".format(path))

def do_something(app_list, pack_list):
	adb_responce = os.popen("adb devices").read()
	lines = adb_responce.split("\n")
	devices = []
	for line in lines:
		if "\tdevice" in line:
			devices.append(line[:-7])
	print("devices in use: " + str(devices))

	#uninstall apps
	if pack_list is not []:
		for device in devices:
			apps_on_device = os.popen(('adb -s {} shell "pm list packages"').format(device)).read()
			for pack in pack_list:
				#verify if the package is installed
				if pack in apps_on_device:
					print("Unistalling the {} on device {}".format(pack,device))
					uninstall_result = os.popen(("adb -s {} uninstall {}").format(device,pack)).read()
					if "Success" in uninstall_result:
						print("{} has been uninstalled".format(pack))
					else: print("The app is not found and/or not installed")
				else: print("The package is not installed, moving forward")
	else:
		print("No uninstall")
	#re-install apps
	if app_list is not []:
		for device in devices:
			for app in app_list:
				print("Installing the {} on device {}".format(app,device))
				install_result = os.popen(("adb -s {} install -r {}").format(device,app)).read()
	else:
		print("No install")

if __name__ == "__main__":
	if not len(sys.argv) > 1:
		raise SystemExit("Usage: {} [package_name and/or app_path]".format(sys.argv[0]))

	settings = list(sys.argv[1:])
	app_list = []
	pack_list = []

	for setting in settings:
		if ".apk" in setting:
			validate_path(setting)
			app_list.append(setting)
		elif "com." in setting:
			pack_list.append(setting)
		else: ("Not parsed")
	if app_list != [] or pack_list != []:
		do_something(app_list, pack_list)
	else: print("Please pass the package to uninstall or app to install and run the script again")
