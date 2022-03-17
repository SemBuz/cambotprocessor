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

def run_10_texturing(baseDir,binDir):
	silent_mkdir(baseDir + "/10_Texturing")

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
	run_02_imagematching(args.output,args.binary)
	run_03_featurematching(args.output,args.binary)
	run_04_structure_from_motion(args.output,args.binary)
	run_05_prepare_densescene(args.output,args.binary)
	run_06_depthmap(args.output,args.binary,numImages,3)
	run_07_depthmapfilter(args.output,args.binary)
	run_08_meshing(args.output,args.binary,args.bounding)
	run_09_meshfiltering(args.output,args.binary)
	run_10_texturing(args.output,args.binary)

def config_standard_queue(configFile):
	#ToDo configparsing
	pass

main()