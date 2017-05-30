from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase

class Rider_trip(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['rider_id']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'trip_id',
                                         'boarding_stop_id',
                                         'alighting_stop_id',
                                         'boarding_time',
                                         'boarding_date',
                                         'alighting_time',
                                         'alighting_date',
                                         'rider_type',
                                         'rider_type_description',
                                         'fare_paid',
                                         'fare_method',
                                         'accompanying_device',
                                         'transfer_status']
  _TABLE_NAME = "rider_trip"

  def __init__(self,name=None,rider_id = None,trip_id = None,boarding_stop_id=None,alighting_stop_id=None,boarding_time=None,
    boarding_date=None,alighting_time=None,alighting_date=None,rider_type=None,rider_type_description=None,fare_paid=None,
    fare_method=None,accompanying_device=None,transfer_status=None,field_dict=None,**kwargs):
    self._schedule = None

    if not field_dict:
      if rider_id:
        kwargs['rider_id'] = rider_id
      if trip_id:
        kwargs['trip_id'] = trip_id
      if boarding_stop_id:
        kwargs['boarding_stop_id'] = boarding_stop_id
      if alighting_stop_id:
        kwargs['alighting_stop_id'] = alighting_stop_id
      if boarding_time:
        kwargs['boarding_time'] = boarding_time
      if alighting_time:
        kwargs['alighting_time'] = alighting_time
      if alighting_date:
        kwargs['alighting_date'] = alighting_date
      if rider_type:
        kwargs['rider_type'] = rider_type
      if rider_type_description:
        kwargs['rider_type_description'] = rider_type_description
      if fare_paid:
        kwargs['fare_paid'] = fare_paid
      if fare_method:
        kwargs['fare_method'] = fare_method
      if accompanying_device:
        kwargs['accompanying_device'] = accompanying_device
      if transfer_status:
        kwargs['transfer_status'] = transfer_status
      field_dict = kwargs
    self.__dict__.update(field_dict)

  #def validateStopID(self,problems):
    #return not util.ValidateID(self.stop_id, 'stop_id', problems)


  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    #found_problem = self.ValidateSId(problems)

    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    return