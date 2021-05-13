import math
import delaunay_lib


#points = [(-9,-9), (9,-9), (0,9), (3,-6), (-4,-5), (0,0), (-2,3), (3,-3), (1,-3), (-3,-9)]	#we store our super triangles points in the first 3 elements
#triangles = [(0,1,2)]

#3D_points are described as a thruple to form a 3D coordinate
#	(x, y, z)
#			x, y, and z are all floats that descirbe the points projection onto 
#			that respective axis

#triangle are described as a thruple of verticies
#	(v1,v2,v3)
#			verticies are integers that refer to the index number
#			of a point in our 'points' list
#
#			Since each vertex is described this way, this data type can be used
#			to describe triangles in 2D or 3D

#6 planes normal to 1 of the cartesian unit vectors of the space will form an equal lateral 
#6 sided box around the point cloud 

##As 3D points are projected onto different planes a new list is used to store points in 
##Their new order
#new_points_3D = []

#Each point in the cloud will be projected onto the plane it is closest to
Plane_dist = 110	#How far away from the origin is each plane?

# Planes are initialized with their super triangles
Front_points = []
Front_tris = []

Back_points = []
Back_tris = []

Left_points = []
Left_tris = []

Right_points = []
Right_tris = []

Top_points = []
Top_tris = []

Bottom_points = []
Bottom_tris = []
#
#Bottom_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Bottom_tris = [(0,1,2)]
#Front_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Front_tris = [(0,1,2)]
#
#Back_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Back_tris = [(0,1,2)]
#
#Left_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Left_tris = [(0,1,2)]
#
#Right_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Right_tris = [(0,1,2)]
#
#Top_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Top_tris = [(0,1,2)]
#
#Bottom_points = [(0,10000), (-10000,-10000), (10000,-10000)]
Bottom_tris = [(0,1,2)]



def main():
	points_3D = [ (1,1,1), (2,2,2), (3,3,3), (-1,-1,-1), (-2,-2,-2),(2,0,0),(0,0,-2),(0,-2,0), (-2,0,0)]

	#Sort points based on what plane they are closest to. 
	#Points will not be projected onto 2D plane until next step
	#----------------------------------------------------------------------
	for point in points_3D:
		x = point[0]
		y = point[1]
		z = point[2]

		x_abs = abs(x)
		y_abs = abs(y)
		z_abs = abs(z)

		if ((x_abs > y_abs) and (x_abs > z_abs)):
			if ( x > 0 ):
				Front_points.append(point)
			else:
				Back_points.append(point)

		elif ((y_abs > z_abs)):
			if ( y > 0 ):
				Right_points.append(point)
			else:
				Left_points.append(point)

		else:
			if ( z > 0 ):
				Top_points.append(point)
			else:
				Bottom_points.append(point)
			

	####Recreate list of points_3D[] now ordered Front, Back, Left, Right, Top, Bottom
	####First three elements of each list are left out to exclude super triangle verticies
	####----------------------------------------------------------------------
	###points_3D = Front_points[3:] + Back_points[3:] + Left_points[3:] + Right_points[3:] + Top_points[3:] + Bottom_points[3:]

	#Recreate list of points_3D[] now ordered Front, Back, Left, Right, Top, Bottom
	#First three elements of each list are left out to exclude super triangle verticies
	#----------------------------------------------------------------------
	points_3D = Front_points + Back_points + Left_points + Right_points + Top_points + Bottom_points

	#Go back through each plane and project its closest planes onto it
	#----------------------------------------------------------------------
	for i in range(len(Front_points)):	
		Front_points[i] = delaunay_lib.project_Front(Front_points[i])

	for i in range(len(Back_points)):	
		Back_points[i] = delaunay_lib.project_Back(Back_points[i])

	for i in range(len(Left_points)):	
		Left_points[i] = delaunay_lib.project_Left(Left_points[i])

	for i in range(len(Right_points)):	
		Right_points[i] = delaunay_lib.project_Right(Right_points[i])

	for i in range(len(Top_points)):	
		Top_points[i] = delaunay_lib.project_Top(Top_points[i])

	for i in range(len(Bottom_points)):	
		Bottom_points[i] = delaunay_lib.project_Bottom(Bottom_points[i])
	
	for plane in [Front_points, Back_points, Left_points, Right_points, Top_points, Bottom_points]:
		print(plane)

	#Add Super Triangle to each plane's list of points and triangles
	#----------------------------------------------------------------------
	H = (1.73 + 1) * Plane_dist#Tan(60 deg) = 1.73		#Exactly how large the super triangle must be to fit the plane
	H = H * (1.2) 						#Add some wiggle room 

	super_tri_points = [(0,H),(-H, -H),(H, -H)]

	for plane in [Front_points, Back_points, Left_points, Right_points, Top_points, Bottom_points]:
		plane = super_tri_points + plane
		print (plane)

	#Run a 2D Delaunay triangulation on each plane's set of 2D points
	#----------------------------------------------------------------------
	delaunay_lib.delaunay_triangulation(Front_points, Front_tris)
	delaunay_lib.delaunay_triangulation(Back_points, Back_tris)
	delaunay_lib.delaunay_triangulation(Left_points, Left_tris)
	delaunay_lib.delaunay_triangulation(Right_points, Right_tris)
	delaunay_lib.delaunay_triangulation(Top_points, Top_tris)
	delaunay_lib.delaunay_triangulation(Bottom_points, Bottom_tris)

	print ("tris")
	for tris in [Front_tris, Back_tris, Left_tris, Right_tris, Top_tris, Bottom_tris]:
		print (tris)

	###delaunay_lib.delaunay_triangulation(points, triangles)
	###
	###print (triangles)
	###print (points)
main()

