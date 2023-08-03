obj-m := adv7511.o

adv7511-y := adv7511_drv.o adv7533.o
adv7511-$(CONFIG_DRM_I2C_ADV7511_AUDIO) += adv7511_audio.o
adv7511-$(CONFIG_DRM_I2C_ADV7511_CEC) += adv7511_cec.o
adv7511-$(CONFIG_DEBUG_FS) += adv7511_debugfs.o
obj-$(CONFIG_DRM_I2C_ADV7511) += adv7511.o

SRC := $(shell pwd)

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC)

modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install

clean:
	rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c
	rm -f Module.markers Module.symvers modules.order
	rm -rf .tmp_versions Modules.symvers