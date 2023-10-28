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
pip install --no-cache-dir -r requirements.txt
```

# Como usar los comandos
```
python3 main.py --example_tours --drop_tours
```
Pueden usar un o el otro o ninguno, si no usan ninguno se corre el server.
Tambien pueden usar --help para ver una descripcion de los comandos.

Para activar el environment:
```
source my-project-env/bin/activate
```