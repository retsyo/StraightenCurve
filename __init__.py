# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

#Author: Lee June
#Please read 'readme.en.txt'(in English) or readme.cn.txt(in Chinese) for details

DEBUG=False
if DEBUG:
    import os
    os.system('cls')

import bpy

#I don't know how to i18n bl_info
bl_info = {
    "name": "Straighten curve",
    "description": "straighten curve without changing every segment's length",
    "author": "Lee June",
    "version": (0, 4),
    "blender": (2, 69, 0),
    "location": "Toolshelf",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/retsyo/StraightenCurve",
    "category": "Create"}

################################################################################
#            the following code is used for i18n                               #
useEnglishGui=False   # if you want use English GUI always, please set it to True
#~ useEnglishGui=True

def aid(s): return s
if useEnglishGui:
    _=aid
else:
    import gettext
    import locale
    import os

    #~ _=gettext.translation('messages','.').gettext
    current_locale, encoding = locale.getdefaultlocale()
    current_locale=bpy.utils._user_preferences.system.language
    if DEBUG:
        print('current_locale', current_locale)
        print('encoding', encoding)

    myPath=os.path.split(os.path.realpath(__file__))[0]
    if DEBUG:
        print('myPath=', myPath)
    locale_path = os.path.join(myPath, 'locale')
    if DEBUG:
        print ('locale_path', locale_path)
    #~ if current_locale=='DEFAULT':
        #~ current_locale='en_US'

    if not gettext.find('messages', locale_path, [current_locale], all=True):
        current_locale='en_US'

    if current_locale=='en_US':
        _=aid
    else:

        language = gettext.translation ('messages', locale_path, [current_locale] )
        language.install()

#                             end code for i18n                                #
################################################################################



