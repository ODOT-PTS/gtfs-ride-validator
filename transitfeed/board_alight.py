from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util

class Board_alight(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['stop_id']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'trip_id',
                                         'boardings',
                                         'alightings',
                                         'bike_boardings',
                                         'bike_alightings',
                                         'ramp_boardings',
                                         'ramp_alightings',
                                         'board_date',
                                         'board_time',
                                         'current_load',
                                         'source']
  _TABLE_NAME = "board_alight"

  def __init__(self,name=None,stop_id = None,trip_id = None,boardings=None,alightings=None,bike_boardings=None,
              bike_alightings=None,ramp_boardings=None,ramp_alightings=None,board_date=None,
              board_time=None,current_load=None,source=None,field_dict=None,**kwargs):
    self._schedule = None

    if not field_dict:
      if stop_id:
        kwargs['stop_id'] = stop_id
      if trip_id:
        kwargs['trip_id'] = trip_id
      if boardings:
        kwargs['boardings'] = boardings
      if alightings:
        kwargs['alightings'] = alightings
      if bike_boardings:
        kwargs['bike_boardings'] = bike_boardings
      if bike_alightings:
        kwargs['bike_alightings'] = bike_alightings
      if ramp_boardings:
        kwargs['ramp_boardings'] = ramp_boardings
      if ramp_alightings:
        kwargs['ramp_alightings'] = ramp_alightings
      if board_date:
        kwargs['board_date'] = board_date
      if board_time:
        kwargs['board_time'] = board_time
      if current_load:
        kwargs['current_load'] = current_load
      if source:
        kwargs['source'] = source
      field_dict = kwargs
    self.__dict__.update(field_dict)

  #def validateStopID(self,problems):
    #return not util.ValidateID(self.stop_id, 'stop_id', problems)

  def ValidateSId(self, problems):
    if util.IsEmpty(self.stop_id):
      problems.MissingValue("stop_id")

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
    self.Validate(problems)

  def AddToSchedule(self, schedule, problems):
    schedule.AddBoardAlightObject(self, problems)

  