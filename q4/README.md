# interviewtest
[Platform Operations Interview Test for MumbleCo](../../master/README.md)

## Question 4
In as much detail as possible, explain what happens between the time a computer system is powered on and the operator is presented with a login prompt. Assume the hardware is a basic desktop system running Linux.


## Answer
I will attempt to approximate the boot of a typical desktop system running Linux. For the sake of simplicity, I'll make some assumptions about the hardware and software going forwards:

 * Reasonably modern Intel hardware
 * Power-on from front-panel switch
 * Single CPU socket and core
 * UEFI firmware on the motherboard
 * No coverage of Secure Boot
 * GPT partitioning of a single SATA hard drive
 * Single OS install
 * Standard System V init scripts, no fancy systemd


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


### On-board Device Initialization
Following early initialization, firmware initializes onboard devices. First devices integrated into the chipset, like GPIO, the Programmable Interrupt Controller (APIC), working in conjunction with the on-die LAPIC on the CPU, and timers. Timers include the original PIT, the more modern HPET, and the RTC (or "CMOS clock"). Serial ports and console in/out become available at this point, and the ME takes over clock signal generation.


### PCI Device Enumeration
Firmare enumerates the PCI buses, maps requested memory regions, assigns requested IRQs. Any expansion ROM code is detected and executed. Most modern motherboard bus interfaces like USB, SATA and LAN controllers are located on the PCI bus. The 'video bios' is generally the first option rom executed. Intel systems typically locate input devices like keyboard and mouse behind a "Super I/O" chip. SIO controls PS/2, serial and parallel interfaces. USB interfaces came up earlier, but any pre-OS use of USB input devices must trap the legacy interfaces.


### Memory Map and Bootloading
Before finding and running a boot loader, the firmware must define a map of system memory, which the bootloader access via a real mode interupt service. This map blocks out areas of memory available to the loader/OS, ACPI tables with hardware information, nonvolatile storage regions, and blocks mapped to the APICs. The firmware finally calls Int 19h, "Load Image", which runs the OS loader.


### OS Loader
The OS loader routine in the firmware is called the "UEFI boot manager". This code can read a standardized configuration from a designated area of nonvolatile memory, and read efi binaries off FAT formatted "efi system" partitions. From an ordered list stored in nvram, the boot manager chooses a partition, loads and runs the efi boot loader off the selected system partition, mounted after boot at /boot/efi. On our linux system that will likely be grub2-efi.


### Bootloader
grub2-efi is an efi binary that reads typical grub configuration. Two basic items grub needs are the root device to mount, and the kernel to execute, along with its boot arguments. It can also load additional modules, and uncompress/mount/execute a compressed initial root filesystem. The bootloader mounts the root filesystem, and from it loads the kernel.


### Kernel load
The kernel actually consists of two parts- a small portion of real-mode code, loaded below the 640K barrier, and the rest of the protected-mode kernel we typically refer to. These two parts communicate via the "Linux boot protocol", a shared segment of memory. This is where the boot loader writes a pointer to the kernel's command line arguments. The bootloader then jumps to the kernel's entry point. From this point the kernel code jumps to setup functions that initialize a stack, initializes the bss segment, and then jumps to main().


### Kernel main()
This initial kernel code handles setting a video mode, and preparing to switch to protected mode. First it sets up an initial interrupt table (IDT) and global descriptor table (GDT). After some legacy PC architecture fiddling with what's called the A20 gate, the kernel enables protected mode by setting PE in CR0. The A20 gate enables the 21st address line, which by default is disabled. Initially this was controlled via the keyboard controller, which moved to a multifunction chip called the LPC (Low Pin Cont) controller. Its now either emulated inside the CPU, or absent. At this point paging is still disabled, but the kernel can now address up to 4GB of ram. It jumps to the 32-bit kernel entry point, and begins decompressing the rest of the kernel which was above the 640k real-mode limit. When done, another jump is done, to startup_32() in the now-uncompressed kernel, located at the start of the second megabyte of ram (0x100000).


### Kernel startup_32() through pid 1
This code clears the bss segment, sets up the final GDT, builds page tables, then enables paging. At this point another jump is made to the platform-independent kernel startup, start_kernel(), which initializes the scheduler, memory and timekeeping. A new kernel thread is created from rest_init(), task scheduling is started, and the original thread goes to sleep, calling cpu_idle(). This thread is process 0, which runs whenever there is no other runnable process.  The new thread runs kernel_init(), which initializes any additional CPUs not in our hypothetical system. It then searches a path for init, which is run as pid 1.


### init
init finds its configuration in /etc/inittab for which runlevel to select, and /etc/init/rc.conf for which 'rc' scripts to run when entering/leaving a run level. As it moves through runlevel 0 up to 3 (the default), it runs /etc/rc.d/rc, which runs scripts in /etc/rcX.d, where X is the current run level. When all scripts have completed, the system has finished booting.


### upstart/systemd
Most modern distributions don't boot using init scripts, and now depend on upstart or systemd to start services at boot time, among other fancy tasks. This answer is long enough already. If you'd like to employ me, I will gladly write much more about the init replacement of your choice.




## References
While the question requested "as much detail as possible", it was not in fact possible to include as much detail as there is available with a bit of googling. Some excellent resources for understanding the boot process on modern Intel architecture systems include:

 * [Booting an Intel Architecture System, Part I: Early Initialization](http://www.drdobbs.com/parallel/booting-an-intel-architecture-system-par/232300699)
 * [Minimum Steps Necessary to Boot an Intel® Architecture Platform](http://www.intel.com/content/dam/www/public/us/en/documents/white-papers/minimal-intel-architecture-boot-loader-paper.pdf)
 * [Secret of Intel Management Engine by Igor Skochinsky](http://www.slideshare.net/codeblue_jp/igor-skochinsky-enpub)
 * [UEFI boot: how does that actually work, then?](https://www.happyassassin.net/2014/01/25/uefi-boot-how-does-that-actually-work-then/)
 * [GDT Tutorial](http://wiki.osdev.org/GDT_Tutorial)
 * [Intel Technology Journal (March 2011) "UEFI Today: Bootstrapping the Continuum"](http://www.intel.com/content/dam/www/public/us/en/documents/research/2011-vol15-iss-1-intel-technology-journal.pdf)
 * [The Kernel Boot Process](http://duartes.org/gustavo/blog/post/kernel-boot-process/)
 * [4.2. Boot process, Init and shutdown](http://www.tldp.org/LDP/intro-linux/html/sect_04_02.html)


