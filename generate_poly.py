import math

#the list of points starts with the known top and bottom of the object
points = [ (0,0,0), (0,0,3) ]
faces = []

#generate a circle of points around the top-bottom axis
#           top down, counter-clockwise order

height = 2.5
num = 5     # the number of points in this circle
radius = 1.2
angle = 0
ang_shift = 2 * math.pi / num

#calculate every point in the shape
for i in range(num):
    x = radius * round(math.cos(angle), 2)
    y = radius * round(math.sin(angle), 2)
    z = height

    angle = angle + ang_shift
    
    points.append( (x,y,z) )

#calculate every face in the shape
for i in range(2,len(points)):
    #top and bottom indicies are known
    top = 0
    bottom = 1

    #we find the indicies of the our point and its 2 neighbors
    cur  = i
    left = i - 1
    right = i + 1

    #handle wrap around with if statements
    if (left < 2):
        left = len(points) - 1
    if (right > (len(points) - 1) ):
        right = 2

    #update faces list with lists of indexes of verticies
    #faces.append([top, cur, left])
    faces.append([top, cur, right])
    #faces.append([bottom, cur, left])
    faces.append([bottom, cur, right])

#Generate the ply file header
print("ply")
print("format ascii 1.0")
print("element vertex %d" %(len(points)))
print("property float x")
print("property float y")
print("property float z")
print("element face %d" %(len(faces)))
print("property list uchar int vertex_index")
print("end_header")

#populate the list of verticies
for point in points:
    print("%.2f %.2f %.2f" %(point[0], point[1], point[2]))

#populate the list of faces
for face in faces:
    print("%d " %(len(face)), end='') # first num is the number of verticies in the face
    for i in face:
        print("%d " %(i), end='')
    print()


