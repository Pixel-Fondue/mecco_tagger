# python

""" Allows you to write typical MODO commands with much less boilerplate,
less redundant code, and fewer common mistakes. The following is a
blessed modo command using Commander:

class CommandClass(tagger.Commander):
    def commander_arguments(self):
        return [
                {
                    'name': 'myGreatString',
                    'label': 'Input String Here',
                    'datatype': 'string',
                    'value': "default string goes here",
                    'flags': [],
                    'sPresetText': function_that_returns_list_of_possible_strings()
                }, {
                    'name': 'greeting',
                    'datatype': 'string',
                    'value': 'hello',
                    'popup': ['hello', 'greetings', 'how ya doin\'?'],
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        myGreatString = self.commander_arg_value(0)
        greeting = self.commander_arg_value(1)

        lx.out("%s, %s" (greeting, myGreatString))
"""

__version__ = "0.19"
__author__ = "Adam"

import lx, lxu, traceback
from lxifc import UIValueHints, Visitor
from operator import ior

ARG_NAME = 'name'
ARG_LABEL = 'label'
ARG_VALUE = 'value'
ARG_DATATYPE = 'datatype'
ARG_POPUP = 'popup'
ARG_FCL = 'fcl'
ARG_FLAGS = 'flags'
ARG_sPresetText = 'sPresetText'

sTYPE_FLOATs = [
        'acceleration',
        'angle',
        'axis',
        'color1',
        'float',
        'force',
        'light',
        'mass',
        'percent',
        'speed',
        'time',
        'uvcoord'
    ]

sTYPE_STRINGs = [
        'date',
        'datetime',
        'filepath',
        'string',
        'vertmapname'
    ]

sTYPE_STRING_vectors = [
        'angle3',
        'color',
        'float3',
        'percent3'
    ]

sTYPE_INTEGERs = [
        'integer'
    ]

sTYPE_BOOLEANs = [
        'boolean'
    ]

class FormCommandListClass(UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]

class PopupClass(UIValueHints):
    def __init__(self, items):
        if not items or not isinstance(items, (list, tuple)):
            self._user = []
            self._internal = []

        elif isinstance(items[0], (list, tuple)):
            self._user = [str(i[1]) for i in items]
            self._internal = [str(i[0]) for i in items]

        else:
            self._user = [str(i) for i in items]
            self._internal = [str(i) for i in items]

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._internal)

    def uiv_PopUserName(self,index):
        return self._user[index]

    def uiv_PopInternalName(self,index):
        return self._internal[index]

class SetMarksClass (Visitor):
    def __init__ (self, acc, mark):
        self.acc = acc
        self.mark = mark

    def vis_Evaluate (self):
        self.acc.SetMarks (self.mark)

class PolysByIslandClass (Visitor):
    def __init__ (self, polygon, point, mark):
        self.polygon = polygon
        self.point = point
        self.mark = mark
        self.islands = []

    def vis_Evaluate (self):
        inner = set ()
        outer = set ()

        outer.add (self.polygon.ID ())

        while len(outer) > 0:
            polygon_ID = outer.pop ()

            self.polygon.Select (polygon_ID)
            self.polygon.SetMarks (self.mark)
            inner.add (polygon_ID)

            num_points = self.polygon.VertexCount ()
            for v in xrange (num_points):
                self.point.Select (self.polygon.VertexByIndex (v))
                num_polys = self.point.PolygonCount ()
                for p in xrange (num_polys):
                    vert_polygon_ID = self.point.PolygonByIndex (p)
                    if vert_polygon_ID not in inner:
                        outer.add (vert_polygon_ID)
        self.islands.append (inner)

