import sys, os
import subprocess
import shutil
import argparse
import numpy as np
from BlurDetection import remove_blur 
import configparser
import meshio

#Creates Directory if Directory doesnt exist
def silent_mkdir(theDir):
	try:
		os.mkdir(theDir)
	except:
		pass
	return 0

#StandardQueue Step 0
def run_00_camerainit(baseDir,binDir,srcImageDir):
	silent_mkdir(baseDir + "/00_CameraInit")

	binName = binDir + "/aliceVision_cameraInit.exe"

	dstDir = baseDir + "/00_CameraInit/"
	cmdLine = binName
	cmdLine = cmdLine + " --defaultFieldOfView 45.0 --verboseLevel info --sensorDatabase \"\" --allowSingleView 1"
	cmdLine = cmdLine + " --imageFolder \"" + srcImageDir + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "cameraInit.sfm\""
	print(cmdLine)
	subprocess.call(cmdLine)

	return 0

#StandardQueue Step 1
def run_01_featureextraction(baseDir,binDir, numImages):
	silent_mkdir(baseDir + "/01_FeatureExtraction")

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm"

	binName = binDir + "/aliceVision_featureExtraction.exe"

	dstDir = baseDir + "/01_FeatureExtraction/"

	cmdLine = binName
	cmdLine = cmdLine + " --describerTypes sift --forceCpuExtraction True --verboseLevel info --describerPreset normal"
	cmdLine = cmdLine + " --rangeStart 0 --rangeSize " + str(numImages)
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""
	print(cmdLine)
	subprocess.call(cmdLine)

	return 0

#StandardQueue Step 2
def run_02_imagematching(baseDir,binDir):
	silent_mkdir(baseDir + "/02_ImageMatching")

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm"
	srcFeatures = baseDir + "/01_FeatureExtraction/"
	dstMatches = baseDir + "/02_ImageMatching/imageMatches.txt"

	binName = binDir + "/aliceVision_imageMatching.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --minNbImages 200 --tree "" --maxDescriptors 500 --verboseLevel info --weights "" --nbMatches 50"
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --featuresFolder \"" + srcFeatures + "\""
	cmdLine = cmdLine + " --output \"" + dstMatches + "\""

	print(cmdLine)
	subprocess.call(cmdLine)

	return 0

#StandardQueue Step 3
def run_03_featurematching(baseDir,binDir):
	silent_mkdir(baseDir + "/03_FeatureMatching")

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm"
	srcFeatures = baseDir + "/01_FeatureExtraction/"
	srcImageMatches = baseDir + "/02_ImageMatching/imageMatches.txt"
	dstMatches = baseDir + "/03_FeatureMatching"

	binName = binDir + "\\aliceVision_featureMatching.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --verboseLevel info --describerTypes sift --maxMatches 0 --exportDebugFiles False --savePutativeMatches False --guidedMatching False"
	cmdLine = cmdLine + " --geometricEstimator acransac --geometricFilterType fundamental_matrix --maxIteration 2048 --distanceRatio 0.8"
	cmdLine = cmdLine + " --photometricMatchingMethod ANN_L2"
	cmdLine = cmdLine + " --imagePairsList \"" + srcImageMatches + "\""
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --featuresFolders \"" + srcFeatures + "\""
	cmdLine = cmdLine + " --output \"" + dstMatches + "\""

	print(cmdLine)
	subprocess.call(cmdLine)
	return 0

