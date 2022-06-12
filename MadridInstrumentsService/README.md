# Madrid Instruments Service

This is a REST service that will simulate the control electronic instruments used in
superconducting based quantum computers. The simulation is pretty straightforward, and not Quantum
at all.

## Service documentation

### Endpoints

This is the endpoint for loading a program: 

```
POST /program/load
```

The input of the service is a sequence of pulses and values that will map to some simple algebraic
operations: Summation, Multiplication and Division.

The format of the input JSON should follow this schema:

```
{
   "program_code":[
      10,
      "Madrid_initial_state_pulse",
      120,
      "Madrid_pulse_1",
      3,
      "Madrid_pulse_2",
      "Madrid_pulse_2",
      2,
      "Madrid_pulse_2",
      "Madrid_pulse_1"
   ]
}
```


In case of success, the HTTP code will be 200 and the response JSON will be:
```
{
     "program_id": "MadridProgramId1"
}
```

This is the endpoint for triggering the execution of the program:

```
GET /program/run/<program_id>
```

In case of success, the HTTP code will be 200 and the response JSON will be:
```
{
     "result": 195
}
```


### Workflow

Due to some hardware imposed constrains, we always need to load the program first, and then
trigger the execution. When we call the `/load_program` endpoint with the corresponding request
body and we will receive a response with a "Program ID". This "Program ID" needs to be used in a
later call to the `/run_program` endpoint so the service identifies the program to run.

This implies two REST calls:
```
POST /program/load {...}
GET /program/run/<program_id>
```

## Installing and running the application

The application is provided as a [`fastapi`] application, which can be run [`using uvicorn`]
(included as a dependency for convenience) or any other ASGI-server.

### Installing the application

```bash
$ pip install .
```

This will install the application and all its dependencies.

### Executing the application


```bash
$ uvicorn madrid_instruments_service.main:app
INFO:     Started server process [477295]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

This will execute the application, listening by default at http://127.0.0.1:8000. You can also
check the documentation for the endpoints at http://127.0.0.1:8000/docs.

[`fastapi`]: http://fastapi.tiangolo.com/
[`using uvicorn`]: https://fastapi.tiangolo.com/deployment/manually/
