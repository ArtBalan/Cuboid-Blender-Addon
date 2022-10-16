from email.policy import default
import bpy
import random

bl_info = {
    "name": "Cuboid",
    "author": "ArtBal",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

def newMaterial(id):

    mat = bpy.data.materials.get(id)

    if mat is None:
        mat = bpy.data.materials.new(name=id)

    mat.use_nodes = True

    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    return mat

def newShader(id, type, r, g, b):

    mat = newMaterial(id)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')

    if type == "diffuse":
        shader = nodes.new(type='ShaderNodeBsdfDiffuse')
        nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)

    elif type == "emission":
        shader = nodes.new(type='ShaderNodeEmission')
        # Color
        nodes["Emission"].inputs[0].default_value = (r, g, b, 1)
        # Strength
        nodes["Emission"].inputs[1].default_value = 50

    elif type == "glossy":
        shader = nodes.new(type='ShaderNodeBsdfGlossy')
        nodes["Glossy BSDF"].inputs[0].default_value = (r, g, b, 1)
        nodes["Glossy BSDF"].inputs[1].default_value = 0

    links.new(shader.outputs[0], output.inputs[0])

    return mat

def sceneClearence ():
    # Scene clearence
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            o.select_set(True)
        else:
            o.select_set(False)
    bpy.ops.object.delete()


# Displacement functions
def p(x):
    return x/2 + 40

def n(x):
    return x/2 - 40

class Cuboid_PT_Panel(bpy.types.Panel):
    bl_label = "Cuboid Panel"
    bl_idname = "Cuboid_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Create"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("wm.cuboidop")

