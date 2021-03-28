from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'
    # GET - просто отобразить, а POST - обработать форму
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        # user_form = ShopUserAdminEditForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            # reverse - генерируем адрес видимый в строке
            # return HttpResponseRedirect(reverse('admin:users'))
            return HttpResponseRedirect(reverse('adminapp:user_reads'))
    else:
        user_form = ShopUserRegisterForm()
        # user_form = ShopUserAdminEditForm()

    content = {
        'title': title,
        'update_form': user_form
        # 'form': user_form
    }

    return render(request, 'adminapp/user_update.html', content)


# def users(request):
@user_passes_test(lambda u: u.is_superuser)
def user_read(request):
    title = 'админка/пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    content = {
        'title': title,
        'objects': users_list
    }
    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        # user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
        # if user_form.is_valid():
            edit_form.save()
            # user_form.save()
            # return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
            # редиректим на список польлователей
            # return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
            return HttpResponseRedirect(reverse('adminapp:user_read'))
    else:
        # генерируем такую же форму, но без переданных данных о странице
        edit_form = ShopUserAdminEditForm(instance=edit_user)
        # user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form
        # 'form': user_form
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'
    # фильтрация pk=pk
    # user = get_object_or_404(ShopUser, pk=pk)
    user_item = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # блок проверки удаления и восстановления пользователя
        if user_item.is_active:
            # вместо удаления лучше сделаем неактивным
            user_item.is_active = False
        else:
            user_item.is_active = True
        # user.delete()
        user_item.save()
        return HttpResponseRedirect(reverse('adminapp:user_read'))

    content = {
        'title': title,
        # шаблонная переменная
        'user_to_delete': user_item
    }

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all().order_by('-is_active')

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категория/создание'
    # GET - просто отобразить, а POST - обработать форму
    if request.method == 'POST':
        user_form = ProductCategoryEditForm(request.POST, request.FILES)
        # user_form = ProductCategory(request.POST, request.FILES)
        # user_form = ShopUserAdminEditForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            # reverse - генерируем адрес видимый в строке
            # return HttpResponseRedirect(reverse('admin:users'))
            return HttpResponseRedirect(reverse('adminapp:category_read'))
    else:
        user_form = ProductCategoryEditForm()
        # user_form = ProductCategory()
        # user_form = ShopUserAdminEditForm()

    content = {
        'title': title,
        'update_form': user_form
        # 'form': user_form
    }

    return render(request, 'adminapp/category_create.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категория/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, instance=edit_category)
        # user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            # if user_form.is_valid():
            edit_form.save()
            # user_form.save()
            # return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
            # редиректим на список польлователей
            # return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
            return HttpResponseRedirect(reverse('adminapp:category_read'))
    else:
        # генерируем такую же форму, но без переданных данных о странице
        edit_form = ProductCategoryEditForm(instance=edit_category)
        # user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form
        # 'form': user_form
    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории/удаление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        if category.is_active:
            category.is_active = False
        else:
            category.is_active = True
            category.save()
        return HttpResponseRedirect(reverse('adminapp:category_read'))

    content = {
        'title': title,
        'category_to_delete': category
    }

    return render(request, 'adminapp/category_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'
    # Если админ перешёл в несуществующую категорию выйдет ошибка 404
    category = get_object_or_404(ProductCategory, pk=pk)
    # category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    # products_list = Product.objects.filter(category=category_item).order_by('-is_active')

    content = {
        'title': title,
        'category': category,
        # 'category': category_item,
        'objects': products_list
    }

    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/категории'
    users_list = Product.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'name')
    content = {
        'title': title,
        'objects': users_list
    }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    # т.к. у продукта есть картинка, то нужен request.FILES
    if request.method == 'POST':
        update_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[edit_product.category_id]))
    else:
        update_form = ProductEditForm(instance=edit_product)

    content = {
        'title': title,
        'category': edit_product.category,
        'update_form': update_form
    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    pass
