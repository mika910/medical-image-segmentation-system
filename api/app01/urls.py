from django.urls import path
from app01.Views import user  # 添加这行导入语句

urlpatterns = [
    # ... 现有URL配置 ...
    path('user/verify-identity', user.VerifyIdentity.as_view()),
    path('user/reset-password', user.ResetPassword.as_view()),
    # ... 其他URL配置 ...
]