from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
color = [ 0, 0, 0 ]
edges = []
temp = new_matrix()
ident(temp)
edges.append(temp)

# print_matrix( make_bezier() )
# print
# print_matrix( make_hermite() )
# print

parse_file( 'dwscript', edges, screen, color )