class MeshEditorClass():
    def __init__(self, args = None, mesh_edit_flags = []):
        self.args = args
        self.mesh_edit_flags = mesh_edit_flags
        self.mesh_svc = None
        self.mesh = None
        self.mark_mode_checked = None
        self.mark_mode_unchecked = None
        self.polygon_accessor = None
        self.edge_accessor = None
        self.meshmap_accessor = None
        self.point_accessor = None

    def mesh_edit_action(self):
        return None

    def mesh_read_action(self):
        return None

    def do_mesh_edit(self):
        return self.mesh_edit()

    def do_mesh_read(self):
        return self.mesh_edit(True)

    def mesh_edit(self, read_only=False):
        """Adapted from James O'Hare's excellent code: https://gist.github.com/Farfarer/31148a78f392a831239d9b018b90330c"""

        if read_only:
            scan_allocate = lx.symbol.f_LAYERSCAN_ACTIVE
        if not read_only:
            scan_allocate = lx.symbol.f_LAYERSCAN_EDIT

        layer_svc = lx.service.Layer ()
        layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (scan_allocate))

        if not layer_scan.test ():
            return

        self.mesh_svc = lx.service.Mesh ()
        self.mark_mode_checked = self.mesh_svc.ModeCompose ('user0', None)
        self.mark_mode_unchecked = self.mesh_svc.ModeCompose (None, 'user0')

        for n in xrange (layer_scan.Count ()):
            if read_only:
                self.mesh = lx.object.Mesh (layer_scan.MeshBase(n))
            if not read_only:
                self.mesh = lx.object.Mesh (layer_scan.MeshEdit(n))

            if not self.mesh.test ():
                continue

            polygon_count = self.mesh.PolygonCount ()
            if polygon_count == 0:
                continue

            self.polygon_accessor = lx.object.Polygon (self.mesh.PolygonAccessor ())
            if not self.polygon_accessor.test ():
                continue

            self.edge_accessor = lx.object.Edge (self.mesh.EdgeAccessor ())
            if not self.edge_accessor.test ():
                continue

            self.point_accessor = lx.object.Point (self.mesh.PointAccessor ())
            if not self.point_accessor.test ():
                continue

            self.meshmap_accessor = lx.object.MeshMap (self.mesh.MeshMapAccessor ())
            if not self.meshmap_accessor.test ():
                continue

            visClear = SetMarksClass (self.polygon_accessor, self.mark_mode_unchecked)
            self.polygon_accessor.Enumerate (self.mark_mode_checked, visClear, 0)

            if read_only:
                self.mesh_read_action()
            if not read_only:
                self.mesh_edit_action()

            if self.mesh_edit_flags and not read_only:
                layer_scan.SetMeshChange (n, reduce(ior, self.mesh_edit_flags))

        layer_scan.Apply ()

    def get_polys_by_island(self):
        visIslands = PolysByIslandClass (self.polygon_accessor, self.point_accessor, self.mark_mode_checked)
        self.polygon_accessor.Enumerate (self.mark_mode_unchecked, visIslands, 0)

        return visIslands.islands

    def get_polys_by_selected(self):
        mark_mode = self.mesh_svc.ModeCompose (lx.symbol.sMARK_SELECT, 'hide lock')

        selectedPolygons = set()

        polyCount = self.mesh.PolygonCount ()
        for p in xrange(polyCount):
            self.polygon_accessor.SelectByIndex(p)
            if self.polygon_accessor.TestMarks (mark_mode):
                selectedPolygons.add (self.polygon_accessor.ID())

        return selectedPolygons


