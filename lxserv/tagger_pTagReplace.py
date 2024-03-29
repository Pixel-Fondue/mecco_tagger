# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REPLACE
DEFAULTS = [tagger.MATERIAL, '', '']

def selected_tag(tagType):
    active_layers = tagger.items.get_active_layers()
    polys = []
    if active_layers:
        for layer in active_layers:
            polys.extend(layer.geometry.polygons.selected)
        if polys:
            return polys[0].tags()[tagType]
        elif not polys:
            return DEFAULTS[1]
    elif not active:
        return DEFAULTS[1]

class CommandClass(tagger.CommanderClass):
    #_commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'default': tagger.MATERIAL,
                    'values_list_type': 'popup',
                    'values_list': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }, {
                    'name': tagger.REPLACETAG,
                    'label': tagger.LABEL_REPLACE_TAG,
                    'datatype': 'string',
                    'default': selected_tag(tagger.MATERIAL),
                    'flags': [],
                    'values_list_type': 'sPresetText',
                    'values_list': tagger.scene.all_tags
                }, {
                    'name': tagger.WITHTAG,
                    'label': tagger.LABEL_WITH_TAG,
                    'datatype': 'string',
                    'default': "",
                    'flags': ['optional'],
                    'values_list_type': 'sPresetText',
                    'values_list': tagger.scene.all_tags
                }, {
                    'name': tagger.IGNORE_CASE,
                    'label': tagger.LABEL_IGNORE_CASE,
                    'datatype': 'boolean',
                    'value': False,
                    'flags': ['optional']
                }, {
                    'name': tagger.REGEXP,
                    'label': tagger.LABEL_REGEXP,
                    'datatype': 'boolean',
                    'value': False,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        replaceTag = self.commander_arg_value(1)
        withTag = self.commander_arg_value(2)
        ignoreCase = self.commander_arg_value(3)
        regexp = self.commander_arg_value(4)

        if not withTag:
            withTag = None

        hitcount = tagger.scene.replace_tag(tagType, replaceTag, withTag, ignoreCase, regexp)

        if hitcount == 0:
            try:
                modo.dialogs.alert(
                    tagger.DIALOGS_TAG_NOT_FOUND[0],
                    tagger.DIALOGS_TAG_NOT_FOUND[1] % (tagType, replaceTag)
                    )
            except:
                pass

        elif hitcount >= 1:
            try:
                modo.dialogs.alert(
                    tagger.DIALOGS_TAG_REPLACED[0],
                    tagger.DIALOGS_TAG_REPLACED[1] % (hitcount, tagType, replaceTag)
                    )
            except:
                pass

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)



lx.bless(CommandClass, CMD_NAME)
