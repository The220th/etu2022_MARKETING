# etu2022_MARKETING

Странное задание по странному предмету... 

## Зависимости

``` bash
> python3 -m venv {venv_folder}
> source {venv_folder}/bin/acticate

> pip3 install --upgrade pip
> pip3 install -r requirements.txt
```

## Настройка и запуск

В файле `questions.json` нужно задать вопросы + ответы. 

В файле `settings.json` нужно установить `ip` и `port`. Например, файл settings.json может выглядить так:

``` json
{
	"ip": "127.0.0.1",
	"port": "8085"
}
```

Также данный порт нужно прописать в `Dockerfile`. 

Вместо `127.0.0.1` можно указать, например, `0.0.0.0` или `192.168.1.228`.

Далее запуск:

``` bash
> python3 start.py
```

И зайти в браузере по `ip` и `port`, который был указан в файле `settings.json`.

По адресу `http://{ip}:{port}` будет опрос.

По адресу `http://{ip}:{port}/see` будут результаты. 