class Commander(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        for n, argument in enumerate(self.commander_arguments()):

            if not argument.get(ARG_DATATYPE):
                return lx.symbol.e_FAILED

            if not argument.get(ARG_NAME):
                return lx.symbol.e_FAILED

            datatype = getattr(lx.symbol, 'sTYPE_' + argument[ARG_DATATYPE].upper())
            if not datatype:
                return lx.symbol.e_FAILED

            self.dyna_Add(argument[ARG_NAME], datatype)

            flags = []
            for flag in argument.get(ARG_FLAGS, []):
                flags.append(getattr(lx.symbol, 'fCMDARG_' + flag.upper()))
            if flags:
                self.basic_SetFlags(n, reduce(ior, flags))

        self.not_svc = lx.service.NotifySys()

        self.notifiers = []
        self.notifier_tuples = tuple([i for i in self.commander_notifiers()])
        for i in self.notifier_tuples:
            self.notifiers.append(None)

    def commander_arguments(self):
        return []

    def commander_notifiers(self):
        return []

    def commander_arg_value(self, index):
        if not self.dyna_IsSet(index):
            return None

        if self.commander_arguments()[index][ARG_DATATYPE].lower() in sTYPE_STRINGs:
            return self.dyna_String(index)

        elif self.commander_arguments()[index][ARG_DATATYPE].lower() in sTYPE_STRING_vectors:
            return [float(i) for i in self.dyna_String(index).split(" ")]

        elif self.commander_arguments()[index][ARG_DATATYPE].lower() in sTYPE_INTEGERs:
            return self.dyna_Int(index)

        elif self.commander_arguments()[index][ARG_DATATYPE].lower in sTYPE_FLOATs:
            return self.dyna_Float(index)

        elif self.commander_arguments()[index][ARG_DATATYPE].lower() in sTYPE_BOOLEANs:
            return self.dyna_Bool(index)

        return None

    def cmd_NotifyAddClient(self, argument, object):
        for i, tup in enumerate(self.notifier_tuples):
            if self.notifiers[i] is None:
                self.notifiers[i] = self.not_svc.Spawn (self.notifier_tuples[i][0], self.notifier_tuples[i][1])

            self.notifiers[i].AddClient(object)

    def cmd_NotifyRemoveClient(self, object):
        for i, tup in enumerate(self.notifier_tuples):
            if self.notifiers[i] is not None:
                self.notifiers[i].RemoveClient(object)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        args = self.commander_arguments()
        if index < len(args):
            label = args[index].get(ARG_LABEL)
            if not label:
                label = args[index].get(ARG_NAME)
            hints.Label(label)

            if args[index].get(ARG_sPresetText):
                hints.Class("sPresetText")

    def arg_UIValueHints(self, index):
        args = self.commander_arguments()
        if index < len(args):
            if args[index].get(ARG_POPUP) is not None:
                return PopupClass(args[index].get(ARG_POPUP, []))
            elif args[index].get(ARG_sPresetText) is not None:
                return PopupClass(args[index].get(ARG_sPresetText, []))
            elif args[index].get(ARG_FCL) is not None:
                return FormCommandListClass(args[index].get(ARG_FCL, []))

    def cmd_DialogInit(self):
        for n, argument in enumerate(self.commander_arguments()):

            if self.dyna_IsSet(n):
                continue

            if self.commander_arguments()[n].get(ARG_VALUE) == None:
                continue

            datatype = argument.get(ARG_DATATYPE, '').lower()
            default_value = self.commander_arguments()[n].get(ARG_VALUE)

            if datatype in sTYPE_STRINGs:
                self.attr_SetString(n, str(default_value))

            elif datatype in sTYPE_STRING_vectors:
                self.attr_SetString(n, str(default_value))

            elif datatype in sTYPE_INTEGERs:
                self.attr_SetInt(n, int(default_value))

            elif datatype in sTYPE_BOOLEANs:
                self.attr_SetInt(n, int(default_value))

            elif datatype in sTYPE_FLOATs:
                self.attr_SetFlt(n, float(default_value))

    def commander_execute(self, msg, flags):
        pass

    def basic_Execute(self, msg, flags):
        try:
            self.commander_execute(msg, flags)
        except:
            lx.out(traceback.format_exc())

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)

        args = self.commander_arguments()

        if index < len(args):
            is_query = 'query' in args[index].get(ARG_FLAGS, [])
            is_not_fcl = False if args[index].get(ARG_FCL) else True
            has_recent_value = self.commander_arg_value(index)

            if is_query and is_not_fcl and has_recent_value:
                va.AddString(str(self.commander_arg_value(index)))

        return lx.result.OK
