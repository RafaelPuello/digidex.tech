from base import blocks


class NfcTagBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.TextBlock()

    class Meta:
        icon = 'tag'
        template = 'nearfieldcommunication/blocks/nfc_tag_block.html'
