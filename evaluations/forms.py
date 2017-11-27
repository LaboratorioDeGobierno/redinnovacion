# -*- coding: utf-8 -*-
#
# models
from evaluations.models import EventEvaluation

# forms
from base.forms import BaseModelForm


class EventEvaluationForm(BaseModelForm):
    class Meta:
        model = EventEvaluation
        exclude = ('user', 'event', 'activity')

        labels = {
            'satisfaction': u'1. En relación al encuentro temático, ¿cuál es tu nivel de satisfacción general?',
            'usefulness': u'2. A tu juicio, ¿qué tan útil fue la jornada para conectar motivaciones en torno a la temática?',
            'clear_topics': '3. ¿Cuán claros fueron los facilitadores para poder explicar los contenidos del taller?',
        }
