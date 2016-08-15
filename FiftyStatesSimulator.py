import tkinter as tk
import random
import os
from xml.dom.minidom import parse
import xml.dom.minidom


class FiftyStatesSimulator(tk.Frame):
    
    WIDTH = 1000
    HEIGHT = 1000

    #Changes to be added - mirror image the polygons, resize polygons at the start
    
    def __init__(self, root):
        #Initialize the scrollbars and the canvas
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, background="white")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,self.WIDTH,self.HEIGHT))
        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



        #Initialize starting fields
        self.scene = []
        self.x = 0
        self.y = 0
        self.zoom_factor = 1.2
        self.vertices = [0,0,self.WIDTH, self.HEIGHT]

        #Various test functions
        #self.draw_checkerboard()
        #self.draw_random_rects()
        #self.draw_example_state()
        #self.draw_example_rect()
        self.get_state_polygons()
        
        #binding drag and zoom functions to mouse click and scroll wheel:
        self.canvas.focus_set()
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind("<Key>", self.test_move)
        
        #unix uses <Button-4> and <Button-5> for scrolling
        if os.name == "posix":
            self.canvas.bind("<Button-4>", self.zoom_in)
            self.canvas.bind("<Button-5>", self.zoom_out)
        else:
            self.canvas.bind("<MouseWheel>", self.zoom_both)

    def test_move(self, event):
        print("hello")
        self.canvas.scale(self.scene[0][2], 100, 100, 1, 1)

    #parse the kml document into polygons to be drawn on the screen
    def get_state_polygons(self):
        DOMTree = xml.dom.minidom.parse("us_states.kml")
        collection = DOMTree.documentElement

        states = collection.getElementsByTagName("Placemark")

        tlist = []
        vlist = []
        #states = [states[0]]
        for state in states:
            print(state.getAttribute("id"))
            description = state.getElementsByTagName("description")
            for d in description:
                table = d.childNodes[0].data
                table = table.replace("<table cellpadding=\"1\" cellspacing=\"1\">", "")
                table = table.replace("</table>", "")
                rows = table.split("<tr>", 15)
                for row in rows:
                    cols = row.split("<td>", 2)
                    dlist = []
                    for col in cols:
                        col = col.replace("</tr>", "")
                        col = col.replace("</td>", "")
                        dlist.append(col)
                    tlist.append(dlist)

            slist = []
            polygons = state.getElementsByTagName("Polygon")
            for polygon in polygons:
                plist = []
                coord = polygon.getElementsByTagName("coordinates")[0]
                pairs = coord.childNodes[0].data.split("\n", 2000)
                for pair in pairs:
                    nums = pair.split(",", 2)
                    for num in nums:
                        if(num.strip() != ""):
                            plist.append(float(num.strip()))
                slist.append(plist)
            vlist.append(slist)

            #vlist = [vlist[0]]
            for state in vlist:
                for polygon in state:
                    color = ("red", "orange", "yellow", "green", "blue")[random.randint(0,4)]
                    poly = self.canvas.create_polygon(polygon, outline = "black", fill=color)
                    self.canvas.move(poly, 500, 500)
                    self.scene.append([polygon[0], polygon[1], poly, 1])
            
        
    def draw_random_rects(self):
        for n in range(50):
            x0 = random.randint(0, 300)
            y0 = random.randint(50, 300)
            x1 = x0 + random.randint(50, 100)
            y1 = y0 + random.randint(50,100)
            color = ("red", "orange", "yellow", "green", "blue")[random.randint(0,4)]
            #points = [x0, y0, x1, y0, x1, y1, x0, y1, x0, y0]
            points = [x0, y0, x1, y0, x0, y1, x0, y0]

            self.scene.append([x0, y0, self.canvas.create_polygon(points, outline="black", fill=color), 1])

            self.canvas.create_text(50,10, anchor="nw", text="Click and drag to move the canvas")
        
    def draw_checkerboard(self):
        sq_size = 40
        num_checkers = 10
        for x in range(0, sq_size*num_checkedrs, sq_size):
            for y in range(0, sq_size*num_checkers, sq_size):
                color = ("black", "white")[(int)(y/sq_size+x/sq_size)%2]
                self.scene.append([x, y, self.canvas.create_rectangle(x, y, x+sq_size, y+sq_size,outline="black", fill=color), 1])

    def draw_example_rect(self):
        self.scene.append([100, 100, self.canvas.create_rectangle(100,100, 500, 500,outline="black", fill="red"), 1])
        

    def draw_example_state(self):
        points1 = [ -79.2316628792895,38.4804961745132,
                    0, 0, 50, 50,
                    -79.2316628792895,38.4804961745132, -79.2316628792895+100,38.4804961745132+100,
                    0+100, 0+100, 50+100, 50+100,
                    -79.2316628792895+100,38.4804961745132+100]
        
        color = ("red", "orange", "yellow", "green", "blue")[random.randint(0,4)]
        self.scene.append([points1[0], points1[1], self.canvas.create_polygon(points1, outline="black", fill=color), 1])
        self.canvas.move(self.scene[0][2], 500, 500);
        
    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def motion(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)
        #print(self.x, self.y)


    def zoom_both(self, event):
        zoom_factor = self.zoom_factor
        if event.delta != abs(event.delta):
            print("out")
            self.zoom(1/zoom_factor)
        else:
            print("in")
            self.zoom(zoom_factor)

    def zoom_in(self, event):
        zoom_factor = self.zoom_factor
        self.zoom(zoom_factor)

    def zoom_out(self, event):
        zoom_factor = self.zoom_factor
        self.zoom(1/zoom_factor)
        
    def zoom(self, zoom_factor):
        #A zoom cap of 1 prevents user from scaling further than the default
        zoom_out_cap = 1
        zoom_in_cap = 8

        #Scroll region resizes proportionally
        orig_size = self.scene[0][3]*zoom_factor
        print("orig", orig_size)
        if orig_size>=zoom_out_cap and orig_size<=zoom_in_cap:
            #print("BEFORE CHANGE"+str(self.vertices))
            vertices_dist = abs(self.vertices[2] - self.vertices[0])
            vertices_dist = abs(self.vertices[3] - self.vertices[1])

            left_x_dist = abs(self.x - self.vertices[0])
            left_y_dist = abs(self.y - self.vertices[1])

            right_x_dist = self.vertices[2] - self.x
            right_y_dist = self.vertices[3] - self.y

            self.vertices = [self.x - left_x_dist*zoom_factor, self.y - left_y_dist*zoom_factor, self.x + right_x_dist*zoom_factor, self.y + right_y_dist*zoom_factor]
            #print("AFTER CHANGE"+str(self.vertices))
   
            self.canvas.configure(scrollregion=(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]))

        #Scales individual shapes
        for shape in self.scene:
            x = shape[0]
            y = shape[1]
            rect = shape[2]
            orig_size = shape[3]
            orig_size*=zoom_factor
            if orig_size>=zoom_out_cap and orig_size<=zoom_in_cap:
                shape[3]*=zoom_factor
                self.canvas.scale( rect, self.x, self.y, zoom_factor, zoom_factor)




if __name__ == "__main__":
    root = tk.Tk()
    FiftyStatesSimulator(root).pack(fill="both", expand=True)
    root.mainloop()
