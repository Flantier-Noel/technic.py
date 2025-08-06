import _3dEngine
import tkinter

def visualisation(scn):
    root = tkinter.Tk()
    cnv = tkinter.Canvas(root)

    global th, ph
    th, ph = 0,0

    def rotate(event):
        global th, ph
        if event.char == 'z' : th -= 0.1
        if event.char == 's' : th += 0.1
        if event.char == 'q' : ph -= 0.1
        if event.char == 'd' : ph += 0.1

        pln_lst = scn.priority(th, ph)
        for pln in pln_lst :
            cnv.create_polygon([_3dEngine.projection(corn_pos, th, ph) for corn_pos in pln.corners_3D], fill = pln.fill, outline = pln.outline)
    root.bind('<Key>', rotate)

    cnv.pack()
    root.mainloop()


## test of basic 3D rendering

# 1 plane

pln = _3dEngine.Plane([(0,0,0), (1,0,0), (1,0,1), (0,0,1)], color=('0xff', '0x0', '0x0'), outline=('0x0', '0x0', '0x0'))
snc = _3dEngine.Scene([pln])