import os
import zipfile

def silent_mkdir(theDir):
	try:
		os.mkdir(theDir)
	except:
		pass
	return 0

def get_inventory(id,dir):
		empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		Filename = "InventoryItem" + id
		open((Filename + ".zip"),'wb').write(empty_zip_data)
		os.mkdir(dir + "/" + Filename)
		with zipfile.ZipFile(Filename + ".zip",'r') as zip_ref:
			zip_ref.extractall(dir + "/" + Filename)
		os.remove(Filename + ".zip")

get_inventory("test","../TestRun")