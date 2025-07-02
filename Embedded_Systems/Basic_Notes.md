# General Overview
We have essentially two types of computers

### 1 - General Purpose Computers
- Run on Operating Systems (OS) which serves as resource manager. Able to run various softwares, designed for heavy user interaction, use peripherals like displays, keyboards, mice, wireless coms, etc. Laptops Desktops Servers Tablets Smart Phones.

### 2 - Embedded Computers (Microcontrollers (MCU))
- Designed to do one specific task. Think about a coffee maker, toasters, washer/dryer, etc. They are built with enough resource just to get the job done. These are very dedicated in terms of the way software is written to control the hardware and are for the most part designed not to have the software changed. Think about how many times you would need to update the software on your washing maching, vending machines or coffee maker. We call the software in the chip of a MCU a **FIRMWARE** because its not meant to change once software has been written to the chip and placed into the system that it controls. 

    - MCUs have something called a task schedulers where they read variety of sensors and inputs and produce the outputs. The task schedulers are called REAL TIME OPERARTING SYSTEMS (RTOS).
    - Very Common Peripherals - Timers, analog-to-digital converters, digital-to-analog converters, serial interfaces, etc. 
    - These periperals are embedded on the chip as the Central Processing Unit (CPU) in addition to all the memory you need.
    - We can implement the entire embedded computer on a single circuit making it versitile.

## 3.1 What is a computer
A collection of hardware and software that are working together to accomplish a task

![alt text](image.png)

Above we have a **Finite State Machine** (FSM Diagram) where when given an input, it can perform 3 types of operations. We can call the input code **operations code or OpCode (instructions)** for short. So OpCode 1 would represent some input that executed operation 1. This works great however a more practical option would be capturing the input in some sort of storage where instead of waiting for an input state, you can provide multiple inputs and those instructions will execute one by one.

| OpCode # | Side Note |
| --- | --- |
| OpCode 1 | 1's 0's in memory that tell machine which opcode to execute|
| OpCode 1 | You can enter or change the OpCode in the storage |
| OpCode 2 | |
| OpCode 1 | |
| OpCode 3 | |

So in this case SOFTWARE is the sequence of instructions the hardware will execute = Computer
The NUMBER OF INSTRUCTIONS the computer is designed to execute is called **INSTRUCTION SET**

Side Note - A register is also memory but its stored inside the CPU vs memory like RAM which is external. So these OpCodes aren't in registers. RAMs are **DATA MEMORY** or places where you can temporary store data

## 3.2 Computer Hardware
**Control Unit** Knows how to fetch, decode, and execute data. Fetch is what gets the operation code from the **PROGRAM MEMORY** and then decode is what interprets the instruction and picks the operation path to execute 

Data Memory are things like RAMs where you can temporary store data

**Registers** are fast storage inside the Control Unit. They are synchronus and they have enables so you can control when information can be stored and when they cannot. Some of these registers are going to be dedicated and some of them are going to be general purpose. FSM cannot store numbers or store information. So thats where registers come in. If we needed to add numbers, we would need to store the numbers in register temporarily

**Arithmetic Logic Unit (ALU)** - All the combinational logic that we put into our computer that perform all the operations we want. We can do plus minus ands ors etc. So any instruction logic has to be implemented in combinational logic within the ALU block. 

The way it works is that the Control Unit will know and configure the ALU to get ready for its operations and it will know what to do with the results. The ALU will operate on Registers most of the time.

Example, instruction states to add two integers. The two int values will be stored in the registers, the ALU will perform the arithmetic and store the result in a different register for Control Unit to use 

![alt text](FSM.png)

**Bus Systems**
How these components talk to each other. The Inout and Output component is for the user to interact with the computer.
![alt text](<Screenshot 2025-07-01 170454.png>)

### Summary
Program memory (non-volatile) will hold OpCode but also, additional information needed by the instruction. You treat this as read only memory. Programs stored on non-volatile memory, so the computer system does not lose its program when power is removed.

Data Memory (volatile - read-write memory) hold temporary variables that are created by the software program. can be written to and read from during normal operations. 

CPU - 3 sub systems 1. Registers 2. Arithmetic/Logic Unit ALU 3. Control Unit
Control Unit - Fetch -> Decode - Execute. This cycle continues over and over again
Registers - Dedicated registers and General purpose registers
    - Program Counter - Holds the address of the next instruction in program memory to execute
    - Stack Pointer - Way to allocate memory dynamically without having to keep track of specific address
    - Status Register - Contains flags that are asserted when various conditions occur during the execution of program
    - Instruction Register - holds the OpCode that is fetched from program
    - General purpose

ALU - The system that performs all mathematical and logic operations. Contains the logic to produce status bits

I/O Ports - Access the outside world, can be input output or bidirectional. Parallel ports - pass data as a bus and allow more information to be transferred per instruction. Serial Ports - use a single line and send data bit by bit

Bus System - Handles routing of signals between cpu and memory. I/O ports, data memory, and program memory share the address and data busses
    - Memory Address Bus (MAB) - provides a single address to data memory, program memory, and the I/O ports.
    - Memory Data Bus (MDB) - Carries information back and forth between the CPU and the memory & I/O ports
    - Memory Map - gives all the addresses for all locations in memory. So Data Memory, Program Memory, and I/O ports are assigned a unique address
