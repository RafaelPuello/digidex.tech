from base import blocks

from biodiversity.blocks import PlantBlock
from nearfieldcommunication.blocks import NfcTagBlock

class InventoryPlantBlock(blocks.StructBlock):
    plant = PlantBlock()
    nfc_tag = NfcTagBlock()

    class Meta:
        icon = 'tablet-alt'
        template = 'inventory/blocks/inventory_block.html'