#StandardQueue Step 4
def run_04_structure_from_motion(baseDir,binDir):
	silent_mkdir(baseDir + "/04_StructureFromMotion")

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm"
	srcFeatures = baseDir + "/01_FeatureExtraction/"
	srcImageMatches = baseDir + "/02_ImageMatching/imageMatches.txt"
	srcMatches = baseDir + "/03_FeatureMatching"
	dstDir = baseDir + "/04_StructureFromMotion"

	binName = binDir + "\\aliceVision_incrementalSfm.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --minAngleForLandmark 2.0 --minNumberOfObservationsForTriangulation 2 --maxAngleInitialPair 40.0 --maxNumberOfMatches 0 --localizerEstimator acransac --describerTypes sift --lockScenePreviouslyReconstructed False --localBAGraphDistance 1"
	cmdLine = cmdLine + " --interFileExtension .ply --useLocalBA True"
	cmdLine = cmdLine + " --minInputTrackLength 2 --useOnlyMatchesFromInputFolder False --verboseLevel info --minAngleForTriangulation 3.0 --maxReprojectionError 4.0 --minAngleInitialPair 5.0"
	
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --featuresFolders \"" + srcFeatures + "\""
	cmdLine = cmdLine + " --matchesFolders \"" + srcMatches + "\""
	cmdLine = cmdLine + " --outputViewsAndPoses \"" + dstDir + "/cameras.sfm\""
	cmdLine = cmdLine + " --extraInfoFolder \"" + dstDir + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "/bundle.sfm\""

	print(cmdLine)
	subprocess.call(cmdLine)
	return 0

#StandardQueue Step 5
def run_05_prepare_densescene(baseDir,binDir):
	silent_mkdir(baseDir + "/05_PrepareDenseScene")

	srcSfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	dstDir = baseDir + "/05_PrepareDenseScene"

	binName = binDir + "\\aliceVision_prepareDenseScene.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --verboseLevel info"
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir +"\""

	print(cmdLine)
	subprocess.call(cmdLine)
	return 0

#StandardQueue Step 6
def run_06_depthmap(baseDir,binDir,numImages,groupSize):
	silent_mkdir(baseDir + "/06_DepthMap")

	numGroups = (numImages + (groupSize-1))/groupSize

	srcsfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	imgFld = baseDir + "/05_PrepareDenseScene/"
	binName = binDir + "\\aliceVision_depthMapEstimation.exe"
	dstDir = baseDir + "/06_DepthMap"

	cmdLine = binName
	cmdLine = cmdLine + " --sgmGammaC 5.5 --sgmWSH 4 --refineGammaP 8.0 --refineSigma 15 --refineNSamplesHalf 150 --sgmMaxTCams 10 --refineWSH 3 --downscale 2 --refineMaxTCams 6 --verboseLevel info --refineGammaC 15.5 --sgmGammaP 8.0"
	cmdLine = cmdLine + " --refineNiters 100 --refineNDepthsToRefine 31 --refineUseTcOrRcPixSize False"
	
	cmdLine = cmdLine + " --input \"" + srcsfm + "\""
	cmdLine = cmdLine + " --imagesFolder \"" + imgFld + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""


	for groupIter in range(int(numGroups)):
		groupStart = groupSize * groupIter
		groupSize = min(groupSize,numImages - groupStart)
		print("DepthMap Group %d/%d: %d, %d" % (groupIter, numGroups, groupStart, groupSize))

		cmd = cmdLine + (" --rangeStart %d --rangeSize %d" % (groupStart,groupSize))
		print(cmd)
		subprocess.call(cmd)


	return 0

#StandardQueue Step 7
def run_07_depthmapfilter(baseDir,binDir):
	silent_mkdir(baseDir + "/07_DepthMapFilter")

	binName = binDir + "\\aliceVision_depthMapFiltering.exe"
	dstDir = baseDir + "/07_DepthMapFilter"
	srcSfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	srcDepthDir = baseDir + "/06_DepthMap"

	cmdLine = binName
	cmdLine = cmdLine + " --minNumOfConsistentCamsWithLowSimilarity 4"
	cmdLine = cmdLine + " --minNumOfConsistentCams 3 --verboseLevel info --pixSizeBall 0"
	cmdLine = cmdLine + " --pixSizeBallWithLowSimilarity 0 --nNearestCams 10"

	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""
	cmdLine = cmdLine + " --depthMapsFolder \"" + srcDepthDir + "\""

	print(cmdLine)
	subprocess.call(cmdLine)
	return 0

