from rest_framework import serializers

from store.models import Category, Product, ProductCart, SubCategory, User


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = 'name', 'slug', 'image'


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = 'name', 'slug', 'image', 'sub_categories'


class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        source='sub_category.category',
    )

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'category',
            'sub_category',
            'price',
            'image',
            'middle_thumbnail',
            'small_thumbnail',
        )


class ProductCartSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    price = serializers.DecimalField(
        source='product.price',
        read_only=True,
        decimal_places=2,
        max_digits=9,
    )
    amount = serializers.IntegerField(
        required=True,
        min_value=1,
    )

    class Meta:
        model = ProductCart
        fields = 'id', 'product', 'amount', 'price'


class CartSerializer(serializers.ModelSerializer):
    products = ProductCartSerializer(source='m2m_product', many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = 'products', 'total'

    def get_total(self, obj):
        return sum(position.get_cost() for position in obj.m2m_product.all())
