from xml.dom.minidom import parse
import xml.dom.minidom

#Test how to parse the polygon information and additional state information from a kml file

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
                #print(col)
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
                    #print(float(num.strip()))
                    plist.append(float(num.strip()))
        slist.append(plist)
        #print(coord.childNodes[0].data)
    vlist.append(slist)
        
