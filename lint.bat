@echo off
REM Change to the directory where the batch script is located
cd %~dp0
call venv\Scripts\activate
echo Running isort on src and tests
isort src tests
echo Running black on src and tests
black src tests
echo Running flake8 on src and tests
flake8 src tests
echo Running pylint on src
pylint src tests
echo Running mypy on src
mypy src tests
echo Linting complete!
