from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

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


# # def users(request):
# @user_passes_test(lambda u: u.is_superuser)
# def user_read(request):
#     title = 'админка/пользователи'
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)

# модель Class Based Views(CBV)
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при
        # @method_decorator(user_passes_test(lambda u: u.is_superuser))
        return super().dispatch(*args, **kwargs)


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


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all().order_by('-is_active')
#
#     content = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', content)

# модель Class Based Views(CBV) категории
# class CategoriesListView(ListView):
class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    # template_name = 'adminapp/category_update.html'
    # success_url = reverse_lazy('adminapp:product_read')
    # object_list = ProductCategory.objects.all().order_by('-is_active')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при
        # @method_decorator(user_passes_test(lambda u: u.is_superuser))
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категория/создание'
#     # GET - просто отобразить, а POST - обработать форму
#     if request.method == 'POST':
#         user_form = ProductCategoryEditForm(request.POST, request.FILES)
#         # user_form = ProductCategory(request.POST, request.FILES)
#         # user_form = ShopUserAdminEditForm(request.POST, request.FILES)
#
#         if user_form.is_valid():
#             user_form.save()
#             # reverse - генерируем адрес видимый в строке
#             # return HttpResponseRedirect(reverse('admin:users'))
#             return HttpResponseRedirect(reverse('adminapp:category_read'))
#     else:
#         user_form = ProductCategoryEditForm()
#         # user_form = ProductCategory()
#         # user_form = ShopUserAdminEditForm()
#
#     content = {
#         'title': title, 'update_form': user_form
#         # 'form': user_form
#     }
#
#     return render(request, 'adminapp/category_create.html', content)

# модель Class Based Views(CBV) для создания категории
class ProductCategoryCreateView(CreateView):
    model = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    # success_url = '/admin/categories/' - можно прописать так
    # reverse_lazy - отдаёт инфо по вызову, как yield
    # success_url = reverse_lazy('adminapp:category_create')
    success_url = reverse_lazy('adminapp:product_read')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    # dispatch
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при @method_decorator(user_passes_test(lambda u: u.is_superuser))
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категория/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, instance=edit_category)
#         # user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             # if user_form.is_valid():
#             edit_form.save()
#             # user_form.save()
#             # return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#             # редиректим на список польлователей
#             # return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
#             # return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_category.pk]))
#             return HttpResponseRedirect(reverse('adminapp:category_read'))
#     else:
#         # генерируем такую же форму, но без переданных данных о странице
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#         # user_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'title': title,
#         'update_form': edit_form
#         # 'form': user_form
#     }
#
#     return render(request, 'adminapp/category_update.html', content)

# модель Class Based Views(CBV) для редактирования категории
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    # success_url = '/admin/categories/' - можно прописать так
    # reverse_lazy - отдаёт инфо по вызову, как yield
    success_url = reverse_lazy('adminapp:category_read')
    # success_url = reverse_lazy('adminapp:product_read')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    # def get_queryset(self):
    #     return get_object_or_404(self.model, pk=self.kwargs['pk'])
    #
    # def get_context_data(self, **kwargs):
    #     self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'

        return context
    #
    # def get_success_url(self):
    #     self.object = self.get_object()
    #     if self.object.is_active:
    #         return self.success_url
    #     return reverse_lazy('adminapp:product_read')

    # def form_valid(self, form):

    # dispatch
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при
        # @method_decorator(user_passes_test(lambda u: u.is_superuser))
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         if category.is_active:
#             category.is_active = False
#         else:
#             category.is_active = True
#         category.save()
#         return HttpResponseRedirect(reverse('adminapp:category_read'))
#
#     content = {
#         'title': title,
#         'category_to_delete': category
#     }
#
#     return render(request, 'adminapp/category_delete.html', content)

# модель Class Based Views(CBV) для удаления категории
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:category_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # if self.object(request.POST):
        # if self.object.is_active:
        #     self.object.is_active = False
        # else:
        #     self.object.is_active = True
        # self.object.save()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при @method_decorator(user_passes_test(...))
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#     # Если админ перешёл в несуществующую категорию выйдет ошибка 404
#     category = get_object_or_404(ProductCategory, pk=pk)
#     # category_item = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#     # products_list = Product.objects.filter(category=category_item).order_by('-is_active')
#
#     content = {
#         'title': title,
#         'category': category,
#         # 'category': category_item,
#         'objects': products_list
#     }
#
#     return render(request, 'adminapp/products.html', content)

