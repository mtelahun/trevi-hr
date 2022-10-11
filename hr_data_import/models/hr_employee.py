# Copyright (C) 2021 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    hire_date = fields.Date(
        help="Initial date of employment if different than date on first contract."
    )
    import_data_id = fields.Many2one("hr.data.import.employee")
