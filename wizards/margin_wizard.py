# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PricelistMarginWizard(models.TransientModel):
    _name = 'pricelist.margin.wizard'
    _description = 'Set Minimum Margin on Pricelist Items'
    
    margin_percentage = fields.Float(
        string='Minimum Margin (%)', 
        default=65.0,
        required=True,
        help="Minimum profit margin percentage over cost price"
    )
    
    apply_to_all_items = fields.Boolean(
        string='Apply to All Items', 
        default=True,
        help="Apply this margin to all pricelist items"
    )
    
    pricelist_id = fields.Many2one(
        'product.pricelist', 
        string='Pricelist',
        required=True
    )
    
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            res['pricelist_id'] = active_id
        return res
    
    def apply_margin(self):
        self.ensure_one()
        
        domain = [('pricelist_id', '=', self.pricelist_id.id)]
        
        items = self.env['product.pricelist.item'].search(domain)
        
        for item in items:
            item.write({
                'margin_percentage': self.margin_percentage,
                'apply_margin_limit': True
            })
            
        return {'type': 'ir.actions.act_window_close'}
