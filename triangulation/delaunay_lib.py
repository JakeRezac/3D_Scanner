import math

def right_of_line(point, start, end):
	# check to see if <point> is on the right side
	# of a line that moves from <start> to <end>
	
	# all points assumed to be unique and on a 2D plane stored in tuples
	#	point = (x,y)


	right = False
	on_a_line = False

	#Basic y = mx + b works if our line isn't verticle
	if (start[0] != end[0]):
		rise = start[1] - end[1]
		run  = start[0] - end[0]
		m    = rise / run
		b    = start[1] - (m * start[0])
		
		#if <point> lies below a line traveling forward on "x" axis 
		#it is to the right of that line

		num = (m * point[0]) + b
		if ( point[1] < num ):
			right = True

		if ( point[1] == num ):
			on_a_line = True

		#if the line travels negatively along "x" then the side is opposite
		if ( start[0] > end[0] ):
			right = not(right)

	#if the line is verticle we just compare x & y values directly to the point
	else:
		if (point[0] > start[0]):
			right = True		#assumes the line points upward

		if (point[0] == start[0]):
			on_a_line = True		

		if (start[1] > end[1]):
			right = not(right)	#Flips the side if our assumption is wrong
		
	return (right, on_a_line)

def same_triangle(tri_1, tri_2):
	# check to see if 2 triangles are the same regardless of vertex order
	#
	# each triangle is a thruple containing its 3 verticies
	#	tri_1 = (v10, v11, v12)
	#	tri_2 = (v20, v21, v22)

	v10 = tri_1[0]	
	v11 = tri_1[1]	
	v12 = tri_1[2]	

	v20 = tri_2[0]	
	v21 = tri_2[1]	
	v22 = tri_2[2]	

	#Cycle each possible order of tri_1's verticies and compare to tri_2's
	for i in range(2):
		for j in range(3):
			if ( (v10 == v20) and (v11 == v21) and (v12 == v22) ):
				return True

			temp = v10
			v10 = v11
			v11 = v12
			v12 = temp

		temp = v11
		v11 = v12
		v12 = temp

	return False


def circle_from_3(p1, p2, p3):
	#We'll be calculating the center point and radius of a circle containing the 3 points
	#p1, p2, and p3	
	#points are stored as (x,y) tuples
	#
	#Returns:
	# 	coordinates of circles center (h,k) and radius r. Stored in thruple like so:
	#		(h,k,r)

	#We'll be: 
	#	Finding the center of the circle by:
	#		intersecting lines that run perpendicularly through the midpoints of the sides
	#		of the triangle created by each pair of points
	#
	#	Finding radius r by:
	#		pluging the center into the equation of a circle with one of our points
	# 		Equation of a circle:	r^2 = (x-h)^2 + (y-k)^2 
	
	points = [p1, p2, p3]

	#midpoints and inverse slope of line segments are used to find lines that intersect at circles center (h,k)
	mp1 = (0,0)
	inv_slope1 = 0

	mp2 = (0,0)
	inv_slope2 = 0

	flag = 0

	#Loop through point pairs to find those midpoints and inverse slopes
	for i in range(3):
		if (flag > 1):		#No need to generate a 3rd line
			break

		pa = points[i]
		pb = points[i-1]	
		
		rise =  pb[1] - pa[1]
		if (rise == 0): 	#If inverse slope is going to be infinity skip it
			continue

		run = pb[0] - pa[0]
		
		mid_x = pa[0] + (run/2)
		mid_y = pa[1] + (rise/2)
		midpoint = (mid_x,mid_y)

		inv_slope = - run / rise
			
		if (flag == 0):
			mp1 = midpoint
			inv_slope1 = inv_slope	
			flag = flag + 1
		else:
			mp2 = midpoint
			inv_slope2 = inv_slope	
			flag = flag + 1
	
	#Find intersection of the 2 lines	(these are just algebraic identities from k = mh + b intersections)
	x1 = mp1[0]
	y1 = mp1[1]

	x2 = mp2[0]
	y2 = mp2[1]

	#print ("(x1,y1) = (%f,%f)" % (x1,y1))
	#print ("(x2,y2) = (%f,%f)" % (x2,y2))
	#print ("inv_slope1")
	#print (inv_slope1)
	#print ("inv_slope2")
	#print (inv_slope2)

	#print("points: ", end='')
	#print(p1, end=', ')
	#print(p2, end=', ')
	#print(p3)
	#h = ( ( y2 - inv_slope2 * x2) - ( y1 - inv_slope1 * x1 ) ) / (inv_slope1 - inv_slope2) 
	h = 	 y2 - (inv_slope2 * x2)
	h = h - (y1 - (inv_slope1 * x1))
	h = h / (inv_slope1 - inv_slope2)
	
	k = (inv_slope1 * h) 	
	k = k + ( y1 - inv_slope1 * x1 ) #add y intercept of midpoint line

	#h and k are used to find r with standard eq. of a circle, r^2 = (x-h)^2 + (y-k)^2 
	r = (p1[0] - h)**2 + (p1[1] - k)**2
	r = math.sqrt(r)			#radius of circle

	return (h,k,r)
	


