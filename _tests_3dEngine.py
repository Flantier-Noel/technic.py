import _3dEngine
import tkinter

def visualisation(scn):
    root = tkinter.Tk()
    cnv = tkinter.Canvas(root, width = 200, height=200)

    global th, ph
    th, ph = 0,0

    def rotate(event):
        global th, ph, cnv_ids
        cnv.forget('all')

        if event.char == 'z' : th -= 0.1
        if event.char == 's' : th += 0.1
        if event.char == 'q' : ph += 0.1
        if event.char == 'd' : ph -= 0.1

        pln_lst = scn.priority(th, ph)
        for pln in pln_lst :
            corners = []
            for corn_pos in pln.corners_3D :
                x2,  y2 = _3dEngine.projection(corn_pos, th, ph)
                corners.append((x2+100, 100-y2))
            cnv.create_polygon(corners, fill = pln.fill, outline = pln.outline)
    root.bind('<Key>', rotate)

    cnv.pack()
    root.mainloop()


## test of basic 3D rendering

# 1 plane

pln = _3dEngine.Plane([(0,0,0), (50,0,0), (50,0,1), (0,0,50)], color=('0xff', '0x0', '0x0'), outline=('0x0', '0x0', '0x0'))
scn = _3dEngine.Scene([pln])
visualisation(scn)

# 3 planes

plnX = _3dEngine.Plane([(0,0,0), (50,0,0), (50,0,50), (0,0,50)], color=('0xff', '0x0', '0x0'), outline=('0x0', '0x0', '0x0'))
plnY = _3dEngine.Plane([(0,0,0), (0,50,0), (0,50,50), (0,0,50)], color=('0x0', '0xff', '0x0'), outline=('0x0', '0x0', '0x0'))
plnZ = _3dEngine.Plane([(0,0,0), (50,0,0), (50,50,0), (0,50,0)], color=('0x0', '0x0', '0xff'), outline=('0x0', '0x0', '0x0'))
scn = _3dEngine.Scene([plnX, plnY, plnZ])
visualisation(scn)