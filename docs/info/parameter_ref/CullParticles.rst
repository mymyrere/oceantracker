##############
CullParticles
##############

**Description:** 

**class_name:** oceantracker.trajectory_modifiers.cull_particles.CullParticles

**File:** oceantracker/trajectory_modifiers/cull_particles.py

**Inheritance:** _BaseTrajectoryModifier> CullParticles


Parameters:
************

	* ``class_name`` :   ``<class 'str'>``   *<optional>*
		Description: Class name as string A.B.C, used to import this class from python path

		- default: ``None``

	* ``cull_interval`` :   ``<class 'float'>``   *<optional>*
		- default: ``86400``
		- min: ``0``

	* ``cull_status_equal_to`` :   ``<class 'str'>``   *<optional>*
		- default: ``None``
		- possible_values: ``dict_keys(['unknown', 'bad_cord', 'cell_search_failed', 'notReleased', 'dead', 'outside_open_boundary', 'frozen', 'stranded_by_tide', 'on_bottom', 'moving'])``

	* ``cull_status_greater_than`` :   ``<class 'str'>``   *<optional>*
		- default: ``dead``
		- possible_values: ``dict_keys(['unknown', 'bad_cord', 'cell_search_failed', 'notReleased', 'dead', 'outside_open_boundary', 'frozen', 'stranded_by_tide', 'on_bottom', 'moving'])``

	* ``probability_of_culling`` :   ``<class 'float'>``   *<optional>*
		- default: ``0.1``
		- min: ``0``
		- max: ``1.0``

	* ``user_note`` :   ``<class 'str'>``   *<optional>*
		- default: ``None``

