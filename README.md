# Cisco-ISE-High-CPU-Mem


This project is aimed to assist troubleshooting high CPU, high Memory, Application server crashes, etc issues on Cisco Identity Services Engine 2.4+


Sometimes in scenarios where there is instability on Cisco ISE - due to high load, insufficient resources, bugs, etc. - it may cause sudden outages of ISE services. If this occurs frequently, and randomly, it is crucial to collect the necessary logs and outputs as soon as the issue occurs. In cases where the issues are frequent but unpredictable, and manual monitoring is difficult, there's a need to 
    1. automate this log collection, and 
    2. applying a automatic workaround(restarting services).

This program is intended to deliver the above two points.

Inspired by and based on a similar program, ISE AD Monitor, created by Charles Youssef under https://github.com/CiscoSE/ISE-AD-Monitor. 





How this works:
1. This program monitors ISE resource usage and status of application services.
2. In case a high load, high resource usage or crash in services is detected, it will trigger the output logs collection.
3. Addtionally the workaround is applied and an email is sent to notify admins.



Instructions:
1. This program requires Python 3+, and a virtual environment setup. (http://docs.python-guide.org/en/latest/dev/virtualenvs/)
2. Python packages needed are mentioned in requirements.txt, and can be installed with "$ pip install -r requirements.txt".
3. Update the variables in the env file with required info.
4. Verify reachability from client machine(where program is running) to ISE.
5. Run this program '$ python ise_main.py'


Note:
Program will exit in case ISE is unreachable or if it fails to log-in thrice.


License
This project is licensed under GPL v3. You must agree to the terms and conditions mentioned under the LICENSE in order to use this program.
Contribution to and usage of this program is open to all agreeing to the above license terms; Please follow the Code of Conduct listed at https://www.contributor-covenant.org/version/2/0/code_of_conduct/.


__author__ = "Reetam"
__email__ = "reetammandal@rediffmail.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2020 remandal"
__license__ = "GPL v3"