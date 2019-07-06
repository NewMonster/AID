import traceback

from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from settings import logger
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    用户 viewset
    """
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('ch_name',)
    filter_fields = ('gender', 'ch_name')
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == 'logout':
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ['iam', 'retrieve']:
            return UserDetailSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        users = User.objects.all()

        # 用户不是超级用户
        if not self.request.user.is_superuser:
            users = users.filter(org=self.request.user.org)
        return users.order_by('username')

    @action(methods=['get'], detail=False)
    def iam(self, request, pk=None):
        data = self.get_serializer(request.user).data
        return Response(data)

    @action(methods=['post'], detail=False)
    def change_password(self, pk=None):
        """
        修改密码
        @author: liangpanfeng
        """
        data = {}
        try:
            old_password = self.request.data.get('old_password')
            new_password = self.request.data.get('new_password')
            user = self.request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                data['result'] = 'info'
                data['msg'] = '已修改'
            else:
                data['result'] = 'error'
                data['msg'] = '密码错误，请重新输入'
        except:
            data['result'] = 'error'
            data['msg'] = '修改失败，请联系管理员'
            logger.error(traceback.format_exc())
        return Response(data)

    @action(methods=['post'], detail=False)
    def logout(self, request, pk=None):
        data = {}
        data['result'] = 'info'
        data['msg'] = '已注销'
        res = Response(data=data)
        res.delete_cookie('token')
        return res