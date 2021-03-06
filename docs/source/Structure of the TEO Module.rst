=================================
Structure of the TEO Module
=================================

The code of the TEO module is based on the long-term energy-planning tool OSeMOSYS (Apache License 2.0) [1]. The TEO is built using the python version of OSeMOSYS written in the PULP package of python, which can be accessed at `here <https://github.com/OSeMOSYS/OSeMOSYS_PuLP>`_ . The standalone version of the TEO module can be accessed from `here <https://github.com/ShravanKumar23/EMB3RS-TEO-Module>`_ .

The code for the TEO is written in PULP, python [2]. The user needs to install python and then the python package PULP to run the TEO. The code for the TEO us organised in three python files, ‘TEO_Model’, ‘TEO_functions’ and ‘TEO_running_file’. The ‘TEO_Model’ file contains the code of the TEO module and all the equations of the optimization model. ‘TEO_functions’ contains certain pre and post processing functions that are needed to run the module. ‘TEO_running_file’ is the executable file of the TEO. The user can specify the input file and desired format of outputs in the ‘TEO_running_file’.


The TEO module has been formulated as a linear (mixed-integer) optimisation problem. The objective function is the minimisation of the net present costs of the energy system under analysis, over the time domain of the case. The costs include operational and capital costs. The optimisation is deterministic and assuming perfect foresight and perfect competition. In the TEO module, the user defines the list of existing and potential future technologies as well as the energy vectors flowing between them. Based on the level of temperature, for example Heat Exchanger (HE), Heat Pump (HP), Waste Heat Recovery (WHR) Boiler and thermalenergy storage.The model will then choose the least cost mix of technologies needed to match the source and sink based on defined constraints of capacity, costs etc.


The model is structured into SETS, PARAMETERS and VARIABLES. The model contains equations written based on a linear/mixed integer linear program. The SETS, PARAMETERS and VARIABLES are described below. The optimisation is dynamic, over several years. Each year is divided in a number of time steps. Both the years and the time steps can be defined by the user. The time domain can span over decades and the time resolution can be up to hourly. For a large model i.e. a model with several sources and sinks and amounting up to more than 50 technologies, optimization at a hourly resolution might take several hours and might need a large memory space for example, up to 64 or 128 GB of RAM.
