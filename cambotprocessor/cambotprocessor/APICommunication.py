import requests
import configparser
import os
import zipfile

#Creates Directory if Directory doesnt exist
def silent_mkdir(theDir):
	try:
		os.mkdir(theDir)
	except:
		pass
	return 0

#retrieves inventoryitem from URL and unzips
def get_inventory(URL,id,dir):
	response = requests.get(f"{URL}/inventory/{id}")
	Filename = "InventoryItem" + id
	#if response valid
	if response.status_code == 201:
		#save Zipfile
		open((Filename + ".zip"),'wb').write(response.content)
		#create directory to extract Zipfile content
		os.mkdir(dir + "/" + Filename)
		#extract Zipfile content under directory
		with zipfile.ZipFile(Filename + ".zip",'r') as zip_ref:
			zip_ref.extractall(dir + "/" + Filename)
		#remove now empty zip
		os.remove(Filename + ".zip")
		print(f"Queue has been succesfully saved under {dir}{FileName}")
	#if Inventoryitem isnt found
	elif response.status_code == 404:
		print("This Inventoryitem does not exist")
	#in case of other error
	else:
		print("something went wrong fetching the Inventory, try again at a later time")


def main():
	#Parser to detect parameters
	parser = argparse.ArgumentParser()

	#All available Parameters
	parser.add_argument('--URL',help='URL of API', default="",type=str)
	parser.add_argument('--id',help='ID for inventory item', default="",type=str)
	parser.add_argument('--outputdirectory',help='declare directory where get output is saved',type=str)

	#Save Parameters in Dictionary
	args = parser.parse_args()

	silent_mkdir(args.outputdirectory)
	get_inventory(args.URL,args.id,args.outputdirectory)

main()





