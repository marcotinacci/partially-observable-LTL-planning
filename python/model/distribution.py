#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

# >>> code

class Distribution:
	"""
	A discrete probability distribution over a given domain set.
	:support: is a dictionary mapping ids to names
	:distr: is a dictionary that maps states ids to their 
		probabilities, elements with null probability are not
		included in the dictionary
	"""
	
	def __init__(self, domain, pdf):
		""" 
		Distribution constructor. 
			:param domain: domain set of the distribution
			:param pdf: probability density function 
		"""
		self.support = dict(enumerate(domain))
		self.distr = dict()
		for i,e in self.support.iteritems():
			pr = pdf(e,domain)
			# do not insert elements with null probability
			if float(pr) != 0.:
				self.distr[i] = pdf(e,domain)

#	def __checkSumOne(self):
#		""" Check if the distribution has sum 1 """
#		return True if float(sum(self.distr.values())) == 1.0 \
#			else False

	def equals(self, d):
		""" Compare with a distribution d """
		if self == d:
			return True
		eq = True
		for k,v in self.distr.iteritems():
			if k in d.distr:
				if d.distr[k] != v:
					eq = False
					break
			else:
				eq = False
				break
		return eq

	@staticmethod
	def normalize(distribution):
		""" Distribution normalization """
		total = sum(distribution.values())
		for k,v in distribution.iteritems():
			distribution[k] = v / total

	@staticmethod
	def customPdf(e,pdf):
		""" Custom pdf """
		if e in pdf:
			return pdf[e]
		else:
			return 0.0

	@staticmethod
	def restrictedUniformPdf(e,domain,subset):
		""" 
		Standard pdf to model uniform distributions 
		over a subset of the domain 
		"""
		if not subset <= domain:
			raise Exception('The restriction set is not a subset of the domain')
		return 1./len(subset) if e in subset else 0.

	@staticmethod
	def uniformPdf(e,domain):
		""" Standard pdf to model uniform distributions """
		return Distribution.restrictedUniformPdf(e,domain,domain)

	@staticmethod
	def diracPfd(e,domain,e1):
		""" Dirac distribution """
		return Distribution.restrictedUniformPdf(e,domain,{e1})

	def __str__(self):
		ret = "id, element, probability\n"
		for i,e in self.support.iteritems():
			if i in self.distr:
				ret = ret + str(i) + ', ' + str(e) + ', ' + str(self.distr[i]) + '\n'
		return ret

	def __str__(self):
		ret = "id, element, probability\n"
		for i,e in self.support.iteritems():
			if i in self.distr:
				ret = ret + str(i) + ', ' + str(e) + ', ' + str(self.distr[i]) + '\n'
		return ret

# >>> main test

if __name__ == '__main__':
	dom = {'a','b','c','d'}
	print dom
	distr = Distribution(dom,Distribution.uniformPdf)
	#distr = Distribution(dom,lambda el,dom: Distribution.restrictedUniformPdf(el,dom,{'a','b'}))
	#distr = Distribution(dom,lambda el,dom: Distribution.diracPfd(el,dom,'b'))
	print distr

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"