#StandardQueue Step 8
def run_08_meshing(baseDir,binDir,bounding):
	silent_mkdir(baseDir + "/08_Meshing")

	binName = binDir + "\\aliceVision_meshing.exe"
	srcSfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	srcDepthFilterDir = baseDir + "/07_DepthMapFilter"

	dstDir = baseDir + "/08_Meshing"

	cmdLine = binName
	if bounding != "":
		cmdLine = cmdLine + " --boundingBox " + bounding
	cmdLine = cmdLine + " --simGaussianSizeInit 10.0 --maxInputPoints 50000000 --repartition multiResolution"
	cmdLine = cmdLine + " --simGaussianSize 10.0 --simFactor 15.0 --voteMarginFactor 4.0 --contributeMarginFactor 2.0 --minStep 2 --pixSizeMarginFinalCoef 4.0 --maxPoints 5000000 --maxPointsPerVoxel 1000000 --angleFactor 15.0 --partitioning singleBlock"
	cmdLine = cmdLine + " --minAngleThreshold 1.0 --pixSizeMarginInitCoef 2.0 --refineFuse True --verboseLevel info"

	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""
	cmdLine = cmdLine + " --depthMapsFolder \"" + srcDepthFilterDir + "\""
	cmdLine = cmdLine + " --outputMesh \"" + dstDir + "/Mesh.obj\""
	
	print(cmdLine)
	subprocess.call(cmdLine)
	return 0

#StandardQueue Step 9
def run_09_meshfiltering(baseDir,binDir):
	silent_mkdir(baseDir + "/09_MeshFiltering")

	binName = binDir + "\\aliceVision_meshFiltering.exe"

	srcMesh = baseDir + "/08_Meshing/Mesh.obj"
	dstMesh = baseDir + "/09_MeshFiltering/Mesh.obj"

	cmdLine = binName
	cmdLine = cmdLine + " --verboseLevel info --filterLargeTrianglesFactor 60.0 --filteringIterations 5 --keepLargestMeshOnly True"
	cmdLine = cmdLine + " --smoothingLambda 1.0"

	cmdLine = cmdLine + " --input \"" + srcMesh + "\""
	cmdLine = cmdLine + " --output \"" + dstMesh + "\""

	print(cmdLine)
	subprocess.call(cmdLine)

	return 0

#StandardQueue Step 10
def run_10_texturing(baseDir,binDir):
	binName = binDir + "\\aliceVision_texturing.exe"

	srcMesh = baseDir + "/09_MeshFiltering/Mesh.obj"
	srcSfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	dstDir = baseDir

	cmdLine = binName
	cmdLine = cmdLine + " --textureSide 8192"
	cmdLine = cmdLine + " --downscale 2 --verboseLevel info --padding 15"
	cmdLine = cmdLine + " --unwrapMethod Basic --outputTextureFileType png --flipNormals False --fillHoles False"

	cmdLine = cmdLine + " --inputMesh \"" + srcMesh + "\""
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""

	print(cmdLine)
	subprocess.call(cmdLine)

	return 0

def run_custom_queue(binDir,queue,input,blur):
	#first remove blur
	remove_blur(input,blur)
	commandqueue = queue.split(",")
	#each command given will be called in CLS
	for command in commandqueue:
		print("command: " + command)
		subprocess.call(command)
	return 0

def convertMesh(outputtype,output):
	#Takes filtered Mesh and saves it in a new format
	mesh = meshio.read(output + "/09_MeshFiltering" + "/Mesh.obj")
	mesh.write(output + "/Mesh." + outputtype)

