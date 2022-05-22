from decimal import Decimal
from rest_framework import serializers

from store.models import Cart, CartItem, Collection, Customer, Product , Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)




class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    
    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
    #id = serializers.IntegerField()
    #title = serializers.CharField(max_length=255)
    #price = serializers.DecimalField(max_digits=6,decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection = serializers.HyperlinkedRelatedField(
    #    queryset = Collection.objects.all(),
    #    view_name='collection-detail'
    #)
    

    def calculate_tax(self, product : Product):
        return product.unit_price * Decimal(1.1)

    #def create(self, validated_data):
    #    product = Product(**validated_data)
    #    product.save()
    #    return product

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cartitem = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance =  cartitem
        except CartItem.DoesNotExist :
            self.instance =  cartitem.create(cart_id=cart_id,**self.validated_data)
        
        return self.instance


    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True,many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum ([item.quantity * item.product.unit_price for item in cart.items.all()])
        

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','birth_date','membership']