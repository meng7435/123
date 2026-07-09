import os

def test_ci_mock_env():
    """验证CI环境变量CI_TEST是否生效"""
    # CI会注入CI_TEST=1，验证Mock逻辑开关正常
    assert os.getenv("CI_TEST") == "1"

def test_basic_assert():
    """基础校验用例，保证pytest能正常运行"""
    a = 1 + 1
    assert a == 2