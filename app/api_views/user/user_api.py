from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from app.authentication import JwtAuthentication
from app.exceptions import ClientException
from app.models import Cart, Order, Payment
from app.models.rating import Rating
from app.models.user import User
from app.permissions import UserPermission, LoggedPermission, OwnerCartPermission, OwnerOrderPermission
from app.serializers import UserSerializer, UserInfoSerializer, UserRateProductSerializer, RatingResponseSerializer, \
    UserCartSerializer, UserCartAddSerializer, UserOrderSerializer, UserOrderCreateSerializer, OrderItemSerializer, \
    OrderItemCreateSerializer, PaymentSerializer, ProductRatingsSerializer, UserOrderCancelSerializer
from app.utils import email_util
from app.utils.constants import SHIPPING_FEE


class UserInfoAPI(generics.GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    # def get_serializer_class(self):
    #     if self.request.method == 'PUT':
    #         return UserInfoSerializer
    #     return UserSerializer

    def get(self, request, *arg, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request, *arg, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRateProductAPI(generics.GenericAPIView):
    queryset = Rating.objects
    # serializer_class = UserRateProductSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductRatingsSerializer
        if self.request.method == 'POST':
            return UserRateProductSerializer

    def get(self, request, *arg, **kwargs):
        product_id = self.request.query_params.get('product')
        c_user = self.request.user
        ratings = self.get_queryset().filter(user=c_user.id)
        if product_id is not None:
            ratings = ratings.filter(product=product_id)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        user_id = request.user.id
        product_id = request.data.get('product')
        data['is_solved'] = False
        try:
            rating = Rating.objects.get(user=user_id, product_id=product_id)
            serializer = self.get_serializer(rating, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResponseRatingAPI(generics.GenericAPIView):
    queryset = Rating
    serializer_class = RatingResponseSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (LoggedPermission,)

    def post(self, request, pk, *arg, **kwargs):
        c_rating = self.get_object()
        data = request.data.copy()
        data['rating'] = c_rating.id
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCartListAPI(generics.GenericAPIView):
    queryset = Cart.objects
    serializer_class = UserCartSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def get(self, request, *arg, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        if request.query_params.get('detail') is not None:
            sum_price = sum([e.product.sale_price * e.count for e in queryset])
            data = {
                'sum_price': sum_price,
                'shipping_fee': SHIPPING_FEE,
                'total_cost': sum_price + SHIPPING_FEE,
                'items': serializer.data,
                'payments': PaymentSerializer(Payment.objects.all(), many=True).data,
            }
            return Response(data)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        list_cart_id = request.data
        if type(list_cart_id) != list:
            raise ClientException('Data must be a list of cart id.')
        list_cart = self.get_queryset().filter(id__in=list_cart_id)
        if len(list_cart_id) != len(list_cart):
            raise ClientException('Invalid id list, there is a cart id not exist.')
        list_cart.delete()
        return Response(f'Deleted {list_cart_id} in cart.')


class UserCartSingleAPI(generics.GenericAPIView):
    queryset = Cart.objects
    serializer_class = UserCartSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission, OwnerCartPermission)

    def get(self, request, pk, *arg, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        c_cart = self.get_object()
        c_cart.delete()
        return Response(f'Cart deleted.')


class UserCartAddItemAPI(generics.GenericAPIView):
    queryset = Cart.objects
    serializer_class = UserCartAddSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def post(self, request, *arg, **kwargs):
        product_id = request.data.get('product')
        user_id = request.user.id
        try:
            c_cart = Cart.objects.get(product=product_id, user=user_id)
            data = {
                'product': product_id,
                'user': user_id,
                'count': c_cart.count + 1
            }
            serializer = self.get_serializer(c_cart, data=data)
            if not serializer.is_valid():
                return Response(serializer.errors)
            serializer.save()
        except Cart.DoesNotExist:
            data = {
                'product': product_id,
                'user': user_id,
                'count': 1
            }
            serializer = self.get_serializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors)
            serializer.save()
        # queryset = self.get_queryset().filter(user=request.user)
        # serializer = UserCartSerializer(queryset, many=True)
        return Response(serializer.data)


class UserCartAddItemAPI(generics.GenericAPIView):
    queryset = Cart.objects
    serializer_class = UserCartAddSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def put(self, request, *arg, **kwargs):
        product_id = request.data.get('product')
        count = int(request.data.get('count', 1))
        user_id = request.user.id
        try:
            c_cart = Cart.objects.get(product=product_id, user=user_id)
            data = {
                'product': product_id,
                'user': user_id,
                'count': c_cart.count + count
            }
            serializer = self.get_serializer(c_cart, data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        except Cart.DoesNotExist:
            data = {
                'product': product_id,
                'user': user_id,
                'count': count
            }
            serializer = self.get_serializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        # queryset = self.get_queryset().filter(user=request.user)
        # serializer = UserCartSerializer(queryset, many=True)
        return Response(serializer.data)


class UserCartRemoveItemAPI(generics.GenericAPIView):
    queryset = Cart.objects
    serializer_class = UserCartAddSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def put(self, request, *arg, **kwargs):
        product_id = request.data.get('product')
        count = int(request.data.get('count', 1))
        user_id = request.user.id
        try:
            c_cart = Cart.objects.get(product=product_id, user=user_id)
            data = {
                'product': product_id,
                'user': user_id,
                'count': c_cart.count - count
            }
            serializer = self.get_serializer(c_cart, data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            print(c_cart.count)
            if c_cart.count <= 0:
                c_cart.delete()
        except Cart.DoesNotExist:
            raise ClientException('Product does not exist in user cart.')
        # queryset = self.get_queryset().filter(user=request.user)
        # serializer = UserCartSerializer(queryset, many=True)
        return Response(serializer.data)


class UserOrderListAPI(generics.GenericAPIView):
    queryset = Order.objects
    # serializer_class = UserOrderSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOrderSerializer
        if self.request.method == 'POST':
            return UserOrderCreateSerializer

    def get(self, request, *arg, **kwargs):
        queryset = self.get_queryset().filter(user=request.user).order_by('-created_at')
        status = request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *arg, **kwargs):
        # data = {
        #     'user': request.user.id,
        #     'payment': request.data.get('payment'),
        #     'name': request.data.get('name'),
        #     'address': request.data.get('address'),
        #     'phone_number': request.data.get('phone_number')
        # }
        data = request.data.copy()
        data['user'] = request.user.id
        # list_data = []
        # for e in data['items']:
        #     new_data = data.copy()
        #     new_data['items'] = [e]
        #     list_data.append(new_data)
        # print(list_data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        c_order = serializer.save()
        serializer = UserOrderSerializer(c_order)
        email_data = serializer.data.copy()
        email_data['email'] = request.user.email
        email_util.send_order_email(email_data)
        return Response(serializer.data)

    # def post(self, request, *arg, **kwargs):
    #     cart_list = Cart.objects.filter(user=request.user)
    #     if len(cart_list) == 0:
    #         raise ClientException("User's cart is empty.")
    #     data = {
    #         'user': request.user.id,
    #         'payment': request.data.get('payment'),
    #         'name': request.data.get('name'),
    #         'address': request.data.get('address'),
    #         'phone_number': request.data.get('phone_number')
    #     }
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     c_order = serializer.save()
    #     o_list_serializer = []
    #     for e in cart_list:
    #         o_data = {
    #             'product': e.product.id,
    #             'count': e.count,
    #             'order': c_order.id,
    #             'order_price': e.product.sale_price
    #         }
    #         o_serializer = OrderItemCreateSerializer(data=o_data)
    #         o_serializer.is_valid(raise_exception=True)
    #         o_list_serializer.append(o_serializer)
    #     for e in o_list_serializer:
    #         e.save()
    #     sum_price = sum([e.product.sale_price * e.count for e in cart_list])
    #     # data = {
    #     #     'sum_price': sum_price,
    #     #     'shipping_fee': SHIPPING_FEE,
    #     #     'total_cost': sum_price + SHIPPING_FEE
    #     # }
    #     c_order.sum_price = sum_price
    #     c_order.shipping_fee = SHIPPING_FEE
    #     c_order.total_cost = sum_price + SHIPPING_FEE
    #     c_order.save()
    #     for e in cart_list:
    #         e.delete()
    #     serializer = UserOrderSerializer(c_order)
    #     return Response(serializer.data)


class UserOrderSingleAPI(generics.GenericAPIView):
    queryset = Order.objects
    # serializer_class = UserOrderSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission, OwnerOrderPermission)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOrderSerializer
        if self.request.method == 'POST':
            return UserOrderCreateSerializer

    def get(self, request, pk, *arg, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class UserOrderCancelAPI(generics.GenericAPIView):
    queryset = Order.objects
    serializer_class = UserOrderCancelSerializer
    authentication_classes = (JwtAuthentication,)
    permission_classes = (UserPermission, OwnerOrderPermission)

    def put(self, request, pk, *arg, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = UserOrderSerializer(queryset)
        return Response(serializer.data)
