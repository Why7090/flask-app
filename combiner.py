import xml.etree.ElementTree as ET
from PIL import Image



class XML:
    
    def PartList(self):
        
        pltree = [ET.parse('tempmods/0/PartList.xml'), ET.parse('tempmods/1/PartList.xml')]
        sstree = [ET.parse('tempmods/0/ShipSprites.xml')]
        r = [pltree[0].getroot(), pltree[1].getroot()]
        ssr = [sstree[0].getroot(), sstree[1].getroot()]


        for i in range(len(ssr[0].findall('.//*[@n]'))):
            ssr[0].findall('.//*[@n]')[i].attrib['n'] = ssr[0].findall('.//*[@n]')[i].attrib['n'].lower()

        for i in range(len(ssr[1].findall('.//*[@n]'))):
            ssr[1].findall('.//*[@n]')[i].attrib['n'] = ssr[1].findall('.//*[@n]')[i].attrib['n'].upper()


        for i in range(len(r[0].findall('.//*[@id]'))):
            
            i_ = r[0].findall('.//*[@id]')[i][:]
            del i_.attrib['id'], i_.attrib['sprite'], i_.attrib['description']

            r[0].findall('.//*[@sprite]')[i] = r[0].findall('.//*[@sprite]')[i].lower()

            for j in range(len(r[1].findall('.//*[@id]'))):
                
                j_ = r[1].findall('.//*[@id]')[j][:]
                del j_.attrib['id'], j_.attrib['sprite'], j_.attrib['description']
                
                if i_.attrib == j_.attrib:
                    r[1].remove(j)

                else:
                    while r[0].findall('.//*[@id="'+r[1].findall('.//*[@id]')[j].attrib['id']+'"]'):
                        r[1].findall('.//*[@id]')[j].attrib['id'] += '-'

        for i in range(len(r[1].findall('.//*[@id]'))):
            r[1].findall('.//*[@sprite]')[i] = r[1].findall('.//*[@sprite]')[i].upper()



class Sprites:
        
    def combine(self, path1, path2, out):
        try:
            im1 = Image.open(path1)
        except:
            im1 = None
             
        try:
            im2 = Image.open(path2)
        except:
            im2 = None

        self.con = []
        im1 and im2 and self.con.append(1)or not im1 and not im2 or im1 and im1.save(out, quality=100) or im2 and im2.save(out, quality=100)
        if not self.con:
            return
        self.new_im = Image.new('RGBA', [im1.size[0]+im2.size[0], im1.size[1]>=im2.size[1] and im1.size[1] or im2.size[1]])

        self.new_im.paste(im1, (0, 0))
        self.new_im.paste(im2, (im1.size[0], 0))

        self.new_im.save(out, quality=100)

    def run(self):
        self.combine('tempmods/0/ShipSprites.png', 'tempmods/1/ShipSprites.png', 'tempmods/out/ShipSprites.png')
        self.combine('tempmods/0/PlanetSprites.png', 'tempmods/1/PlanetSprites.png', 'tempmods/out/PlanetSprites.png')


if __name__ == '__main__':
    Sprites().run()

