# -*- coding: utf-8 -*-
from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.tools import remove_accents
import logging
import re

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"
    is_custom_header = fields.Boolean(string='Custom Header & footer',
                                      help="Use a custom logo, header and footer for this journal type")
    doc_header = fields.Text(string='Document Header',
                             help="Text that will be inserted as a header in the printed document.")
    doc_footer = fields.Text(string='Document Footer',
                             help="Text that will be inserted as a footer in the printed document.")
    doc_logo = fields.Binary(string='logo', help="set a logo", attachment=False)


    use_own_sequence = fields.Boolean(string='Use Own Sequence',
                                      help="Uses a custom sequence in sales orders")
    sequence_type = fields.Char(string='Sequence Type',
                             help="Set this field to define the sequence type")