class StraightenCurve(bpy.types.Operator):
    """straighten curve without changing every segment's length"""
    bl_idname = "scene.create_straighten_curve"
    bl_label = _("straighten")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        oldObj=bpy.context.active_object

        if oldObj:
            bpy.ops.object.select_pattern(pattern = oldObj.name, extend=False )

        if bpy.context.active_object and bpy.context.active_object.type=='CURVE':
            oldObjName=oldObj.name
            oldObjFill=oldObj.data.fill_mode
            oldObjDepth=oldObj.data.bevel_depth
            oldObjResolution=oldObj.data.bevel_resolution

            #这一个，会报告
            #~ RuntimeError: Operator bpy.ops.mesh.select_all.poll() failed, context is incorrect
            #bpy.ops.mesh.select_all(action="DESELECT")
            #所以采用了下面的方法
            #~ allObj=bpy.data.objects
            #~ for i in allObj:
                #~ i.select=False

            #复制原始的curve
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})

            dupObj=bpy.context.active_object
            if DEBUG:
                print (dupObj.data.bevel_depth)
                print (dupObj.data.bevel_resolution)
                print (dupObj.scale)
            dupObjDepth=dupObj.data.bevel_depth
            dupObjResolution=dupObj.data.bevel_resolution

            #如果用户已经给管子直径，则不能得到正确结果。所以必须将厚度变成0.0
            dupObj.data.bevel_depth=0.0

            bpy.context.object.name = '%s.tmp' % oldObjName

            #转换为mesh之后，才能获取各顶点坐标
            bpy.ops.object.convert(target='MESH')

            #必须应用这些，否则尺寸不会对(?)
            #~ bpy.ops.object.visual_transform_apply()
            bpy.ops.object.transform_apply(location=True, scale=True, rotation=True)
            if DEBUG:
                print (dupObj.scale)

            #bpy.ops.object.mode_set(mode="EDIT")

            bpy.ops.mesh.separate(type='LOOSE')

            bpy.ops.object.mode_set(mode="OBJECT")

            #bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

            #分开的物体，全部都是被选择状态
            allSelectedObj=bpy.data.objects
            allSelectedObj=[i for i in allSelectedObj if i.select]

            #~ bpy.ops.mesh.select_all(action="DESELECT")
            for i in allSelectedObj:
                i.select=False

            for everyObj in allSelectedObj:

                vertices=[]
                distance=[]

                for i in everyObj.data.vertices:
                    vertices.append (i.co)

                vertices1=vertices[:-1]
                vertices2=vertices[1:]
                for i in range(len(vertices)-1):
                    p=vertices1[i]
                    q=vertices2[i]
                    distance.append((p-q).length)


                #删除不需要的临时mesh对象
                #extend=False只找完全一样的名字，而不是作为子串
                bpy.ops.object.select_pattern(pattern= everyObj.name, extend = False)
                #276不能用 bpy.ops.objects.select_name
                bpy.ops.object.delete()


                # 创建一个点，位于曲线第一点
                #首先创建一个正方形
                bpy.ops.mesh.primitive_plane_add(location=vertices[0], enter_editmode = True)
                #~ bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0), enter_editmode = True)
                #~ x, y, z=vertices[0].x, vertices[0].y, vertices[0].z
                #~ bpy.ops.mesh.primitive_plane_add(location=(x, y, z), enter_editmode = True)

                # 四个点在正方形中心合并为一个点
                bpy.ops.mesh.merge(type='COLLAPSE')

                #设置为点选取模式
                bpy.context.tool_settings.mesh_select_mode = (True, False, False)

                objNew=bpy.context.object
                objNew.name='%s.straight' % everyObj.name

                for i in distance:
                    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (i, 0, 0)})


                bpy.ops.object.mode_set(mode="OBJECT")



                bpy.ops.object.convert(target='CURVE')

                oldObj.data.bevel_depth=oldObjDepth
                oldObj.data.bevel_resolution=oldObjResolution

                bpy.context.active_object.data.fill_mode=oldObjFill
                bpy.context.active_object.data.bevel_depth=oldObjDepth
                bpy.context.active_object.data.bevel_resolution=oldObjResolution

                if DEBUG:
                    print (bpy.context.active_object.scale)


                scale=oldObj.scale[0]/bpy.context.active_object.scale[0]
                bpy.ops.transform.resize(value=(1, scale, scale))

            #合并拆分出来的各个曲线
            for i in allSelectedObj:
                i.select=True
            bpy.ops.object.join()
            bpy.context.object.name='%s.straight' % oldObj.name

            for i in bpy.data.objects:
                #~ print (dir(i))
                i.select=False

            bpy.context.scene.update()

            #选择操作，并不将物体设置为active；但是单纯设置active，物体也没有被选中（外面没有黄色的线）
            #所以这里必须进行2个操作
            bpy.context.scene.objects.active=oldObj
            bpy.ops.object.select_pattern(pattern = oldObj.name, extend=False )


        return {'FINISHED'}


#----------------------------------------- Create panel in the toolshelf -------------------------------------------------

class CreateStraightenCurvePanel(bpy.types.Panel):
    bl_label = _("Straighten curve")
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Straighten curve"

    def draw(self, context):

        # column buttons solution. Less space than single buttons ...
        layout = self.layout
        view = context.space_data
        # Three buttons
        col = layout.column(align=True)

        col.operator("scene.create_straighten_curve", text=_("straighten"))

# -------------------------------------------------------------------------------------------

# store keymaps here to access after registration
addon_keymaps = []


def register():

    bpy.utils.register_class(StraightenCurve)


    bpy.utils.register_class(CreateStraightenCurvePanel)

    #~ # handle the keymap
    #~ wm = bpy.context.window_manager
    #~ km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')


    #~ kmi = km.keymap_items.new(StraightenCurve.bl_idname, 'TWO', 'PRESS', ctrl=True, shift=True, alt=True)


    #~ addon_keymaps.append(km)

def unregister():

    bpy.utils.unregister_class(StraightenCurve)


    bpy.utils.unregister_class(CreateStraightenCurvePanel)

    #~ # handle the keymap
    #~ wm = bpy.context.window_manager
    #~ for km in addon_keymaps:
        #~ wm.keyconfigs.addon.keymaps.remove(km)
    #~ # clear the list
    #~ del addon_keymaps[:]


if __name__ == "__main__":
    register()


