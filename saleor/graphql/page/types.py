from textwrap import dedent

import graphene
from graphene import relay

from ...page import models
from ..core.connection import CountableDjangoObjectType
from ..translations.resolvers import resolve_translation
from ..translations.types import PageTranslation


class Page(CountableDjangoObjectType):
    available_on = graphene.Date(
        deprecation_reason=(
            'availableOn is deprecated, use publicationDate instead'))
    is_visible = graphene.Boolean(
        deprecation_reason=(
            'isVisible is deprecated, use isPublished instead'))
    translation = graphene.Field(
        PageTranslation, language_code=graphene.String(required=True),
        description='Translation.', resolver=resolve_translation)

    class Meta:
        description = dedent("""A static page that can be manually added by a shop
        operator through the dashboard.""")
        exclude_fields = ['voucher_set', 'sale_set', 'menuitem_set']
        interfaces = [relay.Node]
        model = models.Page

    def resolve_available_on(self, info):
        return self.publication_date

    def resolve_is_visible(self, info):
        return self.is_published
