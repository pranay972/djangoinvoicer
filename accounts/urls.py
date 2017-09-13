from django.conf.urls import url
from . import views

urlpatterns = [
	#view
	url(r'^$', views.index, name='index'),
	url(r'^login/?$', views.login_view, name='login'),
	url(r'^logout/?$', views.logout_view, name='logout'),
	url(r'^products/?$', views.products_view, name='products'),
	url(r'^gen_bill/?$', views.gen_bill_view, name='gen_bills'),
	url(r'^view_bill/(?P<id>[0-9]+)/?$', views.view_bill_view, name='view_bills'),
	url(r'^all_bill/?$', views.all_bill_view, name='all_bills'),

	#popup_views
	url(r'^edit_product/(?P<id>[0-9]+)/?$', views.edit_product_view, name='edit_product'),	
	url(r'^edit_group/(?P<id>[0-9]+)/?$', views.edit_group_view, name='edit_group'),	

	#helpers
	url(r'^add_product/?$', views.add_product_helper, name='add_products'),
	url(r'^del_product/(?P<id>[0-9]+)/?$', views.del_product_helper, name='del_products'),
	url(r'^add_group/?$', views.add_group_helper, name='add_group'),
	url(r'^del_group/(?P<id>[0-9]+)/?$', views.del_group_helper, name='del_groups'),

	#apis
	url(r'^search_product/(?P<query>[a-zA-Z0-9\-]+)/?$', views.search_product, name='search_product'),	
	url(r'^gen_bill_post/?$', views.gen_bill, name='gen_bill'),
]