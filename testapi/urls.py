from django.urls import path
from testapi.api_views.customer_views.hello import HelloApiView
from testapi.api_views.customer_views.signup import (
    SignUpApiView, SignUpVerifyView, ActivateUserView
)
from testapi.api_views.customer_views.signin import(
    SigninView
)
from testapi.api_views.customer_views.signout import(
    SignOutView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from testapi.api_views.customer_views.test_email import TestEmailView
from testapi.api_views.customer_views.test_cookie import TestCookieView

from testapi.api_views.worker_views.worker_email import WorkerEmail


urlpatterns = [
    path(
        'hello',
        HelloApiView.as_view(),
        name='hello'
    ),
    path(
        'sign-up',
        SignUpApiView.as_view(),
        name='sign_up'
    ),
    path(
        'signup-verify',
        SignUpVerifyView.as_view(),
        name='signup_verify'
    ),
    path(
        'activate/<uidb64>/<token>/',
        ActivateUserView.as_view(),
        name='activate'
    ),
    path(
        'sign-in',
        SigninView.as_view(),
        name='signin'
    ),
    path(
        'sign-out',
        SignOutView.as_view(),
        name='signout'
    ),
]

# JWT Tokens handler 
urlpatterns += [
    path(
        'api/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
]

# Testing end points
urlpatterns +=[
    path(
        'test-email',
        TestEmailView.as_view(),
        name='test_email'
    ),
    path(
        'test-cookie',
        TestCookieView.as_view(),
        name='test_cookie'
    ),
]

# worker
urlpatterns +=[
    path(
        'worker-email',
        WorkerEmail.as_view(),
        name='worker_email'
    ),
]