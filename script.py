import math

with open("script", "w") as fd:

    end = ""
    for i in range(0, 72):
        end += "clear\n"

        end += "push\n"
        end += "move\n 250 250 0\n"
        end += "rotate\n y %f\n"%(i*5)
        end += "sphere\n0 0 0 50\n"
        end += "pop\n"
        
        end += "push\n"
        end += "move\n 250 250 0\n"
        end += "rotate\n z %f\n"%(i*5)
        end += "rotate\n x %f\n"%(i*5)
        end += "torus\n0 0 0 25 150\n"
        end += "pop\n"

        if i < 10:
            end += "save\n anim/00%d.png\n"%(i)
        else:
            end += "save\n anim/0%d.png\n"%(i)
    fd.write(end)
