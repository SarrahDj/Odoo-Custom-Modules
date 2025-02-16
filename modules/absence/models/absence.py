from odoo import models, fields, api
from datetime import datetime

class EmployeeAbsence(models.Model):
    _name = 'employee.absence'
    _description = 'Employee Absence'

    name = fields.Char(string='Name', required=True, default=lambda self: self._generate_name())
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    service_id = fields.Many2one('hr.department', string='Service', related='employee_id.department_id', store=True)
    grade_id = fields.Many2one('hr.job', string='Grade', related='employee_id.job_id', store=True)
    reason = fields.Char(string='Reason', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    @api.model
    def _generate_name(self):
        year = datetime.now().year
        sequence = self.env['ir.sequence'].next_by_code('employee.absence.sequence')
        return f"{year}/{sequence}"

    def print_report(self):
        return self.env.ref('absence.report_employee_absence_pdf').report_action(self)
