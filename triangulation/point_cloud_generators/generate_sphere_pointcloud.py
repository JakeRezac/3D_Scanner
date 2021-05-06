import math
#We'll just be creating a point cloud of a spheres surface for testing
def main():
	sphere_points = []
	radius = 100
	angular_res = 40		#How many steps to rotate a full 360 degrees
	for phi in range(0,angular_res):
		phi = phi * (360 / angular_res)	#Convert phi to degrees
		z      = math.sin(math.radians(phi)) * radius
		proj_r = math.cos(math.radians(phi)) * radius

		for theta in range(0,angular_res):
			theta = theta * (360 / angular_res)	#Convert theta to degrees
			y = math.sin(math.radians(theta)) * proj_r
			x = math.cos(math.radians(theta)) * proj_r

			sphere_points.append((x,y,z))

	print (sphere_points)
			
	

main()
