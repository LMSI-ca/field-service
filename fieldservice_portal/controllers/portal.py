from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

import logging

_logger = logging.getLogger(__name__)


class FSMCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'fsm_order_count' in counters:
            values['fsm_order_count'] = (
                request.env['fsm.order'].search_count([])
                if request.env['fsm.order'].check_access_rights(
                    'read', raise_exception=False
                )
                else 0
            )
        _logger.info(f"LMSI: os values sao {values}")
        return values

    # def _fsm_orders_get_page_view_values(
    #     self,
    #     fsm_order,
    #     access_token,
    #     page=1,
    #     date_begin=None,
    #     date_end=None,
    #     sortby=None,
    #     search=None,
    #     search_in='content',
    #     groupby=None,
    #     **kwargs,
    # ):
    #     # default filter by value
    #     domain = [('fsm_order_id', '=', fsm_order.id)]
    #     # pager
    #     url = "/my/fsm_order/%s" % fsm_order.id
    #     values = self._prepare_tasks_values(
    #         page,
    #         date_begin,
    #         date_end,
    #         sortby,
    #         search,
    #         search_in,
    #         groupby,
    #         url,
    #         domain,
    #         su=bool(access_token),
    #     )
    #     # adding the access_token to the pager's url args,
    #     # so we are not prompted for loging when switching pages
    #     # if access_token is None, the arg is not present in the URL
    #     values['pager']['url_args']['access_token'] = access_token
    #     pager = portal_pager(**values['pager'])

    #     values.update(
    #         grouped_tasks=values['grouped_tasks'](pager['offset']),
    #         page_name='fsm_order',
    #         pager=pager,
    #         # project=project,
    #         # task_url=f'projects/{project.id}/task',
    #     )
    #     # default value is set to 'project' in _prepare_tasks_values, so we have to set it to 'none' here.
    #     if not groupby:
    #         values['groupby'] = 'none'

    #     return self._get_page_view_values(
    #         fsm_order, access_token, values, 'my_fsm_orders_history', False, **kwargs
    #     )

    @http.route(
        ['/my/fsm_orders', '/my/fsm_orders/page/<int:page>'],
        type='http',
        auth="user",
        website=True,
    )
    def portal_my_fsm_orders(self, page=1, **kw):
        values = {}
        domain = [('is_visible', '=', True)]
        orders_count = request.env['fsm.order'].search_count(domain)
        pager = portal_pager(
            url="/my/fsm_orders", total=orders_count, page=page, step=20
        )
        orders = request.env['fsm.order'].search(
            domain, limit=20, offset=pager['offset']
        )
        values.update(
            {
                'orders': orders,
                'page_name': 'orders',
                'pager': pager,
                'default_url': '/my/fsm_orders',
            }
        )
        _logger.info(f"LMSI: os values da LISTA DE ORDERS sao {values}")
        return request.render("fieldservice_portal.portal_my_fsm_orders", values)

    @http.route(
        ['/my/fsm_orders/<int:order_id>'], type='http', auth="public", website=True
    )
    def portal_my_fsm_order(
        self, order_id, report_type=None, access_token=None, project_sharing=False, **kw
    ):
        try:
            task_sudo = self._document_check_access('fsm.order', order_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('pdf', 'html', 'text'):
            return self._show_task_report(
                task_sudo, report_type, download=kw.get('download')
            )

        fsm_order = request.env['fsm.order'].sudo().browse(order_id)

        # ensure attachment are accessible with access token inside template
        # for attachment in task_sudo.attachment_ids:
        #     attachment.generate_access_token()
        if project_sharing is True:
            # Then the user arrives to the stat button shown in form view of project.task and the portal user can see only 1 task
            # so the history should be reset.
            request.session['my_tasks_history'] = task_sudo.ids
        # values = self._get_page_view_values(
        #     task_sudo, access_token, values, 'my_fsm_orders_history', False, **kw
        # )
        values = {'page_name': 'fsm order', 'order': fsm_order}
        _logger.info(f"LMSI: os values da Order sao {values}")
        return request.render("fieldservice_portal.portal_my_fsm_order", values)
