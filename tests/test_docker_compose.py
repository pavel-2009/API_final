import os
import re

from .conftest import infra_dir_path, root_dir


class TestDockerfileCompose:

    def test_infra_structure(self):
        assert 'infra' in os.listdir(root_dir), (
            f'Проверьте, что в пути {root_dir} указана папка `infra`'
        )
        assert os.path.isdir(infra_dir_path), (
            f'Проверьте, что {infra_dir_path} - это папка, а не файл'
        )

    def test_docker_compose_file(self):
        docker_compose_yaml = os.path.join(
            infra_dir_path, "docker-compose.yaml"
        )
        docker_compose_yml = os.path.join(
            infra_dir_path, "docker-compose.yml"
        )

        if os.path.isfile(docker_compose_yaml):
            with open(docker_compose_yaml, 'r') as f:
                docker_compose = f.read()
        elif os.path.isfile(docker_compose_yml):
            with open(docker_compose_yml, 'r') as f:
                docker_compose = f.read()
        else:
            assert False, (
                f'Проверьте, что в директорию {infra_dir_path} добавлен '
                f'файл `docker-compose.yaml` или `docker-compose.yml`'
            )

        assert re.search(r'image:\s+postgres:', docker_compose), (
            'Проверьте, что в файл docker-compose добавлен образ postgres'
        )
        pattern = (r'image:\s+([a-zA-Z0-9_]+)(/([a-zA-Z0-9_\-\.]+))?:?'
                   r'([a-zA-Z0-9_\-\.]+)?')
        assert re.search(pattern, docker_compose), (
            'Проверьте, что добавили образ контейнера в файл '
            'docker-compose'
        )
