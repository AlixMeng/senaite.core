# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

from AccessControl import ClassSecurityInfo
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.fields import DateTimeField
from bika.lims.browser.fields import UIDReferenceField
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.config import PROJECTNAME
from bika.lims.content.bikaschema import BikaSchema
from bika.lims.interfaces import IARReport
from plone.app.blob.field import BlobField
from Products.Archetypes import atapi
from Products.Archetypes.public import BaseFolder
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.references import HoldingReference
from Products.ATExtensions.ateapi import RecordsField
from zope.interface import implements


schema = BikaSchema.copy() + Schema((
    UIDReferenceField(
        "AnalysisRequest",
        allowed_types=("AnalysisRequest",),
        referenceClass=HoldingReference,
        required=1,
    ),
    BlobField(
        "Pdf",),
    StringField(
        "SMS",),
    RecordsField(
        "Recipients",
        type="recipients",
        subfields=(
            "UID",
            "Username",
            "Fullname",
            "EmailAddress",
            "PublicationModes"
        ),
    ),
    DateTimeField(
        "DatePrinted",
        mode="rw",
        widget=DateTimeWidget(
            label=_("Date Printed"),
            visible={
                "edit": "visible",
                "view": "visible",
            }
        ),
    ),
))

schema['id'].required = False
schema['title'].required = False


class ARReport(BaseFolder):
    """An AnalysisRequest report, containing the report itself in pdf and html
       format. It includes information about the date when was published, from
       whom, the report recipients (and their emails) and the publication mode
    """
    implements(IARReport)

    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)


atapi.registerType(ARReport, PROJECTNAME)
