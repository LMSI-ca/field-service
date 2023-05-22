from odoo import models, fields, api


class PortalFSMOrder(models.Model):
    _inherit = 'fsm.order'

    _description = "FSM Order for Portal"

    # user_ids = fields.Many2many('res.users', relation='project_task_user_rel', column1='task_id', column2='user_id', string='Responsável')
    person_id = fields.Many2one("res.users", string="Responsável", index=True)

    def _compute_is_visible(self):
        for order in self:
            order.is_visible = order.user_id == self.env.user

    is_visible = fields.Boolean(string="Is Visible", compute="_compute_is_visible")
