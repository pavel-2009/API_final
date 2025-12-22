import os
import re

from .conftest import root_dir


class TestWorkflow:

    def test_workflow(self):
        yamdb_workflow_basename = 'yamdb_workflow'
        workflows_dir = os.path.join(root_dir, '.github', 'workflows')

        yaml = f'{yamdb_workflow_basename}.yaml'
        yml = f'{yamdb_workflow_basename}.yml'

        yaml_path = os.path.join(workflows_dir, yaml)
        yml_path = os.path.join(workflows_dir, yml)

        is_yaml = os.path.isfile(yaml_path)
        is_yml = os.path.isfile(yml_path)

        if not is_yaml and not is_yml:
            assert False, (
                f'В каталоге {workflows_dir} не найден файл workflow'
                f'{yaml} или {yml}.\n'
                '(Это нужно для проверки тестами на платформе)'
            )

        if is_yaml and is_yml:
            assert False, (
                f'В каталоге {workflows_dir} не должно быть двух файлов '
                f'{yamdb_workflow_basename} '
                'с расширениями .yaml и .yml\n'
                'Удалите один из них'
            )

        filename = yaml if is_yaml else yml
        filepath = yaml_path if is_yaml else yml_path

        try:
            with open(filepath, 'r') as file:
                yamdb = file.read()
        except FileNotFoundError:
            assert False, (
                f'Проверьте, что добавили файл {filename} в каталог '
                f'{workflows_dir} для проверки'
            )

        push_trigger_exists = (
            re.search(r'on:\s*push:\s*branches:\s*-\smaster', yamdb)
            or 'on: [push]' in yamdb
            or 'on: push' in yamdb
        )

        assert push_trigger_exists, (
            f'Проверьте, что добавили действие при пуше в файл {filename}'
        )
        assert 'pytest' in yamdb, (
            f'Проверьте, что добавили pytest в файл {filename}'
        )
        assert 'appleboy/ssh-action' in yamdb, (
            f'Проверьте, что добавили деплой в файл {filename}'
        )
        assert 'appleboy/telegram-action' in yamdb, (
            'Проверьте, что настроили отправку telegram сообщения '
            f'в файл {filename}'
        )
