from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase

class Ridership(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['ridership_count','ridership_start_date','ridership_end_date']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'ridership_start_time',
                                         'ridership_end_time',
                                         'route_id',
                                         'trip_id',
                                         'direction_id',
                                         'stop_id']
  _TABLE_NAME = "ridership"

  def __init__(self,name=None,ridership_count = None,ridership_start_date = None,ridership_end_date=None,ridership_start_time=None,
    ridership_end_time=None,route_id=None,trip_id=None,direction_id=None,stop_id=None,field_dict=None,**kwargs):
    self._schedule = None
    self.boardTimeMin = None
    self.boardTimeMax = None

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
      if direction_id:
        kwargs['direction_id'] = direction_id
      if stop_id:
        kwargs['stop_id'] = stop_id
      field_dict = kwargs
    self.__dict__.update(field_dict)

  def validateRidershipCount(self,problems):
    if self.ridership_count is not None:
      if isInstance(self.ridership_count,int) == False or self.transfer_status<1:
        problems.InvalidValue('ridership_count', self.ridership_count)

  def validateRidershipStartDate(self,problems):
    if self.ridership_start_date is not None:
      date = util.DateStringToDateObject(self.ridership_start_date)
      dateMin = util.DateStringToDateObject(self.boardTimeMin)
      dateMax = util.DateStringToDateObject(self.boardTimeMax)
      accept = util.CheckIfInBetweenDates(dateMin,dateMax,date)
      if accept == 0:
        problems.DateOutsideValidRangeGTFSRide('ridership_start_date', int(self.ridership_start_date),int(self.boardTimeMin),int(self.boardTimeMax))

  def validateRidershipEndDate(self,problems):
    if self.ridership_end_date is not None:
      date = util.DateStringToDateObject(self.ridership_end_date)
      dateMin = util.DateStringToDateObject(self.boardTimeMin)
      dateMax = util.DateStringToDateObject(self.boardTimeMax)
      accept = util.CheckIfInBetweenDates(dateMin,dateMax,date)
      if accept == 0:
        problems.DateOutsideValidRangeGTFSRide('ridership_end_date', int(self.ridership_end_date),int(self.boardTimeMin),int(self.boardTimeMax))

  def validateRidershipStartTimeFormat(self,problems):
    if self.ridership_start_time is not None:
      accept = util.checkInProperTimeFormat(self.ridership_start_time)
      if accept == 0:
        problems.UnknownTimeFormat('ridership_start_time',self.ridership_start_time)

  def validateRidershipEndTimeFormat(self,problems):
    if self.ridership_end_time is not None:
      accept = util.checkInProperTimeFormat(self.ridership_end_time)
      if accept == 0:
        problems.UnknownTimeFormat('ridership_end_time',self.ridership_end_time)

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.validateRidershipCount(problems)
    found_problem = self.validateRidershipStartDate(problems)
    found_problem = self.validateRidershipEndDate(problems)
    found_problem = self.validateRidershipStartTimeFormat(problems)
    found_problem = self.validateRidershipEndTimeFormat(problems)



    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    return