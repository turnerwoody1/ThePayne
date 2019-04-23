import numpy as np
from numpy.polynomial.chebyshev import chebval
from numpy.polynomial.chebyshev import Chebyshev as T
from scipy.interpolate import interp1d
from scipy import constants
speedoflight = constants.c / 1000.0
from scipy.optimize import minimize_scalar, minimize, brute, basinhopping, differential_evolution, fmin

from ..utils.smoothing import smoothspec

def polycalc(coef,inwave):
	# define obs wave on normalized scale
	x = inwave - inwave.min()
	x = 2.0*(x/x.max())-1.0
	# build poly coef
	# c = np.insert(coef[1:],0,0)
	poly = chebval(x,coef)
	# epoly = np.exp(coef[0]+poly)
	# epoly = coef[0]+poly
	return poly

def airtovacuum(inwave):
	"""
		Using the relationship from Ciddor (1996) and transcribed in Shetrone et al. 2015
	"""
	a = 0.0
	b1 = 5.792105E-2
	b2 = 1.67917E-3
	c1 = 238.0185
	c2 = 57.362

	deltawave = a + (b1/(c1-(1.0/inwave**2.0))) + (b2/(c2-(1.0/inwave**2.0)))

	return inwave*(deltawave+1)

class RVcalc(object):
	def __init__(self, **kwargs):
		super(RVcalc, self).__init__()
		
		self.wave = kwargs.get('inwave',[])
		self.flux = kwargs.get('influx',[])
		self.eflux = kwargs.get('einflux',[])
		self.modflux = kwargs.get('modflux',[])
		self.modwave = kwargs.get('modwave',[])

	def __call__(self):
		init_vrad = 0.0

		args = [self.wave,self.flux,self.eflux,self.modflux,self.modwave]

		outfn = brute(
			self.chisq_rv,
			# ranges=(slice(-1000,1000,1.0),),
			ranges=((-1000,1000),),
			Ns=10000,
			)
		return outfn

		# return [minimize(
		# 	self.chisq_rv,
		# 	init_vrad,
		# 	method='Nelder-Mead',
		# 	tol=10E-10,
		# 	options={'maxiter':1E6}
		# 	).x]

	def chisq_rv(self,rv):
		wave = self.wave
		flux = self.flux
		eflux = self.eflux
		modflux = self.modflux
		modwave = self.modwave

		# adjust model to new rv
		modwave_i = modwave*(1.0+(rv/speedoflight))

		# interpolate ict back to wave so that chi-sq can be computed
		modflux_i = interp1d(modwave_i,modflux,kind='linear',bounds_error=False,fill_value=1.0)(wave)

		chisq = np.sum([((m-o)**2.0)/(s**2.0) for m,o,s in zip(
			modflux_i,flux,eflux)])
		return chisq

class BROADcalc(object):
	def __init__(self, **kwargs):
		super(BROADcalc, self).__init__()
		
		self.wave = kwargs.get('inwave',[])
		self.flux = kwargs.get('influx',[])
		self.eflux = kwargs.get('einflux',[])
		self.modflux = kwargs.get('modflux',[])
		self.modwave = kwargs.get('modwave',[])
		self.inputres = kwargs.get('inres',300000.0)

	def __call__(self):
		init_broad = 32000.0

		args = [self.wave,self.flux,self.eflux,self.modflux,self.modwave]

		outfn = brute(
			self.chisq_broad,
			ranges=((27000.0,35000.0),),
			# (slice(27000.0,39000.0,0.01),),
			Ns=1000,
			)
		return outfn

		# return [minimize(
		# 	self.chisq_broad,
		# 	init_broad,
		# 	method='Nelder-Mead',
		# 	tol=10E-10,
		# 	options={'maxiter':1E6}
		# 	).x]

	def chisq_broad(self,broad):
		wave = self.wave
		flux = self.flux
		eflux = self.eflux
		modflux = self.modflux
		modwave = self.modwave

		if broad < 0.0:
			return np.inf

		# adjust model to new brodening
		modflux_i = smoothspec(modwave,modflux,resolution=2.355*broad,
			outwave=modwave,smoothtype='R',fftsmooth=True,inres=self.inputres,
			)
		chisq = np.sum([((m-o)**2.0)/(s**2.0) for m,o,s in zip(
			modflux_i,flux,eflux)])
		return chisq



