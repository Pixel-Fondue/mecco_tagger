# python

import lx, tagger, modo

CMD_NAME = tagger.CMD_SET_PTAG_ISLANDS

_island_enumerator = 0

class IslandCounterClass(tagger.MeshEditorClass):
    island_count = 0

    def mesh_read_action(self):
        global _island_enumerator

        islands = self.get_active_polys_by_island()

        for i, island in enumerate(islands):
            self.island_count += 1
            _island_enumerator += 1


class MeshEditorClass(tagger.MeshEditorClass):
    island_count = 0
    poly_count = 0

    def mesh_edit_action(self):
        global _island_enumerator

        i_POLYTAG = tagger.convert_to_iPOLYTAG(self.args[tagger.TAGTYPE])
        stringTag = lx.object.StringTag()
        stringTag.set(self.polygon_accessor)

        islands = self.get_selected_polys_by_island()

        for i, island in enumerate(islands):

            self.island_count += 1
            _island_enumerator += 1
            pTag = "_".join((self.args[tagger.TAG], str(_island_enumerator)))
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag)

            for poly in island:
                self.polygon_accessor.Select(poly)
                stringTag.Set(i_POLYTAG, pTag)
                self.poly_count += 1


class CommandClass(tagger.CommanderClass):
    #_commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG,
                    'datatype': 'string',
                    'default': '',
                    'values_list_type': 'sPresetText',
                    'values_list': tagger.scene.all_tags,
                    'flags': ['optional'],
                }, {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'default': tagger.MATERIAL,
                    'flags': [],
                    'values_list_type': 'popup',
                    'values_list': tagger.POPUPS_TAGTYPES
                }
            ]

    def commander_execute(self, msg, flags):
        global _island_enumerator
        args = self.commander_args()

        _island_enumerator = 0
        island_counter = IslandCounterClass(args, [lx.symbol.f_MESHEDIT_POL_TAGS])
        island_counter.do_mesh_read()

        if _island_enumerator > tagger.MAX_PTAG_ISLANDS:
            try:
                modo.dialogs.alert(
                    tagger.DIALOGS_TOO_MANY_ISLANDS[0],
                    tagger.DIALOGS_TOO_MANY_ISLANDS[1] % (tagger.MAX_PTAG_ISLANDS, _island_enumerator)
                )
            except:
                pass

        else:
            _island_enumerator = 0
            mesh_editor = MeshEditorClass(args, [lx.symbol.f_MESHEDIT_POL_TAGS])
            mesh_editor.do_mesh_edit()

            try:
                modo.dialogs.alert(
                    tagger.DIALOGS_TAGGED_POLY_ISLANDS_COUNT[0],
                    tagger.DIALOGS_TAGGED_POLY_ISLANDS_COUNT[1] % (mesh_editor.poly_count, _island_enumerator)
                    )
            except:
                pass

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

lx.bless(CommandClass, CMD_NAME)
