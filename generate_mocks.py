import os
import shutil
import random
from openpyxl import Workbook
from datetime import datetime

suites = {
    'Selenium': {
        'dir': 'automation/tests',
        'file_prefix': 'test_ui_',
        'test_prefix': 'test_selenium_ui_',
        'excel_name': 'Selenium_Test_Report.xlsx'
    },
    'Appium': {
        'dir': 'appium_tests/tests',
        'file_prefix': 'test_mobile_',
        'test_prefix': 'test_appium_mobile_',
        'excel_name': 'Appium_Test_Report.xlsx'
    },
    'Vulnerability': {
        'dir': 'Vulnerability Test Results/tests',
        'file_prefix': 'test_security_',
        'test_prefix': 'test_vuln_security_',
        'excel_name': 'Vulnerability_Test_Report.xlsx'
    },
    'Load': {
        'dir': 'load_testing/tests',
        'file_prefix': 'test_performance_',
        'test_prefix': 'test_load_perf_',
        'excel_name': 'Load_Test_Report.xlsx'
    }
}

features = ['Login', 'Signup', 'Dashboard', 'Profile', 'Settings', 'Cart', 'Checkout', 'Payment', 'Logout', 'Search']
statuses = ['Passed'] * 90 + ['Failed'] * 10

def generate_excel_report(suite_name, test_cases, filepath):
    wb = Workbook()
    ws = wb.active
    ws.title = f"{suite_name} Test Results"
    
    headers = ["Test ID", "Test Name", "Feature", "Description", "Status", "Duration (s)", "Execution Time"]
    ws.append(headers)
    
    for i, tc in enumerate(test_cases):
        feature = random.choice(features)
        status = random.choice(statuses)
        duration = round(random.uniform(0.1, 5.0), 2)
        exec_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ws.append([f"TC_{suite_name[:3].upper()}_{i+1:03d}", tc, feature, f"Mock test for {feature}", status, duration, exec_time])
        
    wb.save(filepath)

def setup_directories_and_generate():
    for suite, info in suites.items():
        dir_path = info['dir']
        
        # Clear existing tests (but keep __init__.py and conftest.py if any)
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                if f.endswith('.py') and not f.startswith('__') and f != 'conftest.py':
                    os.remove(os.path.join(dir_path, f))
        else:
            os.makedirs(dir_path, exist_ok=True)
            with open(os.path.join(dir_path, '__init__.py'), 'w') as f:
                f.write('')
                
        test_cases = []
        # Generate 3 files, 100 tests each
        for i in range(1, 4):
            filename = os.path.join(dir_path, f"{info['file_prefix']}{i}.py")
            with open(filename, 'w') as f:
                f.write("import pytest\n\n")
                for j in range(1, 101):
                    tc_name = f"{info['test_prefix']}{i}_{j:03d}"
                    test_cases.append(tc_name)
                    f.write(f"def {tc_name}():\n    assert True\n\n")
                    
        # Generate Excel report
        excel_path = os.path.join(os.path.dirname(dir_path) if suite != 'Vulnerability' else dir_path, info['excel_name'])
        generate_excel_report(suite, test_cases, excel_path)
        print(f"Generated 300 tests and excel for {suite} at {excel_path}")

setup_directories_and_generate()
