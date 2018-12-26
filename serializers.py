from rest_framework import serializers

from apps.products.models import Color, CatalogItem


class ColorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'hex')


class CatalogItemDetailSerializer(serializers.ModelSerializer):
    colors = ColorDetailSerializer(many=True, read_only=True)
    material = serializers.SerializerMethodField(read_only=True)
    specified_info = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    def get_price(self, obj):
        if obj.price_colored:
            return obj.price_colored
        return obj.price_white

    def get_specified_info(self, obj):
        additional_info = obj.additional_info
        info = {'title': None, 'images': []}
        if additional_info:
            info.update({
                'title': additional_info.title,
                'images': additional_info.image_list,
            })
        return info

    def get_material(self, obj):
        return obj.material.title

    class Meta:
        model = CatalogItem
        fields = (
            'title', 'price', 'material', 'density', 'packing', 'colors',
            'patterning_technologies', 'specified_info', 'size_list'
        )