class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Product.objects.filter(category__pk=category_pk).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукт/создание'
#     # проверка не ошибку
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#     else:
#         # product_form = ProductEditForm(initial={'category': category_item})
#         product_form = ProductEditForm()
#     content = {
#         # 'form': product_form,
#         'title': title,
#         'update_form': product_form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/product_update.html', content)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при @method_decorator(user_passes_test(...))
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs['pk']])

# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'продукт/редактирование'
#     edit_product = get_object_or_404(Product, pk=pk)
#     # т.к. у продукта есть картинка, то нужен request.FILES
#     if request.method == 'POST':
#         # когда передаём "instance=edit_product", то форма доступна для редактирования, если нет, для создания
#         product_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#         if product_form.is_valid():
#             product_form.save()
#             # return HttpResponseRedirect(reverse('adminapp:products', args=[edit_product.category_id]))
#             return HttpResponseRedirect(reverse('adminapp:products', args=[edit_product.pk]))
#     else:
#         product_form = ProductEditForm(instance=edit_product)
#
#     content = {
#         'title': title,
#         'category': edit_product.category,
#         'update_form': product_form
#     }
#
#     return render(request, 'adminapp/product_update.html', content)

# product_update
class ProductUpdateView(UpdateView):
    ''' Модель Class Based Views(CBV) для редактирования продукта'''
    model = Product
    template_name = 'adminapp/product_update.html'
    # success_url = '/admin/categories/' - можно прописать так
    # reverse_lazy - отдаёт инфо по вызову, как yield
    # success_url = reverse_lazy('adminapp:category_create')
    # success_url = reverse_lazy('adminapp:product_read')
    # fields = '__all__'
    form_class = ProductEditForm

    # dispatch
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        '''Метод dispatch отвечает за контроль авторизации, но только при
        @method_decorator(user_passes_test(lambda u: u.is_superuser))'''
        return super().dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     return get_object_or_404(self.model, pk=self.kwargs['pk'])
    #
    # def get_context_data(self, **kwargs):
    #     self.get_queryset()

    def get_context_data(self, **kwargs):
        '''Обработка контекста '''
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        category = get_object_or_404(ProductCategory, pk=self.object.category.pk)
        # context['category'] = self.get_object().category.pk
        context['category'] = category

        return context

    def get_success_url(self):
        '''Возвращает на страницу продуктов'''
        self.object = self.get_object()
        # pk = self.get_object().category.pk
        # if self.object.is_active:
        #     return self.success_url
        # return reverse_lazy('adminapp:product_read', args=[self.object.pk])
        return reverse_lazy('adminapp:products', args=[self.object.category.pk])
        # return reverse_lazy('adminapp:products', args=[self.kwargs['pk']])
        # return reverse_lazy('adminapp:product_read')
        # return reverse_lazy('adminapp:products')

        # def form_valid(self, form):


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {
#         'title': title,
#         'object': product
#     }
#     return render(request, 'adminapp/product_read.html', content)

# модель Class Based Views(CBV) для деталей продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при @method_decorator(user_passes_test(...))
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#     product_item = get_object_or_404(Product, pk=pk)
#     # если 'POST' в контроллере удаления, то означает, что мы подтвердили удаление, если 'GET', то отправл.
#     # на стр. подтверждения
#     if request.method == 'POST':
#         product_item.is_active = False
#         product_item.save()
#         # return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.pk]))
#         return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#
#     content = {
#         'title': title,
#         'product_to_delete': product_item
#     }
#     return render(request, 'adminapp/product_delete.html', content)

class ProductDeleteView(DeleteView):
    ''' Модель Class Based Views(CBV) для удаления товара'''
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('adminapp:category_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # if self.object(request.POST):
        # if self.request.method == 'POST':
        # if self.object.method == 'POST':-
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        # self.object.is_active = False
        # self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        '''Возвращает на страницу продуктов'''
        self.object = self.get_object()
        # pk = self.get_object().category.pk
        # if self.object.is_active:
        #     return self.success_url
        # return reverse_lazy('adminapp:product_read', args=[self.object.pk])
        return reverse('adminapp:products', args=[self.object.category.pk])
        # return reverse_lazy('adminapp:product_read')
        # return reverse_lazy('adminapp:products')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        # метод dispatch отвечает за контроль авторизации, но только при @method_decorator(user_passes_test(...))
        return super().dispatch(*args, **kwargs)
