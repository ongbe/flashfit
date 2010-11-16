# -*- coding: utf-8 -*- (Python reads this)
from PyQt4 import QtCore, QtGui

class TextItem:
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def text():
        raise NotImplemented

class Name(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "Name")

    def text():
        return u"name: %s" % QtCore.QFileInfo(self.data.fileName).completeBaseName()

class MeasureDate(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "Measure Date")

    def text():
        return u"measured: %s" % self.data.fileCreated.toString("yyyy-MM-dd hh:mm")

class Model(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "Model")

    def text():
        if self.data.fitdata.modelName != None:
            return u"model: %s" % self.data.fitdata.modelName
        else:
            return ""

class A0(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "A0")

    def text():
        if len(self.data.fitdata.values) > 0:
            text += u"A0 = %.4e" % self.data.fitdata.values[0]
        else:
            return ""

class Ainf(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "Ainf")

    def text():
        if self.data.fitdata.ainf != None:
            return u"Ainf = %.4e" % self.data.fitdata.ainf
        else:
            return ""

class Amax(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "Amax")

    def text():
        if self.data.maxAbsorbance != None:
            return u"Amax = %.4e" % self.data.maxAbsorbance

class RateConstants(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "Rate Constants k(n)")

    def text():
        text = u""
        for i in range(0, len(self.data.fitdata.parameters)):
            prec = variables.legendDisplayedPrecision.value()
            template = u"k(%%d) = %%.%de ± %%.%de" % (prec, prec)
            text += template % (i + 1, self.data.fitdata.parameters[i].value, self.data.fitdata.parameters[i].sigma)
        return text

class A0minusAinf(TextItem):
    def __init__(self, data):
        TextItem.__init__(self, data, "A0 - Ainf")

    def text():
        text = u""
        for i in range(0, len(self.data.fitdata.parameters)):
            text += u"A0 - Ainf(%d) = %.4e" % (i + 1, self.data.fitdata.parameters[i].a0minusAinf)
        return text

class List:
    def __init__(self, data):
        self.all = {}
        self.all[Name.__name__] = Name(data)
        self.all[MeasureDate.__name__] = MeasureDate(data)
        self.all[Model.__name__] = Model(data)
        self.all[A0.__name__] = A0(data)
        self.all[Ainf.__name__] = Ainf(data)
        self.all[Amax.__name__] = Amax(data)
        self.all[RateConstants.__name__] = RateConstants(data)
        self.all[A0minusAinf.__name__] = A0minusAinf(data)

    def available(self, visible):
        """
        Parameter visible is a list of class names.
        """
        result = self.all.keys()
        for item in visible:
            result.remove(item)
        return result