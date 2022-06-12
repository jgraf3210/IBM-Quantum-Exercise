# IBM Quantum Systems software exercise proposal

We are building a new and exciting Quantum Computer!
To improve user experience, we will allow our users to write high level quantum programs. Your task is to write a piece of system software that will compile, load, and run the user programs.
Let's start with some terminologies!


## What is a quantum computer?
These quantum computers use quantum bits, or qubits, to carry information. We use microwave pulses to manipulate the qubits into desired states and to measure their final values. The specialty hardware used to generate these microwave pulses are called **control instruments**.


## What is a quantum program?
A quantum program contains source code that can be run on a quantum computer. Similar to the early years of classical computing, when people wrote in assembly to manipulate bits and registers, quantum programs today often consist of low level operations.

For the purpose of this exercise, let's assume that a quantum program is just a set of very simple **arithmetic operations** sequentially applied. Let's further assume these operations include only summation, multiplication, and division.
This is an example of one arithmetic quantum program that could be the (json) input of our software:
```
{
  "id": "abcdefghijkl",
  "control_instrument": "ACME",
  "initial_value": 10,
  "operations": [
    {
      "type": "Sum",
      "value": 120
    },
    {
      "type": "Mul",
      "value": 3
    },
    {
      "type": "Div",
      "value": 2
    }
  ]
}

```

## Some clarifications on the fields

* **control_instrument**: The name of the control instrument this quantum program is targeting.
* **initial_state**: This is the initial value of the quantum computer, right before we start running.
* **operations**: An array of arithmetic operations to apply.
* **type**: Indicates the type of operation: summation ("Sum"), multiplication ("Mul"), or division ("Div"). The "value" field contains the value to use. In the example above, the result will be ((10+120)*3)/2 = 195.

## What is a Control Instrument?
Similar to how classical programs need to be compiled into machine code before it can be loaded into a CPU, our "high level" quantum programs also need to be compiled into microwave pulse representation. The pulse representation can then be loaded into a control instrument to generate the correct pulses.

The funny thing though, is that every instrument manufacturer has its own pulse representation. So a higher-level operation like Sum will be translated into different pulse sequence representations depending on the instrument used. The following table shows the pulse sequences from two different manufacturers, `ACME Instruments` and `Madrid Instruments`:

## High-level operation

| Arithmetic Operation | ACME Instruments Pulse sequence | Madrid Instruments Pulse sequence |
| -------------------- | ------------------------------- | --------------------------------- |
| Sum \<Value\>        |           Acme_pulse_1          |            Value                  |
|                      |           Acme_pulse_2          |            Madrid_pulse_1         |
|                      |           Value                 |                                   |
| Mul \<Value\>        |           Acme_pulse_2          |             Value                 |
|                      |           Acme_pulse_1          |             Madrid_pulse_2        |
|                      |           Acme_pulse_1          |             Madrid_pulse_2        |
|                      |           Value                 |                                   |
| Div \<Value\>        |           Acme_pulse_2          |             Value                 |
|                      |           Acme_pulse_2          |             Madrid_pulse_2        |
|                      |           Value                 |             Madrid_pulse_1        |
| Initial_state \<Value\>|      Acme_initial_state_pulse |       Value                       |
|                      |        Value                    |       Madrid_initial_state_pulse  |
	

Your task here is to build a system software that will translate a high-level quantum program, which is the input of the software, into a pulse sequence that will be loaded and executed on a specific control instrument.  Also, you need to design your software in a way that is easy to extend in the case that we support dozens of different control instruments.
The solution you will submit will only integrate with two of these control systems though: `ACME Instruments` and `Madrid Instruments`. We provide you with two REST services that simulate the control instrument systems for these two manufacturers.

You can get them here:
- https://github.com/atilag/AcmeInstrumentsService
- https://github.com/atilag/MadridInstrumentsService

Read the README on notes about running them.
These programs will return a response with the result of the computation.


## An example
Let's assume that your system software gets this quantum program as an input:
```
{
  "id": "abcdefghijkl",
  "control_instrument": "ACME",
  "initial_value": 10,
  "operations": [
    {
      "type": "Sum",
      "value": 120
    },
    {
      "type": "Mul",
      "value": 3
    },
    {
      "type": "Div",
      "value": 2
    }
  ]
}
```

The software then takes the following steps:
1. Translate the program into pulse representation in JSON format, for an `ACME Instruments` device (which is the target taken from the **control_instrument** field):
```
{
  "program_code": [
    "Acme_initial_state_pulse",
    10,
    "Acme_pulse_1",
    "Acme_pulse_2",
    120,
    "Acme_pulse_2",
    "Acme_pulse_1",
    "Acme_pulse_1",
    3,
    "Acme_pulse_2",
    "Acme_pulse_2",
    2
  ]
}
```


