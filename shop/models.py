from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.models import Page, Orderable, ClusterableModel
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.snippets.models import register_snippet


class ShopIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        productpages = self.get_children().live()
        context['productpages'] = productpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class ProductPage(Page):
    sku = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    categories = ParentalManyToManyField('shop.ShopCategory', blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        MultiFieldPanel([
            FieldPanel(
                'categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('sku'),
            FieldPanel('price'),
            FieldPanel('short_description'),], heading="Product Information"),
        InlinePanel('custom_fields', label='Custom Fields')
    ]


class ProductCustomField(Orderable):
    product = ParentalKey(
        ProductPage, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]


@register_snippet
class ShopCategory(models.Model):
    name = models.CharField(max_length=250)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'shop categories'


# class CartItem(Orderable):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField()

#     panels = [
#         FieldPanel('name'),
#         FieldPanel('price'),
#         FieldPanel('quantity'),
#     ]


# @register_snippet
# class Cart(ClusterableModel):
#     cart_item = models.ManyToManyField(CartItem, related_name='Cart Items')

#     def add_to_cart(self, product, quantity=1):
#         cart_item, created = CartItem.objects.get_or_create(
#             cart=self, product=product)
#         cart_item.quantity += quantity
#         cart_item.save()

#     def calculate_subtotal(self):
#         subtotal = 0
#         for item in self.items.all():
#             subtotal += item.price * item.quantity
#         self.subtotal = subtotal

#     def calculate_total(self):
#         self.total = self.subtotal
