# python

import lx, items, modo


def tag_polys(polys, ptag, i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL):
    """Assigns a pTag of type ptyp. Must be used inside a 'with' statement!
    http://modo.sdk.thefoundry.co.uk/td-sdk/guidelines.html#meshediting102

    :param polys: polys to tag
    :param ptag: tag to apply (str)
    :param connected: extend selection to all connected polys (bool)
    :param ptyp: type of tag to apply (str) - e.g. lx.symbol.i_POLYTAG_MATERIAL
    """

    if not ptag:
        ptag = None

    for p in polys:
        if i_POLYTAG == lx.symbol.i_POLYTAG_PICK and ptag:
            ptags = ptag.split(";")

            if p.getTag(i_POLYTAG):
                tags = set(p.getTag(i_POLYTAG).split(";"))
            else:
                tags = set()

            tags.update(ptags)
            p.setTag(i_POLYTAG,";".join(tags))

        else:
            p.setTag(i_POLYTAG,ptag)
