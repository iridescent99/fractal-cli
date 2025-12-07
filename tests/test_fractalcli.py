from typer.testing import CliRunner


class FractalTaskEngineTest:

    runner = None

    def setup(self):
        self.runner = CliRunner()

    def test_version(self):
