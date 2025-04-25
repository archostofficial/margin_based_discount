# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    
    # Add margin percentage field
    margin_percentage = fields.Float(
        string='Minimum Margin (%)', 
        default=0.0,
        help="Minimum profit margin percentage over cost price that must be maintained regardless of discount"
    )
    
    apply_margin_limit = fields.Boolean(
        string='Limit Discount by Margin',
        default=False,
        help="If checked, the discount will not reduce the price below the minimum margin threshold"
    )
    
    @api.constrains('margin_percentage')
    def _check_margin_percentage(self):
        for item in self:
            if item.margin_percentage < 0 or item.margin_percentage > 100:
                raise ValidationError(_("Margin percentage must be between 0 and 100."))
    
    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        """Override to implement margin-based pricing limits"""
        # First call the original method to get the standard calculated price
        price = super()._compute_price(price, price_uom, product, quantity, partner)
        
        # If margin limit is not applied, return the standard price
        if not self.apply_margin_limit:
            return price
            
        # Get the product cost
        cost = product.standard_price
        if not cost:
            return price  # If no cost defined, can't apply margin logic
            
        # Calculate the minimum price based on cost and margin percentage
        min_price = cost * (1 + (self.margin_percentage / 100))
        
        # Return the greater of the calculated price and minimum price
        return max(price, min_price)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"
    
    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        """Override to implement margin-based pricing limits at pricelist level"""
        results = super()._compute_price_rule(products_qty_partner, date, uom_id)
        
        # Process each product in the results
        for product_id, (price, rule_id) in results.items():
            rule = self.env['product.pricelist.item'].browse(rule_id)
            
            # If this rule applies margin limiting
            if rule.apply_margin_limit and rule.margin_percentage > 0:
                product = self.env['product.product'].browse(product_id)
                
                # Get the product cost
                cost = product.standard_price
                if cost:
                    # Calculate the minimum price based on cost and margin percentage
                    min_price = cost * (1 + (rule.margin_percentage / 100))
                    
                    # Apply the minimum price if needed
                    if price < min_price:
                        results[product_id] = (min_price, rule_id)
        
        return results
