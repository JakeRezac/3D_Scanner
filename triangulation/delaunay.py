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




def main():
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

	#points_3D = [ (1,1,1), (2,2,2), (3,3,3), (-1,-1,-1), (-2,-2,-2),(2,0,0),(0,0,-2),(0,-2,0), (-2,0,0)]
	#points_3D = delaunay_lib.generate_sphere(100, 20)
	points_3D = delaunay_lib.generate_cone(100, 20, 200, 30, 30)
	print("points_3D len: ", end='')
	print(len(points_3D))


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

	#print("printing planes 1")	
	#for plane in [Front_points, Back_points, Left_points, Right_points, Top_points, Bottom_points]:
	#	print(plane)

	#Add Super Triangle to each plane's list of points and triangles
	#----------------------------------------------------------------------
	H = (1.73 + 1) * Plane_dist#Tan(60 deg) = 1.73		#Exactly how large the super triangle must be to fit the plane
	H = H * (1.2) 						#Add some wiggle room 

	super_tri_points = [(0,H),(-H, -H),(H, -H)]
	
	Front_points = super_tri_points + Front_points
	Back_points = super_tri_points + Back_points
	Left_points = super_tri_points + Left_points
	Right_points = super_tri_points + Right_points
	Top_points = super_tri_points + Top_points
	Bottom_points = super_tri_points + Bottom_points

	#for plane in [Front_points, Back_points, Left_points, Right_points, Top_points, Bottom_points]:
	#	print (plane)

	#Run a 2D Delaunay triangulation on each plane's set of 2D points
	#----------------------------------------------------------------------
	delaunay_lib.delaunay_triangulation(Front_points, Front_tris)
	delaunay_lib.delaunay_triangulation(Back_points, Back_tris)
	delaunay_lib.delaunay_triangulation(Left_points, Left_tris)
	delaunay_lib.delaunay_triangulation(Right_points, Right_tris)
	delaunay_lib.delaunay_triangulation(Top_points, Top_tris)
	delaunay_lib.delaunay_triangulation(Bottom_points, Bottom_tris)


	#print ("tris")
	#for tris in [Front_tris, Back_tris, Left_tris, Right_tris, Top_tris, Bottom_tris]:
	#	print (tris)

	#Remove All super triangle points
	#----------------------------------------------------------------------
	#print("printing planes 2")	

	Front_points  = Front_points [3:]
	Back_points   = Back_points [3:]  
	Left_points   = Left_points [3:]  
	Right_points  = Right_points [3:] 
	Top_points    = Top_points [3:]   
	Bottom_points = Bottom_points [3:]

	#for plane in [Front_points, Back_points, Left_points, Right_points, Top_points, Bottom_points]:
	#	print(plane)

	#Adjust Index index numbers to reflect each points index in the complete list
	offset = -3
	for (plane, tri_list) in [(Front_points, Front_tris), (Back_points, Back_tris), (Left_points, Left_tris), (Right_points, Right_tris), (Top_points, Top_tris), (Bottom_points, Bottom_tris)]:
		for i in range(len(tri_list)):
			tri = tri_list[i]		# tri will be a thrupple of indicies to verticies in the points_3D list

			v1 = tri[0] + offset		# Add offset to each vertex index 
			v2 = tri[1] + offset	
			v3  = tri[2] + offset	


			new_tri = (v1,v2,v3)		# update original triangle list
			tri_list[i] = new_tri		

		offset = offset + len(plane)	# Adjust offset to account for lenght of current planes point list
		print("len(plane): ", end='')
		print(len(plane))

		print("new offset: ", end='')
		print(offset)			

	#for i in range(len(Front_tris)):
	#	tri = Front_tris[i]
	#	x = tri[0]
	#	y = tri[1]
	#	z = tri[2]
	#	
	#	x = x + offset				#correct vertex indicies with the offset value
	#	y = y + offset
	#	z = z + offset

	#	tri = (x,y,z)				#update the triangle list with the new values
	#	Front_tris[i] = tri	

	#	offset = offset + len(Front_points)	#update offset value for next lists adjustment
			


#	print("new triangles")
#	for tri_list in [Front_tris, Back_tris, Left_tris, Right_tris, Top_tris, Bottom_tris]:
#		print(tri_list)
			
	#Add each planes triangles together in a complete list	
	#-------------------------------------------------------------------------------------
	triangles = Front_tris + Back_tris + Left_tris + Right_tris + Top_tris + Bottom_tris
	print ("triangles")
	print (triangles)
	#print ("points_3D")
	#print (points_3D)

	#Generate .PLY file
	#-------------------------------------------------------------------------------------
	delaunay_lib.generate_ply(points_3D, triangles)
	###delaunay_lib.delaunay_triangulation(points, triangles)
	###
	###print (triangles)
	###print (points)
main()

