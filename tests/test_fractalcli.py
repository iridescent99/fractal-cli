from typer.testing import CliRunner


class FractalCliTest:

    runner = None

    def setup(self):
        self.runner = CliRunner()


