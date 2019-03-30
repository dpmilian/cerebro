# Commander

## Requirements

- Python 2.7
- Pipenv (https://docs.pipenv.org/)

## Installation and environment activation

```
>cd commander/
>pipenv install
>pipenv shell
```

## Configure connection environment

You must check what port you have to connect depending your OS 
(http://python.dronekit.io/guide/connecting_vehicle.html#get-started-connecting)

You can configure your own environment with your custom file `.env`:

```
>copy .env.sample .env
>vim .env
```

Activate the environment:

```
>export `cat .env`
```


## First connection

```
>cd commander/
>./main.py
```

## Listen location, attitude, velocity and gps

Default:

```
>cd commander/
>./main.py -l
```

### Optional

* Launch external SITL and connect to it:

*Lauch SITL:*

You must have activated python environment.

```
> dronekit-sitl rover-2.50 --home=42.2278287,-8.721840100000009,100,353
```

After SITL is launched you can also connect with your companion software (QGC, MissionPlaner.. ) or
you can connect with *commander*.

*Connection with SITL  at fixed TCP port:*

```
>./main.py --connect "tcp:0.0.0.0:5760" -l
```
