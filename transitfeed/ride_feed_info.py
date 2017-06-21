from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util

class Ride_feed_info(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['ride_start_date']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'ride_end_date']
  _TABLE_NAME = "ride_feed_info"

  def __init__(self,name=None,ride_start_date = None,ride_end_date = None,field_dict=None,**kwargs):
    self._schedule = None

    if not field_dict:
      if ride_start_date:
        kwargs['ride_start_date'] = ride_start_date
      if ride_end_date:
        kwargs['ride_end_date'] = ride_end_date
      field_dict = kwargs
    self.__dict__.update(field_dict)

  #def validateStopID(self,problems):
    #return not util.ValidateID(self.stop_id, 'stop_id', problems)

  def getRideStartDate(self):
    
    return self.ride_start_date

  def getRideEndDate(self):
    
    return self.ride_end_date

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

  def AddToSchedule(self, schedule, problems):
    schedule.AddRideTimes(self, self.ride_start_date, self.ride_end_date,problems )