def point_in_circle(p, circ):
	#Checks to see if a point is inside a circle
	#	circ	(h,k,r)	 = (x_center, y_center, radius)
	#	p	(x,y)
	#
	#Returns:
	#		True	if point is in circle
	#		False 	if point is outside of circle

	x = p[0]	
	y = p[1]	
	h = circ[0]
	k = circ[1]
	r = circ[2]

	dist = (x - h)**2 + (y - k)**2
	dist = math.sqrt(dist)

	if (dist > r):
		return False
	else:
		return True

def delaunay_triangulation(points, triangles):
	#points are expected to come pre-projected onto a plane and only have 2 coordinates
	#	(x,y)
	#			coordinates are floats that refer to a location in space

	#triangle are described as a thruple of verticies
	#	(v1,v2,v3)
	#			verticies are integers that refer to the index number
	#			of a point in our 'points' list

	for point_index, point in enumerate(points[3:], start = 3):		#Consider each point 1 at a time (first 3 points for super triangle so we skip them)
		#print("placing point ", end='')
		#print(point)
		#Check each triangle's validity witht the new point
		illegal_tris = []
		for tri in triangles:						
			#Grab points from triangle and calc their circle
			p1 = points[tri[0]]
			p2 = points[tri[1]]
			p3 = points[tri[2]]

			circle = circle_from_3(p1,p2,p3)
			
			#Check if circle contains the new point
			if (point_in_circle(point, circle)):	
				illegal_tris.append(tri)			#Add illegal triangles to temporary list

		#Remove illegal triangles from main triangles list
		for tri in illegal_tris:
			triangles.remove(tri)
		#Removing these points will create a polygonal border around the new point

		
		#Edges of the polygon will be the only edges in illegal triangles that don't match any others
		#Compare Edges of illgal triangles to find polygon edges:
		poly_edges = []
		for tri in illegal_tris:					#Add every illegal_tri edge to poly_edges[]
			for i in range(3):
				v1 = tri[i-1]
				v2 = tri[i]
				edge = (v1, v2)
				#print("edge: ", end='')
				#print(edge)

				if (v1 > v2):						#Order verticies in edge for easy comparison later
					edge = (edge[1],edge[0])

				if (edge in poly_edges):				#Each edge is shared by a max of 2 triangles.
					poly_edges.remove(edge)				#So this conditional will ensure we only track edges with no matches.
				else:
					poly_edges.append(edge)

		#print ("poly_edges[]: ", end='')
		#print (poly_edges)
		
		#Create new triangles from each edge in the polygon and the new point being added to the triangulation
		#print ("poly_edges: ", end ='')
		#print (poly_edges)
		new_tris = []
		for edge in poly_edges:
			#print ("edge: ", end ='')
			#print (edge)
			new_tri = (edge[0], edge[1], point_index)			#Remember that triangle thruples store index numbers in the points list
			new_tris.append(new_tri)
	
		#print ("new_tris[]: ", end='')	
		#print (new_tris)	
		#Find repeat triangles 
		illegal_tris = []						#Wipe and reuse illegal_tris[] to track duplicates in new_tris[]
		for count, tri in enumerate(new_tris[:-1]):
			for other in new_tris[(count + 1):]:
				if (same_triangle(tri, other)):
					illegal_tris.append(tri)
					break

		#Remove repeats from new_tris[]
		#print("new_tris: ", end='')
		#print(new_tris)
		#print("illegal_tris: ", end='')
		#print(illegal_tris)
		for tri in illegal_tris:
			#print ("removing tri: ", end ='')
			#print (tri)
			new_tris.remove(tri)

		#Add new_tris to main triangles[] list
		for tri in new_tris:
			triangles.append(tri)
	
		#print ("triangles[]: ", end='')	
		#print (triangles)	

	#Remove all triangles that include points from the original super triangle
	#print (triangles)
	illegal_tris = []							#Wipe and reuse illegal_tris again
	for tri in triangles:
		i_p1 = tri[0]
		i_p2 = tri[1]
		i_p3 = tri[2]

		if ( (i_p1 < 3) or (i_p2 < 3) or (i_p3 <3) ):				#Check for points from first 3 elements in the list
			#print ("Removing tri: ", end = '')
			#print (tri)
			illegal_tris.append(tri)

	for tri in illegal_tris:
		#print ("Removing tri: ", end = '')
		#print (tri)
		triangles.remove(tri)

			#########################################################################
			#			Point Projection Functions			#
			#########################################################################
#Important:
#		These projections will seem very much like magic numbers. Please reference the 'Projection_Visual.png' image 
#		On the github repository for an intuitive diagram that should make all of this make sense

def project_Front(point):
	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Front plane
	# 	point 		(x, y, z)
	#     	returns		(x', y')
	
	y = point[1] 
	z = point[2] 
	#The projected point has an origin at the bottom most left corner of the sub-plane
	return ( (y, z) )

def project_Back(point):
	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
	# 	point 		(x, y, z)
	#     	returns		(x', y')

	y = point[1] 
	z = point[2] 
	#The projected point has an origin at the bottom most left corner of the sub-plane
	return ( ((-y),z) )

