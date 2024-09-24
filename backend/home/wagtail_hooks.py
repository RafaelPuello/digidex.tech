from wagtail import hooks
from wagtail.admin.wagtail_hooks import (
    CollectionsMenuItem,
    LockedPagesMenuItem,
)
from wagtail.admin.site_summary import PagesSummaryItem
from wagtail.snippets.wagtail_hooks import SnippetsMenuItem
from wagtail.images.wagtail_hooks import ImagesMenuItem, ImagesSummaryItem
from wagtail.documents.wagtail_hooks import DocumentsMenuItem, DocumentsSummaryItem
from wagtail.admin.wagtail_hooks import (
    WorkflowReportMenuItem,
    SiteHistoryReportMenuItem,
    AgingPagesReportMenuItem,
    PageTypesReportMenuItem,
)


@hooks.register('construct_explorer_page_queryset')
def show_relevant_pages_only(parent_page, pages, request):
    """
    Show only relevant pages to non-superusers.
    """
    if not request.user.is_superuser:
        pages = pages.filter(owner=request.user)
    return pages


@hooks.register('construct_main_menu')
def construct_main_menu_items(request, menu_items):
    """
    Hide menu items for non-superusers.
    """
    HIDDEN_MAIN_MENU_ITEMS = (
        CollectionsMenuItem,
        SnippetsMenuItem,
        ImagesMenuItem,
        DocumentsMenuItem
    )

    if not request.user.is_superuser:
        modified_menu_items = []
        for item in menu_items:
            if isinstance(item, HIDDEN_MAIN_MENU_ITEMS):
                continue
            modified_menu_items.append(item)
        menu_items[:] = modified_menu_items


@hooks.register('construct_reports_menu')
def hide_report_menu_items(request, menu_items):
    """
    Hide report menu items for non-superusers.
    """
    if not request.user.is_superuser:
        menu_items[:] = [
            item for item in menu_items
            if not isinstance(item, (
                SiteHistoryReportMenuItem,
                AgingPagesReportMenuItem,
                PageTypesReportMenuItem,
                WorkflowReportMenuItem,
                LockedPagesMenuItem,
            ))
        ]


@hooks.register("construct_homepage_summary_items", order=1)
def hide_summary_items(request, summary_items):
    """
    Hide summary items for non-superusers.
    """
    if not request.user.is_superuser:
        summary_items[:] = [
            item for item in summary_items
            if not isinstance(item, (
                PagesSummaryItem,
                ImagesSummaryItem,
                DocumentsSummaryItem,
            ))
        ]
