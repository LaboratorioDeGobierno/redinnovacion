# -*- coding: utf-8 -*-


class InstitutionKinds(object):
    MINISTRY = 1
    SERVICES = 2
    PUBLIC_COMPANIES = 3
    UNIVERSITY = 4
    OTHER = 5

    choices = (
        (MINISTRY, 'Ministerio'),
        (SERVICES, 'Servicios'),
        (PUBLIC_COMPANIES, u'Empresas públicas'),
        (UNIVERSITY, 'Universidades'),
        (OTHER, 'Otro'),
    )

    choices_dict = dict(choices)