class PCcalc(object):
	def __init__(self, **kwargs):
		super(PCcalc, self).__init__()
		
		self.wave = kwargs.get('inwave',[])
		self.flux = kwargs.get('influx',[])
		self.eflux = kwargs.get('einflux',[])
		self.modflux = kwargs.get('modflux',[])
		self.modwave = kwargs.get('modwave',[])
		self.numpoly = kwargs.get('numpoly',4)

	def __call__(self):
		init_pc = [1.0] + [0.0 for _ in range(self.numpoly-1)]
		args = [self.wave,self.flux,self.eflux,self.modflux,self.modwave]

		return [minimize(
			self.chisq_pc,
			init_pc,
			method='Nelder-Mead',
			tol=10E-15,
			options={'maxiter':1E4}
			).x]

	def chisq_pc(self,pc):
		wave = self.wave
		flux = self.flux
		eflux = self.eflux
		modflux = self.modflux
		modwave = self.modwave

		polymod = polycalc(pc,wave)

		# interpolate ict back to wave so that chi-sq can be computed
		flux_i = flux / interp1d(modwave,modflux,kind='linear',bounds_error=False,fill_value=1.0)(wave)

		chisq = np.sum([((m-o)**2.0)/(s**2.0) for m,o,s in zip(
			polymod,flux_i,eflux)])
		return chisq

class SEDopt(object):
	def __init__(self, **kwargs):
		super(SEDopt, self).__init__()
		from Payne.predict.predictsed import FastPayneSEDPredict

		self.inputphot = kwargs.get('inputphot',{})
		self.fixedpars = kwargs.get('fixedpars',{})
		self.filterarray = list(self.inputphot.keys())
		if 'photANNpath' in self.filterarray:
			self.filterarray.remove('photANNpath')
		self.returnsed = kwargs.get('returnsed',False)


		self.fsed = FastPayneSEDPredict(
			usebands=self.filterarray,
			nnpath=self.inputphot['photANNpath'])

	def __call__(self):
		init_sed = [6000.0,0.0,3.0]
		output = [minimize(
			self.chisq_sed,
			init_sed,
			method='Nelder-Mead',
			tol=10E-15,
			options={'maxiter':1E4}
			).x]
		if self.returnsed:
			Teff = output[0][0]
			logTeff = np.log10(Teff)
			logg = self.fixedpars.get('logg',4.44)
			FeH  = output[0][1]
			aFe  = self.fixedpars.get('aFe',0.0)
			logA = output[0][2]
			Av   = self.fixedpars.get('Av',0.0)

			photpars = {'logt':logTeff,'logg':logg,'feh':FeH,'afe':aFe,'logA':logA,'av':Av}
			sed = self.fsed.sed(**photpars)
			sedmod = {ff_i:sed_i for sed_i,ff_i in zip(sed,self.filterarray)}			
			return output, sedmod
		else:
			return output


	def chisq_sed(self,pars):
		Teff = pars[0]
		logTeff = np.log10(Teff)
		logg = self.fixedpars.get('logg',4.44)
		FeH  = pars[1] #self.fixedpars.get('FeH',0.0)
		aFe  = self.fixedpars.get('aFe',0.0)
		logA = pars[2]
		Av   = self.fixedpars.get('Av',0.0)

		photpars = {'logt':logTeff,'logg':logg,'feh':FeH,'afe':aFe,'logA':logA,'av':Av}

		sed = self.fsed.sed(**photpars)
		sedmod = {ff_i:sed_i for sed_i,ff_i in zip(sed,self.filterarray)}

		chisq = np.sum(
				[((sedmod[kk]-self.inputphot[kk][0])**2.0)/(self.inputphot[kk][1]**2.0) 
				for kk in self.filterarray]
				)
		return chisq

