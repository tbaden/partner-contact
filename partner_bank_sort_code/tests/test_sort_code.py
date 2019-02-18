# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from psycopg2 import IntegrityError


class TestSortCode(common.TransactionCase):

    def setUp(self):
        super(TestSortCode, self).setUp()

        self.bank_obj = self.env['res.bank']

        vals = {
            'name': 'BANK 1',
            'sort_code': '95-01-32',
        }
        self.bank_1 = self.bank_obj.create(vals)

        vals = {
            'name': 'BANK 2',
            'sort_code': '95-01-33',
        }
        self.bank_2 = self.bank_obj.create(vals)

    def test_sort_code_duplicate(self):
        vals = {
            'name': 'BANK 3',
            'sort_code': '95-01-32',
        }
        with self.assertRaises(IntegrityError):
            self.bank_obj.create(vals)

    def test_sort_code(self):
        vals = {
            'name': 'BANK 3',
            'sort_code': '95-01-34',
        }
        self.bank_obj.create(vals)

    def test_sort_code_inactive(self):
        self.bank_1.write({'active': False})
        vals = {
            'name': 'BANK 3',
            'sort_code': '95-01-32',
        }
        self.bank_obj.create(vals)