2. Send this JSON message to the `ACME Instruments` REST Service through the exposed `/load_program` endpoint via POST:
```
POST /load_program
{
  "program_code": [
    "Acme_initial_state_pulse",
    10,
    "Acme_pulse_1",
    "Acme_pulse_2",
    120,
    "Acme_pulse_2",
    "Acme_pulse_1",
    "Acme_pulse_1",
    3,
    "Acme_pulse_2",
    "Acme_pulse_2",
    2
  ]
}
```
3. Receive a program ID that identifies the pulse program just loaded: `AcmeProgramId1`:
```
{
  "program_id": "AcmeProgramId1"
}
```

4. Trigger the execution of the program using the `ACME Instruments` REST Service endpoint: `/run_program` via GET:
```
GET /run_program/AcmeProgramId1
```
5. Receive the result of the execution of the quantum program: `195`:
```
{
  "result": 195
}
```

6. Return the result to the user or print it to stdout

## What are we expecting to see in the code
- Clean code!
  - Think of it as high-quality production-ready code BUT is fine to make these assumptions/exceptions:
  - The vendor-specific control instrument REST service connection is always fine, you don't have to write a rock-solid code around connecting to to the REST service.
  - We could also assume that the input of the system is always well-formed. No edge cases, or complex user-facing error strategies.
  - Use comments to explain design decisions if you want, but we are sure that your code talks by itself :)
- Testing!
  - Implement just a few (3 or 4) acceptance and unitary tests.
  - If you can think of more interesting tests, just write the functions signature and make it clear what you want to test but do not implement then, just assert to true.
- Pragmatism!
  - Do not over-engineer
  - Is fine if you take assumptions and write code that reflects them. But don't go crazy! Drop us a message if you have questions.
  - You are free to write comments with the tradeoffs, assumptions, notes you want us to know. Let your code talk for yourself!
- Maintainability over performance!
  - Maintainable code is preferred over performant code in general, but it's ok if you want to make some part performant on purpose, just let us know in a comment if you took this decision so we are aware that expressiveness has been scarified a little bit in favor of performance. Let us also know why do you think this code is performant! :)
- It works! (mostly)
  - We will run a set of tests with the inputs we provide just to check the software is correct... it's OK if there are some edge-cases not covered, but in general the software needs to work as expected.


## Restrictions/Notes
- We provide with two files: `quantum_program_input.json` and `large_quantum_program_input.json`. The former is just one arithmetic quantum program, and the latter is a list of 50 arithmetic quantum programs.
- The case for one arithmetic quantum program as the JSON input is exactly the same as the example above, and the case of a list of arithmetic quantum programs is in the form of:
```
[
  {"id": "asdfghjkl1...", ...}
  {"id": "asdfghjkl5...", ...}
  {"id": "asdfghjkl9...", ...}
  ...
]
```
- Each of the arithmetic quantum program in the list could have one of the two **control instrument** manufacturer: `Acme Instruments` or `Madrid Instruments`.
```
[
  {"id": "asdfghjkl1...", control_instrument: "ACME", ... }
  {"id": "asdfghjkl5...", control_instrument: "MADRID", ...}
  {"id": "asdfghjkl9...", control_instrument: "ACME",...}
  ...
]
```
- As we are targeting two different **control instruments** manufacturers: `Acme Instruments` and `Madrid Instruments` and both REST services run in different processes, there's a chance to improve execution performance, we would like to see how! :)
- We also provide a handy tool: `generate-quantum-programs.py`. This tool will generate random lists of inputs. We think this could be useful as a testing tool, you can read the details in the header of the source file.
- You can choose to build a command line tool or a REST service if you prefer, we don't care, whatever works better for you. We will provide the input as files but it's ok if you want to create a client-like app to send the input.
- Use non-GPL open-source libraries/packages/crates if you need/want to (you don't have to parse JSON by yourself nor implement HTTP protocol ;))
- You are free to choose whatever build system, runtime environment, toolchain works better for you.
- Drop some documentation on how to compile/run your program!

## What programming language can I use to code the solution?
Use the programming language you are more confortable with from this list:
Rust, C++, C, Go, Java, Typescript, C#, Python, Javascript, PHP.
If you want to use other language not included in this list, drop us an email and we can discuss.


## How to submit the test
We are proposing 2 ways:
1. Create a Github repository and send us your link so we can clone it :)
2. Send an email with the .tgz/.zip/.7z/etc

Thank you very much for participating and spending your precious time with us!

IBM Quantum Systems team.