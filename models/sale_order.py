# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from itertools import groupby
from markupsafe import Markup

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_is_zero, format_amount, format_date, html_keep_url, is_html_empty
from odoo.tools.sql import create_index

from odoo.addons.payment import utils as payment_utils


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_default_journal_id(self):
        if self.env.user.sudo().default_journal_id:
            return self.env.user.sudo().default_journal_id
        else:
            return None

    suitable_journal_ids = fields.Many2many(
        'account.journal',
        compute='_compute_suitable_journal_ids',
    )


    invoice_filter_type_domain = fields.Char(compute='_compute_invoice_filter_type_domain')

    @api.depends('company_id')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = 'sale'
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)

    journal_id = fields.Many2one('account.journal',
                                 string="Template",
                                 help="Select the template to ensure that the correct company accounts are reflected",
                                 states={'draft': [('readonly', False)]},
                                 check_company=True,
                                 required=True,
                                 default=get_default_journal_id,
                                 domain="[('id', 'in', suitable_journal_ids)]")




