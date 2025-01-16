import logging
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from jupyter_client.kernelspec import KernelSpecManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostInstallCommand(install):
    def run(self):
        super().run()
        self.install_kernelspec()

    def install_kernelspec(self):
        kernel_spec_dir = Path(__file__).resolve().parent / 'bosque_kernel' / 'kernelspec'
        if not kernel_spec_dir.is_dir():
            logger.error("Kernel spec directory not found.")
            return
        try:
            km = KernelSpecManager()
            km.install_kernel_spec(str(kernel_spec_dir), 'bosque', user=False, replace=True)
            logger.info("Bosque Jupyter kernel installed successfully.")
        except Exception:
            logger.exception("Failed to install Bosque Jupyter kernel")

setup(
    name='bosque_kernel',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pygments',
        'ipykernel>=6.29.5',
        'jupyter_client',
    ],
    package_data={
        'bosque_kernel': ['kernelspec/kernel.json'],
    },
    entry_points={
        'console_scripts': [
            'kernel = bosque_kernel.kernel:main',
        ],
        'pygments.lexers': [
            'bosque = bosque_kernel.lexer:BosqueLexer',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    include_package_data=True,
)
