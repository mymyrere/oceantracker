#################
TerminalVelocity
#################

**Description:** 

**class_name:** oceantracker.velocity_modifiers.terminal_velocity.TerminalVelocity

**File:** oceantracker/velocity_modifiers/terminal_velocity.py

**Inheritance:** VelocityModiferBase> TerminalVelocity


Parameters:
************

	* ``class_name`` :   ``<class 'str'>``   *<optional>*
		Description: Class name as string A.B.C, used to import this class from python path

		- default: ``None``

	* ``is3D`` :   ``<class 'bool'>``   *<optional>*
		- default: ``False``
		- possible_values: ``[True, False]``

	* ``user_note`` :   ``<class 'str'>``   *<optional>*
		- default: ``None``

	* ``value`` :   ``<class 'float'>``   *<optional>*
		Description: Terminal velocity positive upwards, ie fall velocities ate negative

		- default: ``0.0``

	* ``variance`` :   ``<class 'float'>``   *<optional>*
		Description: variance of normal distribution of terminal velocity, used to give each particles its own terminal velocity from random normal distribution

		- default: ``None``
		- min: ``0.0``

