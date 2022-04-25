# -*- coding: utf-8 -*-
"""
android step implements class
"""

import flybirds.core.global_resource as gr
from flybirds.core.plugin.plugins.default.app_base_step import AppBaseStep
from flybirds.core.plugin.plugins.default.step.app \
    import (install_app, uninstall_app, return_pre_page)
from flybirds.core.plugin.plugins.default.step.schema import jump_to_page

__open__ = ["Step"]


class Step(AppBaseStep):
    """Android Step Class"""

    name = "android_step"

    def install_app(self, context, param):
        param1 = gr.get_ele_locator(param)
        install_app(context, param1)

    def uninstall_app(self, context, param):
        param1 = gr.get_ele_locator(param)
        uninstall_app(context, param1)

    def return_pre_page(self, context):
        return_pre_page(context)

    def jump_to_page(self, context, param):
        jump_to_page(context, param)
