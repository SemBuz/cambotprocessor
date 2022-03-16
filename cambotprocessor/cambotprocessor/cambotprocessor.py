import sys, os
import subprocess
import argparse

def silent_mkdir(theDir):
	try:
		os.mkdir(theDir)
	except:
		pass
	return 0

def run_00_camerainit(baseDir,binDir,srcImageDir):
	SilentMkdir(baseDir + "/00_CameraInit")

	binName = binDir + "/aliceVision_cameraInit.exe"

	dstDir = baseDir + "/00_CameraInit/"
	cmdLine = binName
	cmdLine = cmdLine + " --defaultFieldOfView 45.0 --verboseLevel info --sensorDatabase \"\" --allowSingleView 1"
	cmdLine = cmdLine + " --imageFolder \"" + srcImageDir + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "cameraInit.sfm\""
	print(cmdLine)
	subprocess.call(cmdLine)

	return 0

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

def run_06_depthmap(baseDir,binDir,numImages):
	silent_mkdir(baseDir + "/06_DepthMap")

	srcSfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	imgFld = baseDir + "/05_PrepareDenseScene"
	dstDir = baseDir + "/06_DepthMap"

	binName = binDir + "\\aliceVision_dephtMapEstimation.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --sgmGammaC 5.5 --sgmWSH 4 --refineGammaP 8.0 --refineSigma 15 --refineNSamplesHalf 150 --sgmMaxTCams 10 --refineWSH 3 --downscale 2 --refineMaxTCams 6 --verboseLevel info --refineGammaC 15.5 --sgmGammaP 8.0"
	cmdLine = cmdLine + " --refineNiters 100 --refineNDepthsToRefine 31 --refineUseTcOrRcPixSize False"

	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --imagesFolder \"" + imgFld + "\""
	cmdLine = cmdLine + " --output \"" + dstDir +"\""

	#ToDo: Finish Step 6
	return 0

def run_07_depthmapfilter():
	#ToDo: Step 7
	return 0

def run_08_meshing():
	#ToDo: Step 8
	return 0

def run_09_meshfiltering():
	#ToDo: Step 9
	return 0

def run_10_texturing():
	#ToDo: Step 10
	return 0

def run_custom_queue(binDir,queue,input,blur):
	#ToDo: Custom Queue
	pass

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--config',help='configFile with Meshroom-parameters',default="",type=str)
	parser.add_argument('--blur',help='declares Blurdetection value',type=float)
	parser.add_argument('--outputtype',help='file extension for final 3D object',type=str)
	parser.add_argument('--meshroomqueue',help='custom Meshroomqueue',default="",type=str)
	parser.add_argument('--bounding',help='declaration of Boundingbox',default="")
	parser.add_argument('--input',help='directory of images',type=str)
	parser.add_argument('--output',help='directory of output',type=str)
	parser.add_argument('--binary',help='directory of the Meshroom binary',type=str)

	args = parser.parse_args()

	if (args.meshroomqueue != "" and args.config == ""):
	    run_custom_queue(args.binary,args.meshroomqueue,args.input,args.blur)
	elif args.config != "":
		config_standard_queue(args.config)
	else:
		print("Base dir  : %s" % args.output)
		print("Image dir : %s" % args.input)
		print("Bin dir   : %s" % args.binary)
		print("Blur      : %s" % args.blur)
		print("outputtype: %s" % args.outputtype)
		print("Bounding  : %s" % args.bounding)
		standard_queue(args)

def standard_queue(args):
	#ToDo RemoveBlur

	numImages = len([name for name in os.listdir(args.input)])

	silent_mkdir(args.output)

	run_00_camerainit(args.output,args.binary,args.input)
	run_01_featureextraction(args.output,args.binary,numImages)
	run_02_imagematchingg(args.output,args.binary)
	run_03_featurematching(args.output,args.binary)
	run_04_structure_from_motion(args.output,args.binary)
	run_05_prepare_densescene(args.output,args.binary)
	run_06_depthmap(args.output,args.binary,numImages,3)
	run_07_depthmapfilter(args.output,args.binary)
	run_08_meshing(args.output,args.binary,args.outputtype,args.bounding)
	run_09_meshfiltering(args.output,args.binary,args.outputtype)
	run_10_texturing(args.output,args.binary,args.outputtype)

def config_standard_queue(configFile):
	#ToDo configparsing
	pass

main()