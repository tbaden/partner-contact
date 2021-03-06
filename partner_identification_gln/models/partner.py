# -*- coding: utf-8 -*-
# ©  2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from openerp import api, models
_logger = logging.getLogger(__name__)

try:
    from stdnum import ean
    from stdnum.exceptions import InvalidChecksum
except ImportError:
    _logger.debug('Cannot `import external dependency python stdnum package`.')


class ResPartnerIdCategory(models.Model):
    _inherit = 'res.partner.id_category'

    def _search_duplicate(self, category_id, id_number, force_active=False):
        domain = [('category_id', '=', category_id),
                  ('name', '=', id_number.name),
                  ('name', '!=', False),
                  ('id', '!=', id_number.id)]

        if force_active:
            domain.append(('partner_id.active', '=', True))
        num_obj = self.env['res.partner.id_number']
        return num_obj.search(domain)

    @api.multi
    def validate_res_partner_gln(self, id_number):
        self.ensure_one()
        if not id_number:
            return False

        try:
            ean.validate(id_number.name)
        except InvalidChecksum:
            return True

        cat = self.env.ref('partner_identification_gln.'
                           'partner_identification_gln_number_category').id
        duplicate_gln = self._search_duplicate(cat, id_number, True)

        if duplicate_gln:
            return True

        return False

    @api.multi
    def validate_res_partner_gcp(self, id_number):
        self.ensure_one()
        if not id_number:
            return False

        if len(id_number.name) < 1 or len(id_number.name) > 12:
            return True

        cat = self.env.ref('partner_identification_gln.'
                           'partner_identification_gcp_number_category').id
        duplicate_gln = self._search_duplicate(cat, id_number)

        if duplicate_gln:
            return True

        return False
