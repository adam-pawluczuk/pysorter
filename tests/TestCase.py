# coding=utf-8

class TestCase(object):

    def test_sort_imports(self):
        source = (
            u'import logging\n'
            u'from security import login_required\n'
            u'from services import vehicle_service\n'
            u'from services import company_service\n'
            u'from models.commission import Commission\n'
            u'from bl_services import estimates_service\n'
            u'from forms.errors import FormValidationError\n'
            u'from controllers.estimates.add import AddEstimateHandler\n'
        )
        print source

