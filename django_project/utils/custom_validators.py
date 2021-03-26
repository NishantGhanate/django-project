import re
import datetime
from cerberus import Validator

from django_project.common import (
    messages as glob_messages
)

class CustomValidator(Validator):
    
    #validate application ID
    def _validate_isnumeric(self,isinteger,field,value):
        """
        {'type':'boolean'}
        """
        if isinteger:
            try:
                number = int(value)
            except Exception:
                self._error(field,glob_messages.INTEGER_ONLY)

    def _validate_isfloat(self,isfloat,field,value):
        """
        {'type':'boolean'}
        """
        try:
            number = float(value)
        except Exception:
            self._error(field,glob_messages.FLOAT_ONLY)

    #validate Student Id
    def _validate_isalphanumeric(self,isalphanumeric,field,value):
        """
        {'type':'boolean'}
        """
        if isalphanumeric:
            zeroes = re.match('^0+$',value)
            if zeroes:
                self._error(
                    field,glob_messages.INVALID_STUDENT_ID)

            alphanumeric_id = re.match('^[a-zA-Z0-9_]+$',value)

            if not alphanumeric_id:
                self._error(
                    field,glob_messages.SPECIAL_CHARS_NOT_ALLOWED)

    #validate Mobile
    def _validate_ismobile(self,ismobile,field,value):
        """
        {'type':'boolean'}
        """
        if ismobile:
            mobile = re.match('^[6-9]\d{9}$', value)
            if (not mobile or
                not len(value) == 10
            ):
                self._error(field,glob_messages.INVALID_MOBILE_NUMBER)
                
   
    # Validate Email
    def _validate_isemail(self, isemail, field, value):
        """
            {'type': 'boolean'}
         """

        if isemail:
            email = re.match(
                '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                value
            )

            if not email:
                self._error(field, glob_messages.INVALID_EMAIL)

   

    


   

   