from django.conf import settings
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import ChangePassword, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),

    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('buynow/<int:product_id>/', views.buynow, name='buynow'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),

    path('orders/', views.orders, name='orders'),

    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='changepassword.html', form_class=ChangePassword, success_url="/passwordchangedone/"), name='changepassword'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('changepassword/passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('mobile/login/', views.loginUser, name="login"),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('laptop/login/', views.loginUser, name="login"),

    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('topwear/login/', views.loginUser, name="login"),

    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('bottomwear/login/', views.loginUser, name="login"),

    path('top-offers/', views.top_offers, name="top_offers"),

    path('top-offers/login/', views.loginUser, name="login"),
    path('top-offers/signup/', views.signup, name='signup'),
    path('top-offers/bottomwear/', views.bottomwear, name='bottomwear'),


    path('bottomwear/', views.bottomwear, name='bottomwear'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name= 'password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('Password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('Password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'password_reset_complete.html'), name='password_reset_complete'),

    path('signup/', views.signup, name='signup'),

    path('Password-reset-complete/login/', views.loginUser, name="login"),
    path('accounts/login/',views.loginUser,  name="login"),
    path('signup/login/', views.loginUser, name="login"),
    path('login/', views.loginUser, name="login"),

    path('about/', views.about, name="about"),

    path('contact', views.contact, name="contact"),

    path('search/', views.search, name="search"),

    path('update/<int:pk>', views.Update.as_view(), name='update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
