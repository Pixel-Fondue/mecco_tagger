#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = 'tagger.pTagClipboard'

class CMD_tagger(lxu.command.BasicCommand):

    _clipboard = {'material': None, 'part': None, 'pick': None}

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.dyna_Add('tagType', lx.symbol.sTYPE_STRING)
        self.dyna_Add('connected', lx.symbol.sTYPE_BOOLEAN)

        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    @classmethod
    def set_clipboard(cls, key, value):
        cls._clipboard[key] = value

    def basic_Execute(self, msg, flags):
        try:
            mode = self.dyna_String(0) if self.dyna_IsSet(0) else None
            if not mode and self._clipboard:
                mode = 'paste'
            else:
                mode = 'copy'

            tagType = self.dyna_String(1) if self.dyna_IsSet(1) else 'material'
            connected = self.dyna_String(2) if self.dyna_IsSet(2) else False

            if mode == COPY:
                self.set_clipboard(tagType, tagger.selection.get_polys()[0].tags()[tagType])

            elif mode == PASTE:
                args = {}
                args[NAME] = self._clipboard[tagType]
                args[MODE] = tagType
                args[CONNECTED] = connected

                lx.eval(tagger.symbols.COMMAND_NAME_PTAG + tagger.util.build_arg_string(args))

        except:
            traceback.print_exc()


lx.bless(CMD_tagger, NAME_CMD)