def main():
	#Parser to detect parameters
	parser = argparse.ArgumentParser()

	#All available Parameters
	parser.add_argument('--config',help='configFile with Meshroom-parameters',default="",type=str)
	parser.add_argument('--blur',help='declares Blurdetection value',type=float, required = True)
	parser.add_argument('--outputtype',help='file extension for final 3D object',default="",type=str)
	parser.add_argument('--meshroomqueue',help='custom Meshroomqueue',default="",type=str)
	parser.add_argument('--bounding',help='declaration of Boundingbox',default="")
	parser.add_argument('--input',help='directory of images',type=str, required = True)
	parser.add_argument('--output',help='directory of output',type=str, required = True)
	parser.add_argument('--binary',help='directory of the Meshroom binary',type=str, required = True)

	#parse arguments into dictionary
	args = parser.parse_args()

	#Show Parameter inputs
	print("Base dir  : %s" % args.output)
	print("Image dir : %s" % args.input)
	print("Bin dir   : %s" % args.binary)
	print("Blur      : %s" % args.blur)
	print("outputtype: %s" % args.outputtype)
	print("Bounding  : %s" % args.bounding)

	#if custom queue is available run custom queue
	if (args.meshroomqueue != ""):
	    run_custom_queue(args.binary,args.meshroomqueue,args.input,args.blur)
	#if no custom queue but config is available then run config standard queue
	elif (args.config != "" and args.meshroomqueue == ""):
		config_standard_queue(args.config)
	else:
	#default case run standardqueue
		standard_queue(args)
	
	return 0

def standard_queue(args):
	#first remove blur
	remove_blur(args.input,args.blur)

	#count number of images (necessary for various Meshroomsteps)
	numImages = len([name for name in os.listdir(args.input)])

	silent_mkdir(args.output)

	#Standardqueue
	run_00_camerainit(args.output,args.binary,args.input)
	run_01_featureextraction(args.output,args.binary,numImages)
	run_02_imagematching(args.output,args.binary)
	run_03_featurematching(args.output,args.binary)
	run_04_structure_from_motion(args.output,args.binary)
	run_05_prepare_densescene(args.output,args.binary)
	run_06_depthmap(args.output,args.binary,numImages,3)
	run_07_depthmapfilter(args.output,args.binary)
	run_08_meshing(args.output,args.binary,args.bounding)
	run_09_meshfiltering(args.output,args.binary)
	if args.outputtype != "":
		#Convert Mesh if different outputtype is given
	    convertMesh(args.outputtype,args.output)
	else:
		#else add texture to final Mesh
		run_10_texturing(args.output,args.binary)


def config_standard_queue(configFile):
	#extract values from configfile
	config = configparser.ConfigParser()
	config.sections()
	config.read(configFile)
	input = config["FileManagement"]["input"]
	output = config["FileManagement"]["output"]
	binary = config["FileManagement"]["binary"]
	blur = int(config["ObligatoryParameters"]["blur"])
	bounding = config["OptionalParameters"]["bounding"]
	outputtype = config["ObligatoryParameters"]["outputtype"]
	meshroomqueue = config["OptionalParameters"]["meshroomqueue"]

	if meshroomqueue == "":
		#first remove blur
		remove_blur(input,blur)

		#count number of images (necessary for various Meshroomsteps)
		numImages = len([name for name in os.listdir(input)])

		silent_mkdir(output)
	
		#Standardqueue
		run_00_camerainit(output,binary,input)
		run_01_featureextraction(output,binary,numImages)
		run_02_imagematching(output,binary)
		run_03_featurematching(output,binary)
		run_04_structure_from_motion(output,binary)
		run_05_prepare_densescene(output,binary)
		run_06_depthmap(output,binary,numImages,3)
		run_07_depthmapfilter(output,binary)
		run_08_meshing(output,binary,bounding)
		run_09_meshfiltering(output,binary)
		if outputtype != "":
			#Convert Mesh if different outputtype is given
			convertMesh(outputtype,output)
		else:
			#else add texture to final Mesh
			run_10_texturing(output,binary)
	else:
		#if customqueue in config
		run_custom_queue(binary,meshroomqueue,input,blur)


main()


