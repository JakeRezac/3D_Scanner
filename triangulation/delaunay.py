import math
import delaunay_lib

#for now we're manually coding the super triangle in
#points = [(7,4),(6,-7),(-5,-3),(-8,9),(0,0),(-20,-20),(20,-20),(0,40)]
###points = [(-20,-20),(20,-20),(0,40),(7,4),(6,-7),(-5,-3),(-8,9),(0,0)]	#we store our super triangles points in the first 3 elements
###triangles = [(0,1,2)]



points = [(-9,-9), (9,-9), (0,9), (3,-6), (-4,-5), (0,0), (-2,3), (3,-3)]	#we store our super triangles points in the first 3 elements
triangles = [(0,1,2)]



#triangle are described as a thruple of verticies
#	(v1,v2,v3)
#			verticies are integers that refer to the index number
#			of a point in our 'points' list

def main():
	for point_index, point in enumerate(points[3:], start = 3):		#Consider each point 1 at a time (first 3 points for super triangle so we skip them)
		#Check each triangle's validity witht the new point
		illegal_tris = []
		for tri in triangles:						
			#Grab points from triangle and calc their circle
			p1 = points[tri[0]]
			p2 = points[tri[1]]
			p3 = points[tri[2]]

			circle = delaunay_lib.circle_from_3(p1,p2,p3)
			
			#Check if circle contains the new point
			if (delaunay_lib.point_in_circle(point, circle)):	
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
					edge = edge[-2:2]

				if (edge in poly_edges):				#Each edge is shared by a max of 2 triangles.
					poly_edges.remove(edge)				#So this conditional will ensure we only track edges with no matches.
				else:
					poly_edges.append(edge)
		
		#Create new triangles from each edge in the polygon and the new point being added to the triangulation
		#print ("poly_edges: ", end ='')
		#print (poly_edges)
		new_tris = []
		for edge in poly_edges:
			#print ("edge: ", end ='')
			#print (edge)
			new_tri = (edge[0], edge[1], point_index)			#Remember that triangle thruples store index numbers in the points list
			new_tris.append(new_tri)
	
		print ("new_tris[]: ", end='')	
		print (new_tris)	
		#Find repeat triangles 
		illegal_tris = []						#Wipe and reuse illegal_tris[] to track duplicates in new_tris[]
		for count, tri in enumerate(new_tris[:-1]):
			for other in new_tris[(count + 1):]:
				if (delaunay_lib.same_triangle(tri, other)):
					illegal_tris.append(tri)
					break

		#Remove repeats from new_tris[]
		#print("new_tris: ", end='')
		#print(new_tris)
		#print("illegal_tris: ", end='')
		#print(illegal_tris)
		for tri in illegal_tris:
			print ("removing tri: ", end ='')
			print (tri)
			new_tris.remove(tri)

		#Add new_tris to main triangles[] list
		for tri in new_tris:
			triangles.append(tri)
	
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


	print (triangles)
	print (points)

	#print out triangles
	#for tri in triangles:
	#	p1 = points[tri[0]]
	#	p2 = points[tri[1]]
	#	p3 = points[tri[2]]
	#	print("( (%f,%f), (%f,%f),  (%f,%f) )" %(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]))

	#Used to test code to find a circle from 3 points
	#for tri in triangles:
	#	p1 = points[tri[0]]
	#	p2 = points[tri[1]]
	#	p3 = points[tri[2]]

	#	circle = delaunay_lib.circle_from_3(p1,p2,p3)
	#	print (circle)
			
main()

