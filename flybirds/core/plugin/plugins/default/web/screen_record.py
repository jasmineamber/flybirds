# -*- coding: utf-8 -*-
"""
web screen record
"""
import os
import time

import flybirds.utils.file_helper as file_helper
import flybirds.utils.flybirds_log as log
import flybirds.utils.uuid_helper as uuid_helper

__open__ = ["ScreenRecordInfo"]


class ScreenRecordInfo:
    name = "web_screen_record"
    instantiation_timing = "plugin"

    def __init__(self):
        self.support = True
        self.start_time = None
        self.end_time = None
        self.process = None
        # 0 Just created 1 Reset state 2 Start recording
        self.status = 0

    @staticmethod
    def record_link(play_wright, scenario, step_index):
        """
        Associate screenshots to report
        """
        support = True
        log.info(
            "link_record support: {}, step_index: {},"
            " len(scenario.steps): {}, if: {}".format(
                str(support),
                str(step_index),
                str(len(scenario.steps)),
                str(len(scenario.steps) > step_index >= 0),
            )
        )
        if not support:
            data = "embeddingsTags, stepIndex={}, " \
                   "<label>the device does not " \
                   "support screen recording</label>".format(step_index)
            scenario.description.append(data)
            return
        feature_name = file_helper.valid_file_name(scenario.feature.name)
        scenario_name = file_helper.valid_file_name(scenario.name)
        if len(scenario.steps) > step_index >= 0:
            file_name = (
                    scenario_name
                    + uuid_helper.create_short_uuid()
                    + str(int(round(time.time() * 1000)))
                    + ".mp4"
            )
            # TODO
            # screen_shot_dir = gr.get_screen_save_dir()
            # current_screen_dir = os.path.join(screen_shot_dir, feature_name)
            current_screen_dir = os.path.join(feature_name)
            file_helper.create_dirs_path_object(current_screen_dir)

            src_path = "../screenshot/{}/{}".format(feature_name, file_name)
            data = (
                'embeddingsTags, stepIndex={}, <video controls width="375">'
                '<source src="{}" type="video/mp4"></video>'.format(
                    step_index, src_path
                )
            )
            scenario.description.append(data)
            src_path = os.path.join(current_screen_dir, file_name)
            log.info(f'web record_link src_path: {src_path}')
            ScreenRecordInfo.web_record(play_wright, src_path)

    @staticmethod
    def web_record(play_wright, src_path):
        browser_type = play_wright.firefox
        browser = browser_type.launch(headless=True)

        context = browser.new_context(record_video_dir='videos')
        page = context.new_page()

        page.goto("https://www.baidu.com/", wait_until='networkidle')
        page.click('#kw')
        page.fill('#kw', '12306')
        page.wait_for_timeout(1000)
        page.click('#su')

        video = page.video
        path = video.path()
        print(f'web_record path: {path}')

        context.close()
        # 将视频另存为
        video.save_as(src_path)
        browser.close()