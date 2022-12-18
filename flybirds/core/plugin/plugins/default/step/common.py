# -*- coding: utf-8 -*-
"""
Command methods.
"""
import json
import re
import time
import traceback

import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log
from flybirds.core.plugin.plugins.default.screen import BaseScreen
from flybirds.core.driver import ui_driver
from flybirds.core.global_context import GlobalContext
from baseImage import Image


def sleep(context, param):
    time.sleep(float(param))


def screenshot(context):
    step_index = context.cur_step_index - 1
    BaseScreen.screen_link_to_behave(context.scenario, step_index, "screen_")


def ocr(context):
    step_index = context.cur_step_index - 1
    image_path = BaseScreen.screen_link_to_behave(context.scenario, step_index, "screen_", True)
    BaseScreen.image_ocr(image_path)


def change_ocr_lang(context,lang=None):
    """
    change ocr language
    """
    ocr_instance = ui_driver.init_ocr(lang)
    gr.set_value("ocrInstance", ocr_instance)
    context.ocr_instance = ocr_instance
    GlobalContext.ocr_driver_instance = ocr_instance
    log.info("ocr change lang complete with {}".format(lang))


def prev_fail_scenario_relevance(context, param1, param2):
    """
    Related operations for the previous failure scenario
    """
    try:
        print("failed info about param", param2)
        fail_info = gr.get_rerun_info(param2.strip())
        if not (fail_info is None):
            if isinstance(fail_info, str):
                fail_info = json.loads(fail_info)
            if isinstance(fail_info, dict):
                scenario = context.scenario
                step_index = context.cur_step_index - 1

                scenario_uri = "failed function: {}。 senario: {}".format(
                    fail_info["feature_name"], fail_info["scenario_name"]
                )
                scenario_uri = scenario_uri.replace(",", "#")
                data = "embeddingsTags, stepIndex={}, <p>{}</p>".format(
                    step_index, scenario_uri
                )
                scenario.description.append(data)

                if isinstance(fail_info["description"], list):
                    # fail_description = fail_info["description"]
                    for des_item in fail_info["description"]:
                        print("des_item", des_item)
                        if des_item.strip().startswith("embeddingsTags"):
                            if "<image" in des_item and "/screen_" in des_item:
                                continue
                            else:
                                scenario.description.append(
                                    re.sub(
                                        r"stepIndex=\d+",
                                        "stepIndex={}".format(step_index),
                                        des_item,
                                        1,
                                    )
                                )
        else:
            log.warn("not find failed senario info: ", param2)
    except Exception:
        log.warn("rerun failed senario error")
        log.warn(traceback.format_exc())


def img_verify(context, search_image_path):
    """
    verify image exist or not
    """
    step_index = context.cur_step_index - 1
    source_image_path = BaseScreen.screen_link_to_behave(context.scenario, step_index, "screen_", False)
    GlobalContext.image_size = Image(source_image_path).size
    result = BaseScreen.image_verify(source_image_path, search_image_path)
    return result

