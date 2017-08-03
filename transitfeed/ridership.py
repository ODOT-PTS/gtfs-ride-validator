from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util

class Ridership(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['total_boardings','total_alightings','ridership_start_date','ridership_end_date']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                         'ridership_start_time',
                                         'ridership_end_time',
                                         'service_id',
                                         'monday',
                                         'tuesday',
                                         'wednesday',
                                         'thursday',
                                         'friday',
                                         'saturday',
                                         'sunday',
                                         'agency_id',
                                         'route_id',
                                         'trip_id',
                                         'direction_id',
                                         'stop_id']
  _TABLE_NAME = "ridership"

  def __init__(self,name=None,total_boardings = None,total_alightings = None,ridership_start_date = None,ridership_end_date=None,ridership_start_time=None,
    ridership_end_time=None,monday = None,tuesday = None,wednesday = None,thursday = None, friday = None, saturday = None, sunday = None,
    service_id = None, agency_id = None,route_id=None,trip_id=None,direction_id=None,stop_id=None,field_dict=None,**kwargs):
    self._schedule = None

    if not field_dict:
      if total_boardings:
        kwargs['total_boardings'] = total_boardings
      if total_alightings:
        kwargs['total_alightings'] = total_alightings
      if ridership_start_date:
        kwargs['ridership_start_date'] = ridership_start_date
      if ridership_end_date:
        kwargs['ridership_end_date'] = ridership_end_date
      if ridership_start_time:
        kwargs['ridership_start_time'] = ridership_start_time
      if ridership_end_time:
        kwargs['ridership_end_time'] = ridership_end_time
      if monday:
        kwargs['monday'] = monday
      if tuesday:
        kwargs['tuesday'] = tuesday
      if wednesday:
        kwargs['wednesday'] = wednesday
      if thursday:
        kwargs['thursday'] = thursday
      if friday:
        kwargs['friday'] = friday
      if saturday:
        kwargs['saturday'] = saturday
      if sunday:
        kwargs['sunday'] = sunday
      if service_id:
        kwargs['service_id'] = service_id
      if agency_id:
        kwargs['agency_id'] = agency_id
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

  def validateTotalBoardings(self,problems):
    try:
      self.total_boardings = int(self.total_boardings)
    except (ValueError, TypeError):
      problems.InvalidValue('total_boardings', self.total_boardings,
          'Value must be non negative integer')
      del self.total_boardings
      return
    if self.total_boardings < 0:
      problems.InvalidValue('total_boardings', self.total_boardings,
          'Value must be non negative integer')

  def validateTotalAlightings(self,problems):
    try:
      self.total_alightings = int(self.total_alightings)
    except (ValueError, TypeError):
      problems.InvalidValue('total_alightings', self.total_alightings,
          'Value must be non negative integer')
      del self.total_alightings
      return
    if self.total_alightings < 0:
      problems.InvalidValue('total_alightings', self.total_alightings,
          'Value must be non negative integer')

  def validateRidershipStartDate(self,problems):
    valid_date = util.ValidateDate(self.ridership_start_date,
                                               'ridership_start_date', problems)
    if self._schedule.validRideDates == 0:
      return
    if valid_date:
      if self.ridership_start_date > self._schedule.ride_feed_date[1] or self.ridership_start_date < self._schedule.ride_feed_date[0]:
        problems.InvalidValue('ridership_start_date',self.ridership_start_date,'Service date does not fall in valid range')

  def validateRidershipEndDate(self,problems):
    valid_date = util.ValidateDate(self.ridership_end_date,
                                               'ridership_end_date', problems)
    if self._schedule.validRideDates == 0:
      return
    if valid_date:
      if self.ridership_end_date > self._schedule.ride_feed_date[1] or self.ridership_end_date < self._schedule.ride_feed_date[0]:
        problems.InvalidValue('ridership_end_date',self.ridership_end_date,'Service date does not fall in valid range')
  
  def validateRidershipStartTime(self,problems):
    if util.IsEmpty(self.ridership_start_time):
      self.ridership_start_time = 0
      return
    accept = util.checkInProperTimeFormat(self.ridership_start_time)
    if accept == 0:
      problems.UnknownTimeFormat('ridership_start_time',self.ridership_start_time)

  def validateRidershipEndTime(self,problems):
    if util.IsEmpty(self.ridership_end_time):
      self.ridership_end_time = 0
      return
    accept = util.checkInProperTimeFormat(self.ridership_end_time)
    if accept == 0:
      problems.UnknownTimeFormat('ridership_end_time',self.ridership_end_time)

  def validateServiceID(self,problems):
    if util.IsEmpty(self.service_id):
      self.service_id = 0
      return
    if self.service_id not in self._schedule.service_periods.keys():
      problems.InvalidValue('service_id',self.stop_id,'Did not find a matching service_id')

  def validateAgencyID(self,problems):
    if util.IsEmpty(self.agency_id):
        return
    if self.agency_id not in self._schedule._agencies.keys():
      problems.InvalidValue('agency_id',self.agency_id,'Did not find a matching agency_id in agencies.txt')

  def validateDirectionID(self,problems):
    # print("Checking direction ids")
    # print(self._schedule.direction_ids)
    if util.IsEmpty(self.direction_id):
        return
    if self.direction_id not in self._schedule.direction_ids:
      problems.InvalidValue('direction_id',self.direction_id,'Did not find a matching direction_id in trips.txt')

  def validateRouteID(self,problems):
    if util.IsEmpty(self.route_id):
      return
    if self.route_id not in self._schedule.routes.keys():
      problems.InvalidValue('route_id',self.route_id,'Did not find a matching route_id in route.txt')

  def validateTripID(self,problems):
    if util.IsEmpty(self.trip_id):
        return
    if self.trip_id not in self._schedule.trips.keys():
      problems.InvalidValue('trip_id',self.trip_id,'Did not find a matching trip_id in trips.txt')

  def validateStopID(self,problems):
    if util.IsEmpty(self.stop_id):
        return
    if self.stop_id not in self._schedule.stops.keys():
      problems.InvalidValue('stop_id',self.stop_id,'Did not find a matching stop_id in stops.txt')

  def validateDates(self,problems):
    if util.IsEmpty(self.monday) != True:
      try:
        self.monday = int(self.monday)
      except (ValueError, TypeError):
        problems.InvalidValue('monday', self.monday,
            'Value must be 0 or 1')
        del self.monday
        return
      if self.monday not in (0, 1):
        problems.InvalidValue('monday', self.monday,
            'Value must be 0 or 1')
    if util.IsEmpty(self.tuesday) != True:
      try:
        self.tuesday = int(self.tuesday)
      except (ValueError, TypeError):
        problems.InvalidValue('tuesday', self.tuesday,
            'Value must be 0 or 1')
        del self.tuesday
        return
      if self.tuesday not in (0, 1):
        problems.InvalidValue('tuesday', self.tuesday,
            'Value must be 0 or 1')
    if util.IsEmpty(self.wednesday) != True:
      try:
        self.wednesday = int(self.wednesday)
      except (ValueError, TypeError):
        problems.InvalidValue('wednesday', self.wednesday,
            'Value must be 0 or 1')
        del self.wednesday
        return
      if self.wednesday not in (0, 1):
        problems.InvalidValue('wednesday', self.wednesday,
            'Value must be 0 or 1')
    if util.IsEmpty(self.thursday) != True:
      try:
        self.thursday = int(self.thursday)
      except (ValueError, TypeError):
        problems.InvalidValue('thursday', self.thursday,
            'Value must be 0 or 1')
        del self.thursday
        return
      if self.thursday not in (0, 1):
        problems.InvalidValue('thursday', self.thursday,
            'Value must be 0 or 1')
    if util.IsEmpty(self.friday) != True:
      try:
        self.friday = int(self.friday)
      except (ValueError, TypeError):
        problems.InvalidValue('friday', self.friday,
            'Value must be 0 or 1')
        del self.friday
        return
      if self.friday not in (0, 1):
        problems.InvalidValue('friday', self.friday,
            'Value must be 0 or 1')
    if util.IsEmpty(self.saturday) != True:
      try:
        self.saturday = int(self.saturday)
      except (ValueError, TypeError):
        problems.InvalidValue('saturday', self.saturday,
            'Value must be 0 or 1')
        del self.saturday
        return
      if self.saturday not in (0, 1):
        problems.InvalidValue('saturday', self.saturday,
            'Value must be 0 or 1')
    if util.IsEmpty(self.sunday) != True:
      try:
        self.sunday = int(self.sunday)
      except (ValueError, TypeError):
        problems.InvalidValue('sunday', self.sunday,
            'Value must be 0 or 1')
        del self.sunday
        return
      if self.sunday not in (0, 1):
        problems.InvalidValue('sunday', self.sunday,
            'Value must be 0 or 1')




  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.validateTotalBoardings(problems)
    found_problem = self.validateTotalAlightings(problems)
    found_problem = self.validateRidershipStartDate(problems)
    found_problem = self.validateRidershipEndDate(problems)
    found_problem = self.validateRidershipStartTime(problems)
    found_problem = self.validateRidershipEndTime(problems)
    found_problem = self.validateServiceID(problems)
    found_problem = self.validateAgencyID(problems)
    found_problem = self.validateRouteID(problems)
    found_problem = self.validateDirectionID(problems)
    found_problem = self.validateTripID(problems)
    found_problem = self.validateStopID(problems)
    found_problem = self.validateDates(problems)

    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    self.Validate(problems)
    return