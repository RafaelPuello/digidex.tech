from wagtail import blocks


class EntityBlock(blocks.StructBlock):
    entity = blocks.PageChooserBlock(
        required=True,
        page_type=['inventory.Entity'],
    )

    class Meta:
        icon = 'doc-empty'
        label = "Inventory Entity"
        template = 'inventory/blocks/entity_block.html'
