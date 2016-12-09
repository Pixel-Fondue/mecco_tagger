#python

import lx

DEFAULT_PTAG = lx.symbol.i_POLYTAG_MATERIAL
DEFAULT_RANDOM_COLOR_SATURATION = .7
DEFAULT_RANDOM_COLOR_VALUE = .95
DEFAULT_MATERIAL_NAME = 'material'

CMD_SET_MATERIAL = 'tagger.setMaterial_auto'
CMD_REMOVE_MATERIAL = 'tagger.removeMaterial_auto'
CMD_SET_PTAG = 'tagger.setMaterial_pTag'
CMD_REMOVE_PTAG = 'tagger.removeMaterial_pTag'
CMD_SET_ITEM = 'tagger.setMaterial_item'
CMD_SET_GROUP = 'tagger.setMaterial_group'
CMD_SELECT_CONNECTED_BY_TAG = 'tagger.selectConnectedByTag'
CMD_PTAG_SET = 'tagger.pTagSet'
CMD_PTAG_CLIPBOARD = 'tagger.pTagClipboard'
CMD_PTAG_INSPECT = 'tagger.pTagInspect'
CMD_PTAG_REMOVEALL = 'tagger.pTagRemoveAll'
CMD_PTAG_REPLACE = 'tagger.pTagReplace'
CMD_PTAG_SELECTION_FCL = 'tagger.pTagSelectionFCL'
CMD_SELECT_ALL_BY_TAG = 'tagger.selectAllByTag'
CMD_TAG_WITH_MASKED = 'tagger.tagWithMasked'

GROUPNAME = "group"
MATNAME = "material"
SHADERNAME = "shader"
BASE_SHADER = 'Base Shader'
BASE_MATERIAL = 'Base Material'

GTYP = "GTYP"

GROUP_TYPES_STANDARD = ''
GROUP_TYPES_ASSEMBLY = 'assembly'

NAME = 'name'
MODE = 'mode'
OPERATION = 'operation'
CONNECTED = 'connected'
REMOVE_SCOPE = 'scope'
PRESET = 'preset'
TAGTYPE = 'tagType'
COPY = 'copy'
PASTE = 'paste'
MATERIAL = 'material'
PICK = 'pick'
PART = 'part'
TAG = 'tag'
i_POLYTAG = 'i_POLYTAG'
MASK = 'mask'
COPYMASK = 'copyMask'
REPLACETAG = 'replaceTag'
WITHTAG = 'withTag'
QUERY = 'query'
RANDOM = 'random'
DELETE_UNUSED_MASKS = 'delete_unused'
WITH_EXISTING = 'withExisting'
GET_MORE_PRESETS = 'getMorePresets'
GET_MORE_PRESETS_URL = 'http://www.mechanicalcolor.com/coming-soon'
OPERATION = 'operation'
REMOVE = 'remove'
ADD = 'add'

LABEL_TAGTYPE = "Tag Type"
LABEL_TAG = "Tag"
LABEL_TAGS = "Tags"
LABEL_PRESET = "Preset"
LABEL_CONNECTED = "Connected"
LABEL_REMOVE_SCOPE = "Remove From"
LABEL_NONE = "(none)"
LABEL_REPLACE_TAG = "Replace Tag"
LABEL_WITH_TAG = "With Tag"
LABEL_RANDOM_COLOR = "Random Color"
LABEL_GET_MORE_PRESETS = "Get more presets..."
LABEL_WITH_EXISTING = "With Existing"
LABEL_DELETE_UNUSED_MASKS = "Cleanup unused masks"
LABEL_OPERATION = "Operation"

POPUPS_CONNECTED = [(0,'Selected Polys'), (1,'Connected Polys'), (2,'Flood Polys')]
POPUPS_REMOVE_SCOPE = [(0,'Selected Polys'), (1,'Connected Polys'), (2,'Flood Polys'), (3,'Entire Scene')]
POPUPS_TAGTYPES = [('material','Material'), ('part','Part'), ('pick','Selection Set')]
POPUPS_WITH_EXISTING = [('use','Use'), ('keep','Keep and add'), ('remove','Remove and add'), ('consolidate','Consolidate and add')]
POPUPS_ADD_REMOVE = [(ADD, ADD.title()), (REMOVE, REMOVE.title())]

FILTER_TYPES_AUTO = 'auto'
FILTER_TYPES_MATERIAL = 'material'
FILTER_TYPES_PART = 'part'
FILTER_TYPES_PICK = 'selection'
FILTER_TYPES_ITEM = 'item'
FILTER_TYPES_ACTIVE = 'active'
FILTER_TYPES_GLOC = 'folder'
FILTER_TYPES_GROUP = 'group'

OPERATIONS_ADD = ADD
OPERATIONS_REMOVE = REMOVE

def sICHAN_MASK_PTYP(i_POLYTAG):
    """Returns a suitable string for a mask item's lx.symbol.sICHAN_MASK_PTYP channel
    based on an lx.symbol.i_POLYTAG_* symbol."""

    return {
        lx.symbol.i_POLYTAG_MATERIAL:'Material',
        lx.symbol.i_POLYTAG_PICK:'Selection Set',
        lx.symbol.i_POLYTAG_PART:'Part'
    }[i_POLYTAG]

def i_POLYTAG(sICHAN_MASK_PTYP):
    """Returns an lx.symbol.i_POLYTAG_* symbol based on a mask
    item's lx.symbol.sICHAN_MASK_PTYP channel string."""

    return {
        '':lx.symbol.i_POLYTAG_MATERIAL,
        'Material':lx.symbol.i_POLYTAG_MATERIAL,
        'Selection Set':lx.symbol.i_POLYTAG_PICK,
        'Part':lx.symbol.i_POLYTAG_PART
    }[sICHAN_MASK_PTYP]
