from pathlib import Path
from setuptools import find_packages, setup

about = {}
exec((Path(__file__).parent / "consignment_portfolio" / "__init__.py").read_text(), about)

setup(
    name="consignment_portfolio",
    version=about["__version__"],
    description="Installable Frappe/ERPNext portfolio app for a consignment outlet workflow",
    author="Patrick Umoh",
    author_email="patrickumoh571@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
