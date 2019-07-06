# coding: utf-8
import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from users.admin import User


class UserSerializer(serializers.ModelSerializer):
    '''
        @summary: 用户表的序列化类
        @author: lipeng
    '''

    class Meta:
        model = User
        fields = '__all__'


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    重置密码序列化器
    """
    password2 = serializers.CharField(label='确认密码',  write_only=True)
    token = serializers.CharField(label='token', write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'password2')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许6-20个字符的密码',
                    'max_length': '仅允许6-20个字符的密码',
                }
            }
        }

    def validate(self, attr):
        """
        校验数据
        """
        # 判断两次密码
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 对比 access token中的user_id 与请求用户的id是否一致
        allow = User.check_set_password_token(attr['token'], self.context['view'].kwargs['pk'])
        if not allow:
            raise serializers.ValidationError('无效的token')

        return attr

    def update(self, instance, validated_data):
        """
        更新密码
        """
        # 调用django 用户模型类的设置密码方法
        instance.set_password(validated_data['password'])
        instance.update_pwd_time = datetime.datetime.now()
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    '''
        @summary: 用户详情的序列化类
        @author: liangpanfeng
    '''

    permissions = serializers.SerializerMethodField()
    is_update_pwd = serializers.SerializerMethodField()
    update_pwd_msg = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_permissions(self, obj):
        """
        @summary: 获取用户所有权限
        @author: liangpanfeng
        """
        return obj.get_all_permissions()

    def get_is_update_pwd(self, obj):
        """
        @summary: 判断用户密码是否需要修改
        @author: lilipeng
        """
        update_pwd_time = obj.update_pwd_time
        if update_pwd_time + relativedelta(months=3) < datetime.datetime.now()\
                or obj.check_password('123456'):
            return True

        return False

    def get_update_pwd_msg(self, obj):
        """
        @summary: 判断用户密码是否需要修改的信息
        @author: lipeng
        """
        msg = ''
        update_pwd_time = obj.update_pwd_time
        if update_pwd_time + relativedelta(months=3) < datetime.datetime.now():
            msg = '密码已过期,请修改密码后重新登录'
        if obj.check_password('123456'):
            msg = '密码为初始密码,请修改密码后重新登录'

        return msg

