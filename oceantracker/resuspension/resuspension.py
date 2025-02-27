# modfiy aspects pof all isActive particles, ie moving and stranded
from oceantracker.util.parameter_checking import ParamValueChecker as PVC
import numpy as np
from oceantracker.resuspension._base_resuspension import _BaseResuspension


from numba import  njit

class BasicResuspension(_BaseResuspension):
    # based on
    # Lynch, Daniel R., David A. Greenberg, Ata Bilgili, Dennis J. McGillicuddy Jr, James P. Manning, and Alfredo L. Aretxabaleta.
    # Particles in the coastal ocean: Theory and applications. Cambridge University Press, 2014.
    # Equation  eq 9.26 and 9.28

    def __init__(self):
        # set up info/attributes
        super().__init__()  # required in children to get parent defaults
        self.add_default_params({
                'critical_friction_velocity': PVC([0.], [float], min=[0.], doc_str='Critical friction velocity, u_* in m/s defined in terms of bottom stress (this param is not the same as near seabed velocity)'),
                'friction_velocity_field_class_name': PVC('oceantracker.fields.friction_velocity.FrictionVelocity', str)
                                 })

    # is 3D test of parent
    def check_requirements(self):
        self.check_class_required_fields_prop_etc(
                        required_fields_list=['water_velocity'],
                        required_props_list=['status','water_velocity'],
                        requires3D=True)

    def initial_setup(self, **kwargs):
        si = self.shared_info
        info = self.info
        info['number_resupended'] = 0
        # add required field and particle property for resuspension
        si.classes['field_group_manager'].create_field('friction_velocity', 'derived_from_reader_field',   {'class_name':self.params['friction_velocity_field_class_name']},
                                                       crumbs='initializing resuspension class ')
        si.classes['particle_group_manager'].create_particle_property('friction_velocity','from_fields', {}, crumbs='initializing resuspension class friction velocity')

    from oceantracker.fields.friction_velocity import FrictionVelocity
    def select_particles_to_resupend(self,critical_friction_velocity, groupe):
        # compare to single critical value
        # todo add comparison to  particles critical value from distribution, add new particle property to hold  individual critical values
        si = self.shared_info
        part_prop = si.classes['particle_properties']

        in_group= part_prop['IDrelease_group'].compare_all_to_a_value('eq',groupe,out=self.get_partID_buffer('B1'))

        on_bottom = part_prop['status'].find_subset_where(in_group,'eq', si.particle_status_flags['on_bottom'], out = self.get_partID_subset_buffer('B1'))

        # compare to critical friction velocity
        resupend = part_prop['friction_velocity'].find_subset_where(on_bottom, 'gteq',critical_friction_velocity, out=self.get_partID_subset_buffer('B1'))
        return resupend


    # all particles checked to see if they need status changing
    def update(self,time_sec, active):
        # do resupension
        #todo move 'resuspension_factor' calc to initialize() when substeping removed

        si= self.shared_info
        info = self.info
        info['resuspension_factor']= 2.0*0.4*si.z0*si.solver_info['model_time_step']/(1. - 2./np.pi)
        info['min_resuspension_jump']  = np.min(np.sqrt(info['resuspension_factor']*
            np.asarray(self.params['critical_friction_velocity'])))

        # redsuspend those on bottom and friction velocity exceeds critical value
        part_prop = si.classes['particle_properties']
        groups=list(part_prop['IDrelease_group'].data[active])

        for group in np.unique(groups):
      
            resupend = self.select_particles_to_resupend(self.params['critical_friction_velocity'][group],
                group)

            self.resuspension_jump(part_prop['friction_velocity'].data, self.info['resuspension_factor'], part_prop['x'].data, resupend)

            #  dont adjust resupension distance for terminal velocity,
            #  Lynch (Particles in the Ocean Book, says dont adjust as a fall velocity  affects prior that particle resuspends)

            # any z out of bounds will  be fixed by find_depth cell at start of next time step
            self.info['number_resupended'] += resupend.shape[0]
            part_prop['status'].set_values(si.particle_status_flags['moving'], resupend)


    @staticmethod
    @njit
    def resuspension_jump(friction_velocity, resuspension_factor, x, sel):
        # add entrainment jump up to particle z, Book: Lynch(2015) book, Particles in the coastal ocean  eq 9.26 and 9.28
        for n in sel:
            x[n, 2] += np.sqrt(resuspension_factor*friction_velocity[n])*np.abs(np.random.randn())