def project_Left(point):
	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
	# 	point 		(x, y, z)
	#     	returns		(x', y')

	x = point[0] 
	z = point[2] 
	#The projected point has an origin at the bottom most left corner of the sub-plane
	return ( (x,z) )

def project_Right(point):
	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
	# 	point 		(x, y, z)
	#     	returns		(x', y')

	x = point[0] 
	z = point[2] 
	#The projected point has an origin at the bottom most left corner of the sub-plane
	return ( ((-x),z) )

def project_Bottom(point):
	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
	# 	point 		(x, y, z)
	#     	returns		(x', y')

	x = point[0] 
	y = point[1] 
	#The projected point has an origin at the bottom most left corner of the sub-plane
	return ( (y,x) )

def project_Top(point):
	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
	# 	point 		(x, y, z)
	#     	returns		(x', y')

	x = point[0] 
	y = point[1] 
	#The projected point has an origin at the bottom most left corner of the sub-plane
	return ( (y, (-x)) )

		
def generate_cone(rad_max, rad_min, height, ang_res, step_res):
	points = []
	z = - (height/2)
	rad = rad_max

	step = height / step_res
	rad_change = (rad_max - rad_min) / step_res

	for j in range(step_res):
		for i in range(ang_res):
			theta = i * (360/ang_res)

			x = rad * math.cos(math.radians(theta))
			y = rad * math.sin(math.radians(theta))

			points.append((x,y,z))

		z = z + step
		rad = rad - rad_change

	return points
			

		
	
	
def generate_sphere(rad, ang_res):
	#used to generate a test point cloud
	sphere_points = []
	#radius = 100
	#angular_res = 40
	radius = rad
	angular_res = ang_res		#How many steps to rotate a full 360 degrees
	for phi in range(0,angular_res):
		phi = phi * (360 / angular_res)	#Convert phi to degrees
		z      = math.sin(math.radians(phi)) * radius
		proj_r = math.cos(math.radians(phi)) * radius

		for theta in range(0,angular_res):
			theta = theta * (360 / angular_res)	#Convert theta to degrees
			y = math.sin(math.radians(theta)) * proj_r
			x = math.cos(math.radians(theta)) * proj_r

			sphere_points.append((x,y,z))

	return (sphere_points)

def generate_ply(points, tris):
	ply_file = open("output.ply", "w")
	#Generate the ply file header
	ply_file.write("ply\n")
	ply_file.write("format ascii 1.0\n")
	ply_file.write("element vertex %d\n" %(len(points)))
	ply_file.write("property float x\n")
	ply_file.write("property float y\n")
	ply_file.write("property float z\n")
	ply_file.write("element face %d\n" %(len(tris)))
	ply_file.write("property list uchar int vertex_index\n")
	ply_file.write("end_header\n")

	#populate the list of verticies
	for point in points:
	    ply_file.write("%.2f %.2f %.2f\n" %(point[0], point[1], point[2]))
	
	#populate the list of faces
	for tri in tris:
	    ply_file.write(("3 ") ) # first num is the number of verticies in the face

	    for v in tri:
	        ply_file.write("%d " %(v))
	    ply_file.write("\n")

	ply_file.close()

#def project_Front(point, Plane_dist):
#	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Front plane
#	# 	point 		(x, y, z)
#	#     	returns		(x', y')
#	
#	y = point[1] 
#	z = point[2] 
#	#The projected point has an origin at the bottom most left corner of the sub-plane
#	return ( (y, z) )
#
#def project_Back(point, Plane_dist):
#	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
#	# 	point 		(x, y, z)
#	#     	returns		(x', y')
#
#	y = point[1] 
#	z = point[2] 
#	#The projected point has an origin at the bottom most left corner of the sub-plane
#	length = 2 * Plane_dist
#	return ( ((length - y),z) )
#
#def project_Left(point, Plane_dist):
#	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
#	# 	point 		(x, y, z)
#	#     	returns		(x', y')
#
#	x = point[0] 
#	z = point[2] 
#	#The projected point has an origin at the bottom most left corner of the sub-plane
#	return ( (x,z) )
#
#def project_Right(point, Plane_dist):
#	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
#	# 	point 		(x, y, z)
#	#     	returns		(x', y')
#
#	x = point[0] 
#	z = point[2] 
#	#The projected point has an origin at the bottom most left corner of the sub-plane
#	length = 2 * Plane_dist
#	return ( ((length - x),z) )
#
#def project_Bottom(point, Plane_dist):
#	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
#	# 	point 		(x, y, z)
#	#     	returns		(x', y')
#
#	x = point[0] 
#	y = point[1] 
#	#The projected point has an origin at the bottom most left corner of the sub-plane
#	return ( (y,x) )
#
#def project_Top(point, Plane_dist):
#	#point will be a 3D coordinate that we will convert to 2D by projecting it onto the Back plane
#	# 	point 		(x, y, z)
#	#     	returns		(x', y')
#
#	x = point[0] 
#	y = point[1] 
#	#The projected point has an origin at the bottom most left corner of the sub-plane
#	length = 2 * Plane_dist
#	return ( (y, (length - x)) )


