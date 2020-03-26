# Copyright 2020 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class RolePolicyExportXls(models.AbstractModel):
    _name = "report.role_policy.export_xls"
    _inherit = "report.report_xlsx.abstract"
    _description = "Role Policy XLSX Export"

    def _get_ws_params(self, wb, data, role):
        ws_params = []
        for entry in [
            "acl",
            "menu",
            "act_window",
            "act_server",
            "act_report",
            "modifier_rule",
        ]:
            method = getattr(self, "_get_ws_params_{}".format(entry))
            ws_params.append(method(data, role))
        return ws_params

    def _get_ws_params_acl(self, data, role):

        acl_template = {
            "name": {
                "header": {"value": "Name"},
                "data": {"value": self._render("role_acl.name")},
                "width": 50,
            },
            "model": {
                "header": {"value": "Model"},
                "data": {"value": self._render("role_acl.model_id.model")},
                "width": 20,
            },
            "perm_read": {
                "header": {"value": "Read"},
                "data": {"value": self._render("role_acl.perm_read and 1 or 0")},
                "width": 6,
            },
            "perm_write": {
                "header": {"value": "Write"},
                "data": {"value": self._render("role_acl.perm_write and 1 or 0")},
                "width": 6,
            },
            "perm_create": {
                "header": {"value": "Create"},
                "data": {"value": self._render("role_acl.perm_create and 1 or 0")},
                "width": 6,
            },
            "perm_unlink": {
                "header": {"value": "Delete"},
                "data": {"value": self._render("role_acl.perm_unlink and 1 or 0")},
                "width": 6,
            },
        }
        params = {
            "ws_name": "Role ACLs",
            "generate_ws_method": "_export_acl",
            "title": "Role ACLs",
            "wanted_list": [k for k in acl_template],
            "col_specs": acl_template,
        }
        return params

    def _export_acl(self, workbook, ws, ws_params, data, role):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for role_acl in role.acl_ids:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"role_acl": role_acl},
                default_format=self.format_tcell_left,
            )

    def _get_ws_params_menu(self, data, role):

        menu_template = {
            "name": {
                "header": {"value": "Menu"},
                "data": {"value": self._render("menu.complete_name")},
                "width": 50,
            },
            "menu_id": {
                "header": {"value": "Id"},
                "data": {"value": self._render("menu.id")},
                "width": 5,
            },
        }

        params = {
            "ws_name": "Menu Items",
            "generate_ws_method": "_export_menu",
            "title": "Role ACLs",
            "wanted_list": [k for k in menu_template],
            "col_specs": menu_template,
        }

        return params

    def _export_menu(self, workbook, ws, ws_params, data, role):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for menu in role.menu_ids:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"menu": menu},
                default_format=self.format_tcell_left,
            )

    def _get_ws_params_act_window(self, data, role):

        act_window_template = {
            "name": {
                "header": {"value": "Window Action"},
                "data": {"value": self._render("act_window.name")},
                "width": 50,
            },
            "act_window_id": {
                "header": {"value": "Id"},
                "data": {"value": self._render("act_window.id")},
                "width": 5,
            },
        }

        params = {
            "ws_name": "Window Actions",
            "generate_ws_method": "_export_act_window",
            "title": "Window Actions",
            "wanted_list": [k for k in act_window_template],
            "col_specs": act_window_template,
        }

        return params

    def _export_act_window(self, workbook, ws, ws_params, data, role):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for act_window in role.act_window_ids:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"act_window": act_window},
                default_format=self.format_tcell_left,
            )

    def _get_ws_params_act_server(self, data, role):

        act_server_template = {
            "name": {
                "header": {"value": "Server Action"},
                "data": {"value": self._render("act_server.name")},
                "width": 50,
            },
            "act_server_id": {
                "header": {"value": "Id"},
                "data": {"value": self._render("act_server.id")},
                "width": 5,
            },
        }

        params = {
            "ws_name": "Server Actions",
            "generate_ws_method": "_export_act_server",
            "title": "Server Actions",
            "wanted_list": [k for k in act_server_template],
            "col_specs": act_server_template,
        }

        return params

    def _export_act_server(self, workbook, ws, ws_params, data, role):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for act_server in role.act_server_ids:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"act_server": act_server},
                default_format=self.format_tcell_left,
            )

    def _get_ws_params_act_report(self, data, role):

        act_report_template = {
            "name": {
                "header": {"value": "Report Action"},
                "data": {"value": self._render("act_report.name")},
                "width": 50,
            },
            "act_server_id": {
                "header": {"value": "Id"},
                "data": {"value": self._render("act_report.id")},
                "width": 5,
            },
        }

        params = {
            "ws_name": "Report Actions",
            "generate_ws_method": "_export_act_report",
            "title": "Report Actions",
            "wanted_list": [k for k in act_report_template],
            "col_specs": act_report_template,
        }

        return params

    def _export_act_report(self, workbook, ws, ws_params, data, role):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for act_report in role.act_report_ids:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"act_report": act_report},
                default_format=self.format_tcell_left,
            )

    def _get_ws_params_modifier_rule(self, data, role):

        modifier_template = {
            "model": {
                "header": {"value": "Model"},
                "data": {"value": self._render("rule.model")},
                "width": 50,
            },
            "priority": {
                "header": {"value": "Prio"},
                "data": {"value": self._render("rule.priority")},
                "width": 4,
            },
            "view": {
                "header": {"value": "View"},
                "data": {"value": self._render("rule.view_id.name or ''")},
                "width": 20,
            },
            "view_id": {
                "header": {"value": "View Id"},
                "data": {"value": self._render("rule.view_id.id or ''")},
                "width": 7,
            },
            "view_type": {
                "header": {"value": "View Type"},
                "data": {"value": self._render("rule.view_id.type or ''")},
                "width": 10,
            },
            "element": {
                "header": {"value": "Element"},
                "data": {"value": self._render("rule.element")},
                "width": 50,
            },
            "invisible": {
                "header": {"value": "Invisible"},
                "data": {"value": self._render("rule.modifier_invisible or ''")},
                "width": 25,
            },
            "readonly": {
                "header": {"value": "Readonly"},
                "data": {"value": self._render("rule.modifier_readonly or ''")},
                "width": 25,
            },
            "required": {
                "header": {"value": "Required"},
                "data": {"value": self._render("rule.modifier_required or ''")},
                "width": 25,
            },
        }

        params = {
            "ws_name": "View Modifier Rules",
            "generate_ws_method": "_export_modifier_rule",
            "title": "View Modifier Rules",
            "wanted_list": [k for k in modifier_template],
            "col_specs": modifier_template,
        }

        return params

    def _export_modifier_rule(self, workbook, ws, ws_params, data, role):

        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        # row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_yellow_left,
        )
        ws.freeze_panes(row_pos, 0)

        for rule in role.modifier_rule_ids:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"rule": rule},
                default_format=self.format_tcell_left,
            )
