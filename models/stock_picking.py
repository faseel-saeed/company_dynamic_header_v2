# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import time
from ast import literal_eval
from datetime import date, timedelta
from collections import defaultdict

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime, format_date, groupby
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class PickingType(models.Model):
    _inherit = "stock.picking"

    def get_default_journal_id(self):

        current_uid = self._context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user.default_journal_id.id:
            return user.default_journal_id.id
        else:
            raise UserError(_("User does not have a default template selected."))
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
                                 help="Select the journal to ensure that the correct company accounts are reflected",
                                 states={'draft': [('readonly', False)]},
                                 check_company=True,
                                 required=True,
                                 default=get_default_journal_id,
                                 domain="[('id', 'in', suitable_journal_ids)]")
