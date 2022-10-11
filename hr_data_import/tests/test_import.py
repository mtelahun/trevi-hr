# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date

from odoo.tests import common


class TestImport(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.DataImport = cls.env["hr.data.import.employee"]
        cls.Department = cls.env["hr.department"]
        cls.Job = cls.env["hr.job"]
        cls.PayrollStructure = cls.env["hr.payroll.structure"]
        cls.PolicyGroup = cls.env["hr.policy.group"]
        cls.Schedule = cls.env["hr.payroll.period.schedule"]
        cls.SalaryRule = cls.env["hr.salary.rule"]
        cls.SalaryRuleCateg = cls.env["hr.salary.rule.category"]

        # Payroll related
        #
        cls.categ_basic = cls.SalaryRuleCateg.create(
            {
                "name": "Basic",
                "code": "BASIC",
            }
        )
        cls.rule_basic = cls.SalaryRule.create(
            {
                "name": "Basic Salary",
                "code": "BASIC",
                "sequence": 1,
                "category_id": cls.categ_basic.id,
                "condition_select": "none",
                "amount_select": "code",
                "amount_python_compute": "result = contract.wage",
            }
        )
        cls.pay_structure = cls.PayrollStructure.create(
            {
                "name": "Basic Salary Structure",
                "code": "BSS",
                "company_id": cls.env.ref("base.main_company").id,
                "rule_ids": [
                    (4, cls.rule_basic.id),
                ],
            }
        )

        cls.dept_sales = cls.Department.create({"name": "Sales"})
        cls.job_sales_rep = cls.Job.create(
            {"name": "Sales Rep", "department_id": cls.dept_sales.id}
        )
        cls.pps = cls.Schedule.create(
            {
                "name": "PPS",
                "tz": "Africa/Addis_Ababa",
                "type": "manual",
                "initial_period_date": date.today(),
            }
        )
        cls.policy_group = cls.PolicyGroup.create(
            {
                "name": "Default Policy Group",
            }
        )
        cls.data = cls.DataImport.create(
            [
                {
                    "name": "Sally Ford",
                    "gender": "female",
                    "street": "123 A Avenue",
                    "private_phone": "(555) 555-5555",
                    "emergency_contact": "John Doe",
                    "emergency_phone": "(555) 555-666",
                    "date_start": date.today(),
                    "wage": 5000.00,
                    "job_id": cls.job_sales_rep.id,
                    "struct_id": cls.pay_structure.id,
                    "pps_id": cls.pps.id,
                    "policy_group_id": cls.policy_group.id,
                },
                {
                    "name": "John Doe",
                    "gender": "male",
                    "birthday": date(2000, 1, 1),
                    "marital": "single",
                    "street": "456 B Avenue",
                    "private_phone": "(555) 555-666",
                    "date_start": date.today(),
                    "wage": 4000.00,
                    "job_id": cls.job_sales_rep.id,
                    "struct_id": cls.pay_structure.id,
                    "pps_id": cls.pps.id,
                    "policy_group_id": cls.policy_group.id,
                },
            ]
        )

    def test_workflow(self):
        self.data.action_import_employees()

        for rec in self.data:
            self.assertTrue(
                rec.related_employee_id,
                f"The created employee is linked to the data record: '{rec.name}'",
            )
            self.assertTrue(
                rec.related_employee_id.address_home_id,
                f"The employee has a home address record: '{rec.name}'",
            )
            self.assertEqual(
                rec.related_employee_id.address_home_id.type,
                "private",
                f"The employee home address contact type is private: '{rec.name}'",
            )
            self.assertEqual(
                rec.state,
                "imported",
                f"The record state is 'imported' after employee creation: '{rec.name}'",
            )
