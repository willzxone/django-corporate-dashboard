import graphene
from graphene_django import DjangoObjectType

from .models import Category, Product, ProductImage, CategoryImage, ProductSpecification, ProductSpecificationValue


class CategoryImageType(DjangoObjectType):
    class Meta:
        model = CategoryImage
        field = ("id", "image", "alt_text")

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "category", "level",
                  "slug", "slogan", "category_image")


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        field = ("id", "image", "alt_text")

    def resolve_image(self, info):
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image


class ProductSpecificationType(DjangoObjectType):
    class Meta:
        model = ProductSpecification
        fields = ("id", "product_type", "name")


class ProductSpecificationValueType(DjangoObjectType):
    class Meta:
        model = ProductSpecificationValue
        fields = ("id", "product", "specification", "value")


class ProductType(DjangoObjectType):
    specifications = graphene.List(ProductSpecificationValueType)

    class Meta:
        model = Product
        fields = ("id", "title", "description",
                  "regular_price", "slug", "product_image")

    def resolve_specifications(self, info):
        # Fetch the associated specifications for the product
        return self.productspecificationvalue_set.all()


class Query(graphene.ObjectType):
    all_Categories = graphene.List(CategoryType)
    category_by_name = graphene.Field(
        CategoryType, name=graphene.String(required=True))
    all_Products = graphene.List(ProductType, first=graphene.Int())
    all_Products_by_name = graphene.Field(
        ProductType, slug=graphene.String(required=True))
    all_product_specification_values = graphene.List(
        ProductSpecificationValueType)

    # all_product_specification = graphene.List(ProductSpecificationType)

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

    def resolve_all_Products_by_name(root, info, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None

    def resolve_all_Categories(root, info):
        return Category.objects.all().order_by('id')

    def resolve_all_Products(root, info, first=None, **kwargs):
        qs = Product.objects.all()

        if first:
            qs = qs[:first]

        return qs

    # def resolve_all_product_specification(self, info):
    #     return ProductSpecification.objects.all()

    # def resolve_all_product_specification_values(self, info):
    #     return ProductSpecificationValue.objects.all()
