from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase

class Ridership(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['ridership_count']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'ridership_start_date',
                                         'ridership_end_date',
                                         'ridership_start_time',
                                         'ridership_end_time',
                                         'route_id',
                                         'trip_id']
  _TABLE_NAME = "ridership"

  def __init__(self,name=None,ridership_count = None,ridership_start_date = None,ridership_end_date=None,ridership_start_time=None,
    ridership_end_time=None,route_id=None,trip_id=None,field_dict=None,**kwargs):
    self._schedule = None

    if not field_dict:
      if ridership_count:
        kwargs['ridership_count'] = ridership_count
      if ridership_start_date:
        kwargs['ridership_start_date'] = ridership_start_date
      if ridership_end_date:
        kwargs['ridership_end_date'] = ridership_end_date
      if ridership_start_time:
        kwargs['ridership_start_time'] = ridership_start_time
      if ridership_end_time:
        kwargs['ridership_end_time'] = ridership_end_time
      if route_id:
        kwargs['route_id'] = route_id
      if trip_id:
        kwargs['trip_id'] = trip_id
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