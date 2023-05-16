# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Field Service Portal",
    "summary": """Field Service Portal to visualize all tasks""",
    "version": "16.0.0.0.0",
    "category": "Field Service",
    "license": "AGPL-3",
    "author": "LMSI",
    "website": "https://github.com/LMSI-ca/field-service",
    "depends": ["fieldservice", "portal"],
    "data": [
        "views/fsm_order_portal_templates.xml",
        # "security/ir.model.access.csv",
    ],
    "development_status": "Beta",
    "maintainers": ["guilindner"],
}
