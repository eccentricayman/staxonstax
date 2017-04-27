from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         sphere: add a sphere to the edge matrix - 
	    takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the edge matrix - 
	    takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the edge matrix - 
	    takes 6 arguemnts (x, y, z, width, height, depth)	    

	 circle: add a circle to the edge matrix - 
	    takes 3 arguments (cx, cy, r)
	 hermite: add a hermite curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
	 bezier: add a bezier curve to the edge matrix -
	    takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
         clear: clear the edge matrix of points
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def parse_file( fname, edges, screen, color ):

    f = open(fname)
    lines = f.readlines()

    step = 0.05
    c = 0

    top = 0
    
    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:            
            c+= 1
            args = lines[c].strip().split(' ')
            #print 'args\t' + str(args)

        #EDGES IS A STACC NOW
            
        if line == 'push':
            new = edges[top][:]
            edges.append(new)
            top += 1
        
        elif line == 'pop':
            edges.pop()
            top -= 1
            
        elif line == 'sphere':
            #print 'SPHERE\t' + str(args)
            sphere_edges = []
            add_sphere(sphere_edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(edges[top], sphere_edges)
            draw_polygons(sphere_edges, screen, color)
            
        elif line == 'torus':
            #print 'TORUS\t' + str(args)
            torus_edges = []
            add_torus(torus_edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult(edges[top], torus_edges)
            draw_polygons(torus_edges, screen, color)
            
        elif line == 'box':
            #print 'BOX\t' + str(args)
            box_edges = []
            add_box(box_edges,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(edges[top], box_edges)
            draw_polygons(box_edges, screen, color)
            
        elif line == 'circle':
            #print 'CIRCLE\t' + str(args)
            circle_edges = []
            add_circle(circle_edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(edges[top], circle_edges)
            draw_lines(circle_edges, screen, color)

        elif line == 'hermite' or line == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            curve_edges = []
            add_curve(curve_edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)
            matrix_mult(edges[top], curve_edges)
            draw_lines(curve_edges, screen, color)
            
        elif line == 'line':            
            #print 'LINE\t' + str(args)
            line_edges = []
            add_edge( line_edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(edges[top], line_edges)
            draw_lines(line_edges, screen, color)

        elif line == 'scale':
            #print 'SCALE\t' + str(args)
            scale = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(edges[top], scale)
            edges[top] = scale

        elif line == 'move':
            #print 'MOVE\t' + str(args)
            move = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(edges[top], move)
            edges[top] = move

        elif line == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
                
            matrix_mult(edges[top], t)
            edges[top] = t
                
        elif line == 'clear':
            edges = [ ]
            cleared = new_matrix()
            ident(cleared)
            edges.append(cleared)
            top = 0
            clear_screen(screen)
            
        # elif line == 'ident':
        #     ident(transform)

        # elif line == 'apply':
        #     matrix_mult( transform, edges )

        elif line == 'display' or line == 'save':

            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        c+= 1
