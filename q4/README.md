# quantcast
[Platform Operations Interview Test for Quantcast](../../master/README.md)

## Question 4
In as much detail as possible, explain what happens between the time a computer system is powered on and the operator is presented with a login prompt. Assume the hardware is a basic desktop system running Linux.


## Answer
I will attempt to approximate the boot of a typical desktop system running Linux. For the sake of simplicity, I'll make some assumptions about the hardware and software going forwards:

 * Reasonably modern Intel hardware
 * Power-on from front-panel switch
 * Single CPU socket and core
 * UEFI firmware on the motherboard
 * No coverage of Secure Boot
 * GPT partitioning of a single hard drive
 * Single OS install


### Power-on
Power-on is signalled by a momentary switch grounding a pin on the motherboard. Where in older systems this signal was passed on to the power supply, it now signals the onboard microcontroller (Intel calls it the Management Engine). This microcontroler can either be discrete or integrated into the chipset. Intel hides their ME in the memory controller hub. This microcontroller signals the power suply either via legacy logic signals or an I2C bus interconnection. Once the power supply is up and running, the ME can stop driving the RESET line on the CPU, allowing it to begin running.


### Reset Vector
Once the CPU begins running, it begins by fetching instructions, basically executing an unconditional jump to 0xFFFFFFF0, the architecture's standard reset vector. Since this is 16 bytes from the top of physical memory in the current ("Real") addressing mode, this vector just contains a far jump to the real location of the system initialization code. A legacy feature of the hardware at this point is that the top 12 address lines are held high, allowing address "aliasing". This allows code to be executed from nonvolatile memory mapped at the lowest region of space as if it were at the top of the map.


### Cold boot
Firmware at this point may probe for configuration changes including enumerating the size and type of memory modules installed on the motherboard, and setting up the memory controller to use them. This may include characterizing the transmission lines interconnecting memory for the fastest and most reliable operation. Vendors may also run through memory to validate that it is in fact working correctly, and initialize memory with a specific ECC pattern used to detect corruption.


### Early initialization
The UEFI firmware begins executing, and begins initializing device address registers, allowing initialization before memory mapping is complete. This essentially involves device probing and subsequent configuration. This will include enumeration of the DRAM and PCI bus, identification of device Base Address Registers, and mapping into firmware-controlled I/O space.


### RAM Shadowing
Executing firmware from flash is much slower than executing from DRAM. Because of this, firmware typically copies itself from flash into DRAM as soon as possible after cold boot. On modern systems this is usually handled by the memory controller hub.


### CPU Initialization
The next steps the firmware take initialize the CPU. If needed, a microcode update is transferred from the firmware to the CPU. Next, APICs are configured to manage interrupts from hardware before handers are installed at the transition from Real mode into Protected mode. And finally, several registers are set up with required structures before switching modes. These include the IDT, the GDT, the TSS and LDT. These tables are used by the processor in protected mode in order to maintain state including interrupts and memory segmentation. The control registers CR1 through CR4 are also set.

Paging is also configured here, at least minimally, pointing to the code page that will be executed when CR0 triggers the actual switch into Protected mode.




## References
While the question requested "as much detail as possible", it was not in fact possible to include as much detail as there is available with a bit of googling. Some excellent resources for understanding the boot process on modern Intel architecture systems include:

 * [Booting an Intel Architecture System, Part I: Early Initialization](http://www.drdobbs.com/parallel/booting-an-intel-architecture-system-par/232300699)
 * [Minimum Steps Necessary to Boot an Intel® Architecture Platform](http://www.intel.com/content/dam/www/public/us/en/documents/white-papers/minimal-intel-architecture-boot-loader-paper.pdf)
 * [Secret of Intel Management Engine by Igor Skochinsky](http://www.slideshare.net/codeblue_jp/igor-skochinsky-enpub)
 * [UEFI boot: how does that actually work, then?](https://www.happyassassin.net/2014/01/25/uefi-boot-how-does-that-actually-work-then/)
 * [GDT Tutorial](http://wiki.osdev.org/GDT_Tutorial)


