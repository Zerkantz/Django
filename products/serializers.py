from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if hasattr(value, 'name'):
            return value.name
        try:
            return Category.objects.get(pk=value.pk if hasattr(value, 'pk') else value).name
        except Category.DoesNotExist:
            return str(value)

    def to_internal_value(self, data):
        if isinstance(data, str) and not data.isdigit():
            try:
                return Category.objects.get(name=data)
            except Category.DoesNotExist:
                raise serializers.ValidationError(f"Categoría '{data}' no encontrada.")
        return super().to_internal_value(data)


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category')
