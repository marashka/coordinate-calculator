# coordinate-calculator

Сервис считает координаты космического аппарата по снимку орбиты и интервалу времени. На вход подаются две строки TLE или JSON с элементами орбиты в виде Celestrak OMM. В ответ приходят широта и долгота в градусах и высота в километрах, WGS84. Паспорт аппарата сохраняется в PostgreSQL.

Снимок для примеров ниже — МКС, номер NORAD `25544`, эпоха `2026-10-31T10:25:39.478080Z`. Актуальные элементы публикует [Celestrak](https://celestrak.org/NORAD/elements/gp.php?CATNR=25544).

## Запуск

Нужны Python 3.14 и Docker.

```shell
python3 -m venv .venv
.venv/bin/pip install uv
make venv-install
make db
make dev
```

`make db` поднимает PostgreSQL на порту `5437` и применяет миграции. `make dev` запускает приложение на хосте. Адрес сервера — `http://127.0.0.1:8000`, описание API — `http://127.0.0.1:8000/docs`.

`make up` собирает и запускает приложение и PostgreSQL в Docker Compose, `make down` останавливает их. Миграции контейнер не применяет: их по-прежнему выполняет `make db` с хоста. Процесс в контейнере слушает `127.0.0.1`, поэтому примеры ниже рассчитаны на `make dev`.

## Расчёт по TLE

`POST /v1/coordinates/`

```shell
curl -s -X POST http://127.0.0.1:8000/v1/coordinates/ \
  -H 'Content-Type: application/json' \
  -d @- <<'EOF'
{
  "launch_date": "1998-11-20",
  "start": "2026-10-31T10:25:39.478080Z",
  "end": "2026-10-31T10:25:39.478080Z",
  "step_seconds": 60,
  "elements": {
    "source": "tle",
    "name": "ISS (ZARYA)",
    "line1": "1 25544U 98067A   26304.43448470  .00006246  00000+0  12087-3 0  9997",
    "line2": "2 25544  51.6334 345.8717 0007023 331.3934  28.6669 15.49127356592878"
  }
}
EOF
```

`start` и `end` включены в интервал. Шаг — от 1 до 60 секунд. Здесь они совпадают, поэтому в ответе одна точка, на эпохе снимка:

```json
{
  "points": [
    {
      "time": "2026-10-31T10:25:39.478080Z",
      "latitude_deg": 0.0000592975450172915,
      "longitude_deg": 149.7166234052871,
      "altitude_km": 415.8302653029653
    }
  ]
}
```

## Расчёт по JSON

Тот же снимок в полях OMM. `source` стоит внутри `elements`.

```shell
curl -s -X POST http://127.0.0.1:8000/v1/coordinates/ \
  -H 'Content-Type: application/json' \
  -d @- <<'EOF'
{
  "launch_date": "1998-11-20",
  "start": "2026-10-31T10:25:39.478080Z",
  "end": "2026-10-31T10:26:39.478080Z",
  "step_seconds": 60,
  "elements": {
    "source": "orbit",
    "OBJECT_NAME": "ISS (ZARYA)",
    "OBJECT_ID": "1998-067A",
    "NORAD_CAT_ID": 25544,
    "EPOCH": "2026-10-31T10:25:39.478080",
    "MEAN_MOTION": 15.49127356,
    "ECCENTRICITY": 0.0007023,
    "INCLINATION": 51.6334,
    "RA_OF_ASC_NODE": 345.8717,
    "ARG_OF_PERICENTER": 331.3934,
    "MEAN_ANOMALY": 28.6669,
    "BSTAR": 0.00012087,
    "MEAN_MOTION_DOT": 0.00006246,
    "MEAN_MOTION_DDOT": 0,
    "CLASSIFICATION_TYPE": "U",
    "EPHEMERIS_TYPE": 0,
    "ELEMENT_SET_NO": 999,
    "REV_AT_EPOCH": 59287
  }
}
EOF
```

Интервал в одну минуту даёт две точки: на `start` и через 60 секунд. На эпохе координаты совпадают с ответом по TLE.

## Разработка

Тесты запускаются командой:

```shell
make test
```

Перед коммитом один раз поставьте хук:

```shell
.venv/bin/prek install
```
