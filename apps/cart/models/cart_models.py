from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models.products import Products
import uuid

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):

    def valores(self, request):
        pd = dict()
        pd['qtd'] = request.POST['quantity']
        pd['value'] = request.POST['value']
        pd['produto_id'] = list(request.POST['quantity'])
        pd['name'] = request.POST['name']

        print('pd', pd)
        return pd

    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)

        if qs.count() == 1:
            #print('SRSRS',qs)
            new_obj = False
            cart_obj = qs.first()
            
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
                
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    
    def get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        return qs

    def new(self, user = None):
        user_obj = None
        if not user is None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    produto = models.ManyToManyField(Products, blank=True)
    valor_produto = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text='Valor original do produto')
    desconto = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, help_text='Desconto do produto')
    subtotal = models.DecimalField(default = 0.00, max_digits=100, decimal_places = 2, help_text='Valor com desconto')
    quantity = models.IntegerField(default=1)
    valor_total = models.DecimalField(default = 0.00, max_digits=100, decimal_places = 2,  null=False, blank=False, help_text='Valor total a ser pago')
    atualizado_em = models.DateTimeField(auto_now=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    objects = CartManager()

    def __str__(self) -> str:
        return f'{self.id}'

    def get_total_preco(self, value, quantity):
        self.valor_total = value * quantity
        return self.valor_total

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        ordering = ('-atualizado_em',)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    #print(action)
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        #print('instance',dir(instance))
        #print(instance.total)
        produtos = instance.produto.all()
        total = 0
        desconto = 0
        taxas = 0
        for produto in produtos:
            total += produto.value
            desconto += produto.value / 100

        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
            
        #instance.valor_produto = total
        instance.desconto = desconto * total
        instance.subtotal = total - instance.desconto
        instance.taxa_envio_outros = taxas
        #instance.valor_total += instance.valor_produto
        instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender = Cart.produto.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.valor_produto > 0:
        # considere o 10 como uma taxa de entrega
        print(instance.valor_total)
        instance.valor_total += instance.valor_produto
    else:
        instance.valor_total = instance.valor_total
        
pre_save.connect(pre_save_cart_receiver, sender = Cart)