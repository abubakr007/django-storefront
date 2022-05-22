from django.shortcuts import get_object_or_404
from django.db.models import  Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,DestroyModelMixin, UpdateModelMixin
from .pagination import DefaultPagaingation
from .filters import ProductFilter
from .models import CartItem, Collection, Customer, OrderItem, Product, Review, Cart
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CustomerSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer

# Create your views here.

class ReviewViewSet(ModelViewSet):
    
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
class CartViewSet(CreateModelMixin, GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer  
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagaingation
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = collection_id=self.request.query_params.get('collection_id')
    #     if  collection_id is not None:
    #         queryset =  queryset.filter(collection_id=collection_id)
    #     return queryset


    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':'product cannot be deleted because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)    
   

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() >0 :
            return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer




    # def delete(self,request,pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')).all(),pk=pk)
    #     if collection.product.count() > 0:
    #         return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer

    
   
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         products_count=Count('product'))
#     serializer_class = CollectionSerializer
#     def delete(self,request,pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')).all(),pk=pk)
#         if collection.product.count() > 0:
#             return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    #def get(self,request):
    #    queryset = Product.objects.select_related('collection').all()
    #    serializer = ProductSerializer(queryset,many=True,context={'request': request})
    #    return Response(serializer.data)
    #def post(self,request):
    #    serializer = ProductSerializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data,status=status.HTTP_201_CREATED)



        
# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset,many=True,context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)



  



# @api_view()    
# def collection_detail(request,pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')).all(),pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.product.count() > 0:
#             return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

    

#     def get_serializer_context(self):
#         return {'request': self.request}
    
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
   