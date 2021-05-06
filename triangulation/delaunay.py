import math
import delaunay_lib

points = [(-9,-9), (9,-9), (0,9), (3,-6), (-4,-5), (0,0), (-2,3), (3,-3), (1,-3), (-3,-9)]	#we store our super triangles points in the first 3 elements
triangles = [(0,1,2)]


#triangle are described as a thruple of verticies
#	(v1,v2,v3)
#			verticies are integers that refer to the index number
#			of a point in our 'points' list


def main():
	delaunay_lib.delaunay_triangulation(points, triangles)
	
	print (triangles)
	print (points)
main()

