# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Proveedor(models.Model):
    _name = 'oriflame.proveedor'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre Proveedor")
    rut = fields.Char(string="Rut")
    celular = fields.Char(string="Celular")
    correo = fields.Char(string="Correo")
    direccion = fields.Text(string="Direccion")

    detallepedido_ids = fields.One2many('oriflame.detallepedido', 'proveedor_id')

class Producto(models.Model):
    _name = 'oriflame.producto'
    _rec_name = 'nombrep'

    nombrep = fields.Char(string="Nombre Producto")
    codigo = fields.Char(string="Código Producto")
    punto = fields.Integer(string="Puntos Producto")
    preciop = fields.Integer(string="Precio")
    tipo_id = fields.Many2one('oriflame.tipo')
    stock = fields.Integer(compute ="_cal_cantidad", string= "Stock")
    ingreso = fields.Integer(compute="_ingreso")
    egreso = fields.Integer(compute="_egreso")

    pedido_ids = fields.One2many('oriflame.pedido', 'producto_id')
    detalle_producto_ids = fields.One2many('oriflame.detalle_producto', 'producto_id')   
    @api.one
    @api.depends('detalle_producto_ids')
    def _egreso(self):
        for detalle_producto in self.detalle_producto_ids:
            self.egreso += detalle_producto.cantidad

    @api.one
    @api.depends('pedido_ids')
    def _ingreso(self):
        for pedido_ids in self.pedido_ids:
            self.ingreso += pedido_ids.cantidadp

    @api.one
    @api.depends('ingreso','egreso')
    def _cal_cantidad(self):
        self.stock = self.ingreso - self.egreso

   
class Tipo(models.Model):
    _name = 'oriflame.tipo'
    _rec_name = 'nombret'

    nombret = fields.Char(string="Nombre Tipo")
  
    producto_ids = fields.One2many('oriflame.producto', 'tipo_id')


class Pedido(models.Model):
     _name = 'oriflame.pedido'
     _rec_name = 'id'
     
     producto_id = fields.Many2one('oriflame.producto')
     detallepedido_id = fields.Many2one('oriflame.detallepedido', string= "Número de Pedido")
     cantidadp = fields.Integer(string="Cantidad")
     totalp = fields.Integer(compute="_pedido_producto", string= "Total")
     totalpuntos = fields.Integer(compute="_punto_producto", string= "Total de Puntos")

     @api.one
     @api.depends('producto_id', 'cantidadp')
     def _pedido_producto(self):
        for producto in self.producto_id:
          self.totalp = producto.preciop * self.cantidadp
     
     @api.one
     @api.depends('producto_id', 'cantidadp')
     def _punto_producto(self):
        for producto in self.producto_id:
          self.totalpuntos = producto.punto * self.cantidadp


class Detallepedido(models.Model):
     _name = 'oriflame.detallepedido'
     _rec_name = 'id'
     
     proveedor_id = fields.Many2one('oriflame.proveedor')
     fecha = fields.Datetime(string= "Fecha de Pedido")
     totaldet = fields.Integer(compute="_totaldet", string= "Total")
     estadop = fields.Selection(
         [('pendiente', 'Pendiente'), ('recibido', 'Recibido')], default='pendiente', string = "Estado de Pedido")
     totalpuntosdet = fields.Integer(compute="_totalpuntosdet", string= "Total de Puntos")
      
     pedido_ids = fields.One2many('oriflame.pedido', 'detallepedido_id')

     @api.one
     @api.depends('pedido_ids')
     def _totaldet(self):
        for pedido in self.pedido_ids:
          self.totaldet += pedido.totalp

    
     @api.one
     @api.depends('pedido_ids')
     def _totalpuntosdet(self):
        for pedido in self.pedido_ids:
          self.totalpuntosdet += pedido.totalpuntos

class Cliente(models.Model):
    _name = 'oriflame.cliente'
    _rec_name = 'nombrec'

    nombrec = fields.Char(string ="Nombre Cliente")
    rutc = fields.Char(string="Rut")
    celularc = fields.Char(String="Celular")
    correoc = fields.Char(String="Correo")
    direccionc = fields.Text(String="Direccion Envio")

    factura_ids = fields.One2many('oriflame.factura', 'cliente_id')

class Factura(models.Model):
    _name = 'oriflame.factura'
    _rec_name = 'id'


    precio = fields.Integer(compute="_precio_factura")
    estado = fields.Selection([ ('pendiente', 'Pendiente'),('entregado', 'Entregado')], default='pendiente')

    cliente_id = fields.Many2one('oriflame.cliente')
    detalle_producto_ids = fields.One2many('oriflame.detalle_producto', 'factura_id')


    @api.one
    @api.depends('detalle_producto_ids')
    def _precio_factura(self):
        total_precio_producto = 0
        for detalle_producto in self.detalle_producto_ids:
            total_precio_producto += detalle_producto.precio
       
        self.precio = total_precio_producto

class Detalle_producto(models.Model):
    _name = 'oriflame.detalle_producto'
    _rec_name = 'id'

    cantidad = fields.Integer()
    precio = fields.Integer(compute="_precio_productos") 
    stock = fields.Integer(compute="_stock")

    factura_id = fields.Many2one('oriflame.factura')
    producto_id = fields.Many2one('oriflame.producto')

    @api.one
    @api.depends('producto_id', 'cantidad')
    def _precio_productos(self):
        for producto in self.producto_id:
            self.precio = producto.preciop * self.cantidad

    @api.one
    @api.depends('producto_id')
    def _stock(self):
        for producto in self.producto_id:
            self.stock = producto.stock

    @api.constrains('cantidad')
    def _validar_stock(self):
        if self.stock < 0:
            raise ValidationError('No hay suficiente stock')
