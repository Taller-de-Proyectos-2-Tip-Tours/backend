# Como correr el backend

```
sudo docker build -t backend . && sudo docker run -p 5000:5000 backend 
```

# Como correr los tests con code coverage

```
python3 -m pytest --cov-report term --cov=./ tests/ --cov-fail-under=70
```
Si tienen problemas de dependencias ejecutar:

```
pip install pytest-cov

pip install -U pytest
```