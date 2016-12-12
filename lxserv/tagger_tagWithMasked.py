# python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_TAG_WITH_MASKED

class CommandClass(tagger.Commander):
    _commander_last_used = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        connected = self.commander_arg_value(0)

        masks = set()

        for i in modo.Scene().selected:
            if i.type == 'mask':
                masks.add(i)

        if len(masks) < 1:
            modo.dialogs.alert(tagger.DIALOGS_NO_MASK_SELECTED)
            return

        if len(masks) > 1:
            modo.dialogs.alert(tagger.DIALOGS_TOO_MANY_MASKS)
            return

        mask = list(masks)[0]

        if not mask.channel(lx.symbol.sICHAN_MASK_PTAG).get():
            modo.dialogs.alert(tagger.DIALOGS_NO_PTAG_FILTER)
            return

        if mask.channel(lx.symbol.sICHAN_MASK_PTAG).get() == "(none)":
            modo.dialogs.alert(tagger.DIALOGS_NONE_PTAG_FILTER)
            return

        tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
        tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

        tagger.selection.tag_polys(tag, connected, tagger.util.string_to_i_POLYTAG(tagLabel))


lx.bless(CommandClass, NAME_CMD)