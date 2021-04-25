import math

#calculate every point in the shape
#for i in range(num):
#    x = radius * round(math.cos(angle), 2)
#    points.append( (x,y,z) )
#print("element vertex %d" %(len(points)))
#for point in points:
#    print("%.2f %.2f %.2f" %(point[0], point[1], point[2]))
#print("%d " %(len(face)), end='') # first num is the number of verticies in the face

points_2D = [ (-3,3), (0,2), (3,-3), (0,-1), (3,1), (-3,-3)]
triangles = [ (0,1,3), (1,3,4), (3,2,4), (5,0,3), (3,2,5)]

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


def point_in_triangle(point, tri_index):
	# check to see if <point> lies within a triangle
	# 	point_i = (x,y)
	#	triangle = (point_1, point_2, point_3)

	#Makes code more readable
	x = 0
	y = 1

	triangle = triangles[tri_index]

	p1 = triangle[0] #this element in triangles is an index in points_2D
	p2 = triangle[1]
	p3 = triangle[2]
	
	p1 = points_2D[p1] #this will be a 2D point tuple (x,y)
	p2 = points_2D[p2]
	p3 = points_2D[p3]
	
	p_list = [p1,p2,p3]

	# this may not be necessary
	##ENSURE WE ALWAYS TRAVERSE TRIANGLE COUNTER CLOCKWISE FOR CONCISTENCY
	##Select 1st point	
	#for i in range(1,3):					#Start list with the right most point
	#	if (p_list[i][x] > p_list[0][x]):  		#compare "x" values of every point
	#		temp_p = p_list[0]
	#		p_list[0] = p_list[i]
	#		p_list[i] = temp_p

	#	elif (p_list[i][x] == p_list[0][x]): 		#if values are equal we choose for the lower "y"
	#		if (p_list[i][y] < p_list[0][y]):
	#			temp_p = p_list[0]
	#			p_list[0] = p_list[i]
	#			p_list[i] = temp_p


	##Select order of last 2 points
	#if (p_list[2][y] > p_list[1][y]):			#2nd point is chosen to be highest of remaining 2
	#	temp_p = p_list[1]
	#	p_list[1] = p_list[2]
	#	p_list[2] = temp_p
	#							#If last 2 points are equal height pick right most
	#if (p_list[2][y] == p_list[1][y]) and (p_list[2][x] > p_list[1][x]):
	#	temp_p = p_list[1]
	#	p_list[1] = p_list[2]
	#	p_list[2] = temp_p
			

	# Traverse the triangle and check if all sides match	
	# right_of_line returns a tuple: (right, on_a_line)
	on_a_line = 0	
	
	side1 = right_of_line(point, p_list[0], p_list[1])
	on_a_line += side1[1]
	side1 = side1[0]

	side2 = right_of_line(point, p_list[1], p_list[2])
	on_a_line += side2[1]
	side2 = side2[0]

	side3 = right_of_line(point, p_list[2], p_list[0])
	on_a_line += side3[1]
	side3 = side3[0]

	if (on_a_line):						#on the line is considered inside
		return True
	elif (side1 == side2) and (side2 == side3):
		return True
	else:
		return False	

#def circle_from_3(p1, p2, p3):
#	#We'll be calculating the center point and radius of a circle containing the 3 points
#	#p1, p2, & p3	
#	#points are stored as (x,y) tuples
#	#
#	#Returns:
#	# 	coordinates of circles center (h,k) and radius r. Stored in thruple like so:
#	#		(h,k,r)
#
#	#We'll be utilizing the equation for a circle
#	#		r^2 = (x-h)^2 + (y-k)^2 
#	# all values are found using algebraic identities derived from 
#	# the system of equations made from this eq. and our 3 points.
#	x1 = p1[0]
#	y1 = p1[1]
#	x2 = p2[0]
#	y2 = p2[1]
#	x3 = p3[0]
#	y3 = p3[1]
#
#	# we compartmentalize our equations with more workable constants
#	c1 = (y1 - y3) / (x3 - x1)
#	c2 = (y3**2 - y1**2 + x3**2 - x1**2) / (2 * (x3 - x1))
#	c3 = (x2 - x1) / (y1 - y2)
#	c4 = (x1**2 - x2**2 + y1**2 - y2**2) / (2 * (y1 - y2))
#
#	k = ((c2*c3) + c4) / (1 - (c1 * c3))	#y-coord. of center
#	h = (k * c1) + c2			#x-coord. of center
#
#	r = (x1 - h)*(x1 - h) + (y1 - k)*(y1 - k)
#	r = math.sqrt(r)			#radius of circle
#
#	return (h,k,r)

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
	
#def circle_from_tri(triangle):
#	#Wrapper function to get a circle from the 3 points of a triangle
#	#	triangle will be a thruple of vertex tuples: 
#	#
#	#	triangle	(v1, v2, v3)
#	#	v1		(x,y)
#	#
#	#Returns:
#	#	circle		(h,k,r); a circle with center (h,k) and radius r
#
#	p1 = triangle[0]
#	p2 = triangle[1]
#	p3 = triangle[2]
#
#	return circle_from_3(p1, p2, p3)


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




#def circle_from_3(p1, p2, p3):
#	#We'll be calculating the center point and radius of a circle containing the 3 points
#	#p1, p2, & p3	
#	#points are stored as (x,y) tuples
#	#
#	#Returns:
#	# 	coordinates of circles center (h,k) and radius r. Stored in thruple like so:
#	#		(h,k,r)
#
#	#We'll be utilizing the equation for a circle
#	#		r^2 = (x-h)^2 + (y-k)^2 
#	# all values are found using algebraic identities derived from 
#	# the system of equations made from this eq. and our 3 points.
#	x1 = p1[0]
#	y1 = p1[1]
#	x2 = p2[0]
#	y2 = p2[1]
#	x3 = p3[0]
#	y3 = p3[1]
#
#	# we compartmentalize our equations with more workable constants
#	c1 = (y1 - y3) / (x3 - x1)
#	c2 = (y3**2 - y1**2 + x3**2 - x1**2) / (2 * (x3 - x1))
#	c3 = (x2 - x1) / (y1 - y2)
#	c4 = (x1**2 - x2**2 + y1**2 - y2**2) / (2 * (y1 - y2))
#
#	k = ((c2*c3) + c4) / (1 - (c1 * c3))	#y-coord. of center
#	h = (k * c1) + c2			#x-coord. of center
#
#	r = (x1 - h)*(x1 - h) + (y1 - k)*(y1 - k)
#	r = math.sqrt(r)			#radius of circle
#
#	return (h,k,r)

#def circle_from_tri(triangle):
#	#Wrapper function to get a circle from the 3 points of a triangle
#	#	triangle will be a thruple of vertex tuples: 
