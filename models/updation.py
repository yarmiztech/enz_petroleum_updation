from odoo import fields,models,api
from datetime import datetime
from odoo.tests.common import Form


class InternalVehicleSaleLine(models.Model):
    _inherit = 'internal.vehicle.sale.line'

    vehicle_id = fields.Many2one('vehicle.config',domain=[('owner_type','=','internal')])


    @api.onchange('nozzle_id')
    def compute_products(self):
        self.product_id = self.nozzle_id.fuel_type.id

    @api.onchange('date', 'product_id')
    def compute_values(self):
        fuel_price = self.env['fuel.price.details'].search([('date', '=', self.date), ('state', '=', 'updated')])
        for line in fuel_price.price_lines:
            if line.fuel_type.id == self.product_id.id:
                self.unit_price = line.price

    @api.onchange('unit_price', 'quantity')
    def compute_price_total(self):
        self.price_subtotal = self.unit_price * self.quantity

    @api.onchange('unit_price', 'price_subtotal')
    def compute_price(self):
        if self.price_subtotal > 0:
            if self.unit_price > 0:
                self.quantity = self.price_subtotal / self.unit_price

class CreditSaleDetails(models.Model):
    _inherit = 'credit.sale.details'

    vehicle_id = fields.Many2one('vehicle.config',domain=[('owner_type','=','external')])


    @api.onchange('nozzle_id')
    def compute_product(self):
        self.product_id = self.nozzle_id.fuel_type.id

    @api.onchange('date', 'product_id')
    def compute_values(self):
        fuel_price = self.env['fuel.price.details'].search([('date', '=', self.date), ('state', '=', 'updated')])
        for line in fuel_price.price_lines:
            if line.fuel_type.id == self.product_id.id:
                self.unit_price = line.price

    @api.onchange('unit_price', 'quantity')
    def compute_price_details(self):
        if self.unit_price > 0:
            if self.quantity > 0:
                self.price_subtotal = self.unit_price * self.quantity
                print(self.price_subtotal)

    @api.onchange('unit_price', 'price_subtotal')
    def compute_price(self):
        if self.unit_price > 0:
            if self.price_subtotal > 0:
                self.quantity = self.price_subtotal / self.unit_price

    @api.onchange('vehicle_id')
    def computecustomer(self):
        self.customer_id = self.vehicle_id.customer_id.id

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def purchase_validate(self):
        self.button_confirm()
        stock_picking = self.env['stock.picking'].search([('purchase_id', '=', self.id)])
        validate = stock_picking.button_validate()
        Form(self.env['stock.immediate.transfer'].with_context(validate['context'])).save().process()
        self.action_create_invoice()
        invoices_list = self.env['account.move'].search([('purchase_id', '=', self.id)])
        for inv in invoices_list:
            inv.invoice_date = datetime.now().date()
        self.invoice_ids.action_post()
