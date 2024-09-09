from base import blocks

class PlantBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    description = blocks.TextBlock()

    class Meta:
        icon = 'plant'
        template = 'biodiversity/blocks/plant_block.html'
