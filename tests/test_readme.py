import os
import re

from .conftest import root_dir


class TestReadme:

    def test_readme(self):
        readme_path = os.path.join(root_dir, "README.md")
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл README.md'

        re_str = (
            r'https:\/\/github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+'
            r'\/(actions\/)?workflows\/[-a-zA-Z0-9._+]+\/badge\.svg'
        )

        assert re.search(re_str, readme), (
            'Проверьте, что добавили бейдж со статусом работы workflow '
            'в файл README.md'
        )
