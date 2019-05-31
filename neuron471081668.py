'''
Defines a class, Neuron471081668, of neurons from Allen Brain Institute's model 471081668

A demo is available by running:

    python -i mosinit.py
'''
class Neuron471081668:
    def __init__(self, name="Neuron471081668", x=0, y=0, z=0):
        '''Instantiate Neuron471081668.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron471081668_instance is used instead
        '''
        
        # load the morphology
        from load_swc import load_swc
        load_swc('Pvalb-IRES-Cre_Ai14_IVSCC_-170929.04.01_396782215_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
        
        self._name = name
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron471081668_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im_v2', u'K_T', u'Kd', u'Kv2like', u'Kv3_1', u'NaV', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 10.0
            sec.e_pas = -84.2060089111
        
        for sec in self.axon:
            sec.cm = 4.67
            sec.g_pas = 0.000551105698649
        for sec in self.dend:
            sec.cm = 4.67
            sec.g_pas = 3.74146529165e-05
        for sec in self.soma:
            sec.cm = 4.67
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Ih = 0.00186174
            sec.gbar_NaV = 0.154786
            sec.gbar_Kd = 0
            sec.gbar_Kv2like = 0.000537784
            sec.gbar_Kv3_1 = 0.740282
            sec.gbar_K_T = 0.029341
            sec.gbar_Im_v2 = 0.000102816
            sec.gbar_SK = 0.0387274
            sec.gbar_Ca_HVA = 5.73808e-05
            sec.gbar_Ca_LVA = 0.00850799
            sec.gamma_CaDynamics = 0.00154199
            sec.decay_CaDynamics = 34.6782
            sec.g_pas = 0.000472007
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

