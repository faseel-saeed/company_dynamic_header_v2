# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.bus.models.bus_presence import AWAY_TIMER
from odoo.addons.bus.models.bus_presence import DISCONNECTION_TIMER


class ResUsers(models.Model):
    _inherit = "res.users"

    suitable_journal_ids = fields.Many2many(
        'account.journal',
        compute='_compute_suitable_journal_ids',
    )

    @api.depends('company_id')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = 'sale'
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)

    default_journal_id = fields.Many2one('account.journal',
                                 string="Template",
                                 help="Default journal to set in invoices for this user",
                                 states={'draft': [('readonly', False)]},
                                 check_company=True,
                                 required=False,
                                 domain="[('id', 'in', suitable_journal_ids)]")