class WM_OT_cuboidOp(bpy.types.Operator):
    bl_label = "Cuboid Operator"
    bl_idname = "wm.cuboidop"

    iteration : bpy.props.IntProperty(name= "Iterations", default= 3)
    cSize : bpy.props.FloatProperty(name= "Size", default= 3)
    decrease : bpy.props.FloatProperty(name= "Decrease factor", default= 3)

    rand : bpy.props.BoolProperty(name = "Random Placement", default= False)
    fact : bpy.props.IntProperty(name = "Number of Random placement", default= 4)

    wireFrame : bpy.props.BoolProperty(name ="Wireframe:", default= True)

    Exl : bpy.props.BoolProperty(name = "Enable X", default= False)
    Eyl : bpy.props.BoolProperty(name = "Enable Y", default= False)
    Ezl : bpy.props.BoolProperty(name = "Enable Z", default= False)
    
    Epxyl : bpy.props.BoolProperty(name = "Enable PXY", default= False)
    Enxyl : bpy.props.BoolProperty(name = "Enable NXY", default= False)

    Epxzl : bpy.props.BoolProperty(name = "Enable PXY", default= False)
    Enxzl : bpy.props.BoolProperty(name = "Enable NXY", default= False)

    Epyzl : bpy.props.BoolProperty(name = "Enable PXY", default= False)
    Enyzl : bpy.props.BoolProperty(name = "Enable NXY", default= False)

    def draw (self, context):
        layout = self.layout

        PropertyBox = layout.box()
        
        generalProperty = PropertyBox.row()
        generalProperty.prop(self, "iteration")
        generalProperty.prop(self, "cSize")
        generalProperty.prop(self, "decrease")
        
        randomProperty = PropertyBox.row()
        randomProperty.prop(self,"rand")
        if self.rand == True:
            randomProperty.prop(self,"fact")
        
        otherProperty = PropertyBox.row()
        otherProperty.prop(self,"wireFrame")

        mainAxisBox = layout.box()
        mainAxis = mainAxisBox.row()
        mainAxis.prop(self,"Exl")
        mainAxis.prop(self,"Eyl")
        mainAxis.prop(self,"Ezl")

        otherAxisBox = layout.box()
        otherAxis = otherAxisBox.row()
        zFixed = otherAxis.column()
        zFixed.prop(self,'Epxyl')
        zFixed.prop(self,'Enxyl')
        yFixed = otherAxis.column()
        yFixed.prop(self,'Epxzl')
        yFixed.prop(self,'Enxzl')
        xFixed = otherAxis.column()
        xFixed.prop(self,'Epyzl')
        xFixed.prop(self,'Enyzl')


    def execute(self, context):

        iteration = self.iteration
        cSize = self.cSize
        decrease = self.decrease

        Exl = self.Exl
        Eyl = self.Eyl
        Ezl = self.Ezl
        
        Epxyl = self.Epxyl
        Enxyl = self.Enxyl
        
        Epxzl = self.Epxzl
        Enxzl = self.Enxzl

        Epyzl = self.Epyzl
        Enyzl = self.Enyzl
        
        rand = self.rand
        fact = self.fact
        #col

        sceneClearence()

        # element List
        xl = []
        yl = []
        zl = []
        pxyl = []
        nxyl = []
        
        nxzl = []
        pxzl = []

        nyzl = []
        pyzl= []

        x = 0
        y = 0
        z = 0
        r = 2
        c = iteration

        temp = [x,y,z,r,c]

        mat = newShader("Shader1", "emission", 1, 0, 0)

        xMin =-75
        xMax = 75 
        yMin =-75
        yMax = 75 
        zMin =-75
        zMax = 75 

        if Exl:
            if not rand:
                xl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    xl.append(temp)
        if Eyl :
            if not rand:
                yl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    yl.append(temp)

        if Ezl :
            if not rand:
                zl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    zl.append(temp)


        if Epxyl :
            if not rand:
                pxyl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    pxyl.append(temp)

        if Enxyl :
            if not rand:
                nxyl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    nxyl.append(temp)

        if Epxzl :
            if not rand:
                pxzl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    pxzl.append(temp)

        if Enxzl :
            if not rand:
                nxzl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    nxzl.append(temp)        

        if Enyzl :
            if not rand:
                nyzl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    nyzl.append(temp) 

        if Epyzl :
            if not rand:
                pyzl.append(temp)
            else :
                for i in range(0,fact):
                    x = random.randint(xMin,xMax)
                    y = random.randint(yMin,yMax)
                    z = random.randint(zMin,zMax)
                    temp = [x,y,z,r,c]
                    pyzl.append(temp) 

        # X axis
        while len(xl)> 0:
            tl = []
            for el in xl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [n(x),y,z,r-decrease,c-1]
                    b = [p(x),y,z,r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            xl = tl

        # Y axis
        while len(yl)> 0:
            tl = []
            for el in yl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [x,n(y),z,r-decrease,c-1]
                    b = [x,p(y),z,r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            yl = tl

        # Z axis
        while len(zl)> 0:
            tl = []
            for el in zl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [x,y,p(z),r-decrease,c-1]
                    b = [x,y,n(z),r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            zl = tl


        # Horyzontal Diag 1
        while len(pxyl)> 0:
            tl = []
            for el in pxyl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [n(x),n(y),z,r-decrease,c-1]
                    b = [p(x),p(y),z,r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            pxyl = tl
            
        # Horyzontal Diag 2
        while len(nxyl)> 0:
            tl = []
            for el in nxyl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [p(x),n(y),z,r-decrease,c-1]
                    b = [n(x),p(y),z,r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            nxyl = tl

        # Vertical Diag 1
        while len(pxzl)> 0:
            tl = []
            for el in pxzl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [n(x),y,n(z),r-decrease,c-1]
                    b = [p(x),y,p(z),r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            pxzl = tl
            
        # Vertical Diag 2
        while len(nxzl)> 0:
            tl = []
            for el in nxzl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [p(x),y,n(z),r-decrease,c-1]
                    b = [n(x),y,p(z),r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            nxzl = tl

        # Vertical Diag 3
        while len(pyzl)> 0:
            tl = []
            for el in pyzl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [x,n(y),n(z),r-decrease,c-1]
                    b = [x,p(y),p(z),r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            pyzl = tl
            
        # Vertical Diag 4
        while len(nyzl)> 0:
            tl = []
            for el in nyzl:
                x = el[0]
                y = el[1]
                z = el[2]
                r = el[3]
                c = el[4]
                if(c>0):
                    a = [x,p(y),n(z),r-decrease,c-1]
                    b = [x,n(y),p(z),r-decrease,c-1]
                    bpy.ops.mesh.primitive_cube_add(location=(a[0],a[1],a[2]),size=cSize,scale=(r,r,r))
                    bpy.ops.mesh.primitive_cube_add(location=(b[0],b[1],b[2]),size=cSize,scale=(r,r,r))
                    r -= decrease
                    tl.append(a)
                    tl.append(b)
            nyzl = tl


        for obj in bpy.data.objects:
            if obj.type == "MESH":
                if self.wireFrame:
                    obj.modifiers.new("WireFrame", type = "WIREFRAME")
                    obj.modifiers["WireFrame"].thickness = 0.05
                obj.data.materials.append(mat)

                pass
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(Cuboid_PT_Panel)
    bpy.utils.register_class(WM_OT_cuboidOp)
    
def unregister():
    bpy.utils.unregister_class(Cuboid_PT_Panel)
    bpy.utils.unregister_class(WM_OT_cuboidOp)

if __name__ == "__main__":
    register()
