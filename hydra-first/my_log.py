import hydra
import logging

# A logger for this file
log = logging.getLogger(__name__)


@hydra.main(config_path=None)
def my_log(_cfg):
    log.info("Info level message")
    log.debug("Debug level message")


if __name__ == "__main__":
    my_log()

'''
$ python my_log.py hydra.verbose=__main__
[2020-02-11 16:09:52,431][__main__][INFO] - Info level message
[2020-02-11 16:09:52,431][__main__][DEBUG] - Debug level message
'''

'''
$ python my_log.py hydra.verbose=True
[2021-12-13 11:44:08,838][HYDRA] Hydra 1.1.1
[2021-12-13 11:44:08,838][HYDRA] ===========
[2021-12-13 11:44:08,838][HYDRA] Installed Hydra Plugins
[2021-12-13 11:44:08,838][HYDRA] ***********************
[2021-12-13 11:44:08,838][HYDRA] 	ConfigSource:
[2021-12-13 11:44:08,838][HYDRA] 	-------------
[2021-12-13 11:44:08,838][HYDRA] 		FileConfigSource
[2021-12-13 11:44:08,838][HYDRA] 		ImportlibResourcesConfigSource
[2021-12-13 11:44:08,838][HYDRA] 		StructuredConfigSource
[2021-12-13 11:44:08,838][HYDRA] 	CompletionPlugin:
[2021-12-13 11:44:08,838][HYDRA] 	-----------------
[2021-12-13 11:44:08,838][HYDRA] 		BashCompletion
[2021-12-13 11:44:08,838][HYDRA] 		FishCompletion
[2021-12-13 11:44:08,838][HYDRA] 		ZshCompletion
[2021-12-13 11:44:08,838][HYDRA] 	Launcher:
[2021-12-13 11:44:08,838][HYDRA] 	---------
[2021-12-13 11:44:08,838][HYDRA] 		BasicLauncher
[2021-12-13 11:44:08,838][HYDRA] 	Sweeper:
[2021-12-13 11:44:08,838][HYDRA] 	--------
[2021-12-13 11:44:08,838][HYDRA] 		BasicSweeper
[2021-12-13 11:44:08,838][HYDRA] 	SearchPathPlugin:
[2021-12-13 11:44:08,838][HYDRA] 	-----------------
[2021-12-13 11:44:08,839][HYDRA] 		HydraColorlogSearchPathPlugin
[2021-12-13 11:44:08,839][HYDRA] 
[2021-12-13 11:44:08,839][HYDRA] Config search path
[2021-12-13 11:44:08,839][HYDRA] ******************
[2021-12-13 11:44:08,909][HYDRA] | Provider       | Search path                             |
[2021-12-13 11:44:08,909][HYDRA] ------------------------------------------------------------
[2021-12-13 11:44:08,909][HYDRA] | hydra          | pkg://hydra.conf                        |
[2021-12-13 11:44:08,910][HYDRA] | hydra-colorlog | pkg://hydra_plugins.hydra_colorlog.conf |
[2021-12-13 11:44:08,910][HYDRA] | schema         | structured://                           |
[2021-12-13 11:44:08,910][HYDRA] ------------------------------------------------------------
[2021-12-13 11:44:08,943][HYDRA] 
[2021-12-13 11:44:08,943][HYDRA] Defaults Tree
[2021-12-13 11:44:08,943][HYDRA] *************
[2021-12-13 11:44:08,943][HYDRA] <root>:
[2021-12-13 11:44:08,943][HYDRA]   hydra/config:
[2021-12-13 11:44:08,943][HYDRA]     hydra/output: default
[2021-12-13 11:44:08,943][HYDRA]     hydra/launcher: basic
[2021-12-13 11:44:08,943][HYDRA]     hydra/sweeper: basic
[2021-12-13 11:44:08,943][HYDRA]     hydra/help: default
[2021-12-13 11:44:08,943][HYDRA]     hydra/hydra_help: default
[2021-12-13 11:44:08,943][HYDRA]     hydra/hydra_logging: default
[2021-12-13 11:44:08,943][HYDRA]     hydra/job_logging: default
[2021-12-13 11:44:08,943][HYDRA]     hydra/callbacks: null
[2021-12-13 11:44:08,943][HYDRA]     hydra/env: default
[2021-12-13 11:44:08,943][HYDRA]     _self_
[2021-12-13 11:44:08,943][HYDRA]   _dummy_empty_config_
[2021-12-13 11:44:08,976][HYDRA] 
[2021-12-13 11:44:08,976][HYDRA] Defaults List
[2021-12-13 11:44:08,976][HYDRA] *************
[2021-12-13 11:44:08,976][HYDRA] | Config path                 | Package             | _self_ | Parent       | 
[2021-12-13 11:44:08,976][HYDRA] ------------------------------------------------------------------------------
[2021-12-13 11:44:08,976][HYDRA] | hydra/output/default        | hydra               | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/launcher/basic        | hydra.launcher      | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/sweeper/basic         | hydra.sweeper       | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/help/default          | hydra.help          | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/hydra_help/default    | hydra.hydra_help    | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/hydra_logging/default | hydra.hydra_logging | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/job_logging/default   | hydra.job_logging   | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/env/default           | hydra.env           | False  | hydra/config |
[2021-12-13 11:44:08,976][HYDRA] | hydra/config                | hydra               | True   | <root>       |
[2021-12-13 11:44:08,976][HYDRA] ------------------------------------------------------------------------------
[2021-12-13 11:44:09,039][HYDRA] Config
[2021-12-13 11:44:09,039][HYDRA] ******
[2021-12-13 11:44:09,040][HYDRA] {}

[2021-12-13 11:44:09,066][__main__][INFO] - Info level message
[2021-12-13 11:44:09,066][__main__][DEBUG] - Debug level message
'''
