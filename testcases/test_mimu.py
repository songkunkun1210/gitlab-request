import logging

import allure
import pytest

from common.assert_util import response_body_check
from common.public_function import *
from common.yaml_util import read_yaml


@allure.epic("迷姆消费端-接口")
class TestMain:
    def setup_class(self):
        self.req = RequestHandler()
        self.logger = logging

    @pytest.mark.parametrize('args', yaml_case_data())
    def test_mimu_api(self, args):
        if args['case_name'] is not None:
            # 动态生成标题
            allure.dynamic.title(args['case_name'])
        # 动态获取级别信息
        if args['severity'] is not None:
            allure.dynamic.severity(args['severity'])
        # 动态获取模块名称
        if args['feature'] is not None:
            allure.dynamic.feature(args['feature'])
        # 动态获取用例功能名称
        if args['story'] is not None:
            allure.dynamic.story(args['story'])

        url = get_url(args['url'])
        payload = args['body']
        token = read_yaml('config/config.yaml')['token']
        headers = request_header(payload, token)
        response = self.req.visit("POST", url, headers=headers, json=payload)
        response_json = response.text
        self.logger.info('模块名称: {},测试目的: {} ,响应结果: {}'.format(args['story'], args['case_name'], response_json))
        response_body_check(args, response)
        return response_json

    def teardown_class(self):
        self.logger.info("测试用例执行完毕")
