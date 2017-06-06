from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util


class Board_alight(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['stop_id','trip_id','boardings']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
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

  def ValidateBoardingsHasValidValue(self, problems):
    if self.boardings is not None:
      try:
        if not isinstance(self.boardings, int):
          self.boardings = util.NonNegIntStringToInt(self.boardings, problems)
      except (TypeError, ValueError):
        problems.InvalidValue('boardings', self.boardings)

  def ValidateAlightingsHasValidValue(self, problems):
    if self.alightings is not None:
      try:
        if not isinstance(self.alightings, int):
          self.alightings = util.NonNegIntStringToInt(self.alightings, problems)
      except (TypeError, ValueError):
        problems.InvalidValue('alightings', self.alightings)

  def ValidateBikeBoardingsHasValidValue(self, problems):
    if self.bike_boardings is not None:
      try:
        if not isinstance(self.bike_boardings, int):
          self.bike_boardings = util.NonNegIntStringToInt(self.bike_boardings, problems)
      except (TypeError, ValueError):
        problems.InvalidValue('bike_boardings', self.bike_boardings)

  def ValidateBikeAlightingsHasValidValue(self, problems):
    if self.bike_alightings is not None:
      try:
        if not isinstance(self.bike_alightings, int):
          self.bike_alightings = util.NonNegIntStringToInt(self.bike_alightings, problems)
      except (TypeError, ValueError):
        problems.InvalidValue('bike_alightings', self.bike_alightings)
  
  def ValidateRampBoardingsHasValidValue(self, problems):
    if self.ramp_boardings is not None:
      try:
        if not isinstance(self.ramp_boardings, int):
          self.ramp_boardings = util.NonNegIntStringToInt(self.ramp_boardings, problems)
      except (TypeError, ValueError):
        problems.InvalidValue('ramp_boardings', self.ramp_boardings)

  def ValidateRampAlightingsHasValidValue(self, problems):
    if self.ramp_alightings is not None:
      try:
        if not isinstance(self.ramp_alightings, int):
          self.ramp_alightings = util.NonNegIntStringToInt(self.ramp_alightings, problems)
      except (TypeError, ValueError):
        problems.InvalidValue('ramp_alightings', self.ramp_alightings)

  def validateSource(self,problems):
    if self.source is not None:
      if self.source != 0 or 1 or 2 or 3 or 4:
        problems.InvalidValue('source', self.source)

  def validateCurrentLoad(self,problems):
    if self.current_load is not None:
      if self.current_load  < 0 or self.current_load>100:
        problems.InvalidValue('current_load', self.current_load)

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.ValidateBoardingsHasValidValue(problems)
    found_problem = self.ValidateAlightingsHasValidValue(problems)
    found_problem = self.ValidateBikeBoardingsHasValidValue(problems)
    found_problem = self.ValidateBikeAlightingsHasValidValue(problems)
    found_problem = self.ValidateRampBoardingsHasValidValue(problems)
    found_problem = self.ValidateRampAlightingsHasValidValue(problems)
    found_problem = self.validateSource(problems)
    found_problem = self.validateCurrentLoad(problems)


    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    self.Validate(problems)

  def AddToSchedule(self, schedule, problems):
    schedule.AddBoardAlightObject(self, problems)

  