import os

from django.conf import settings


class TestRequirements:

    def test_requirements(self):
        req_path = os.path.join(settings.BASE_DIR, "requirements.txt")
        try:
            with open(req_path, 'r') as f:
                requirements = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл requirements.txt'

        assert 'gunicorn' in requirements, (
            'Проверьте, что добавили gunicorn в файл requirements.txt'
        )
        assert 'django' in requirements, (
            'Проверьте, что добавили django в файл requirements.txt'
        )
        assert 'pytest-django' in requirements, (
            'Проверьте, что добавили pytest-django в файл requirements.txt'
        )
