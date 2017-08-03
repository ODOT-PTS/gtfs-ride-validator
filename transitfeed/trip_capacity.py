from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase
import util
from loader import Loader
import gtfsfactory as gtfsfactory_module


class Trip_capacity(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = []
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
                                          'agency_id',
                                          'trip_id',
                                          'service_date',
                                          'vehicle_description',
                                          'seated_capacity',
                                          'standing_capacity',
                                          'wheelchair_capacity',
                                          'bike_capacity'
                                         ]
  _TABLE_NAME = "trip_capacity"

  def __init__(self,agency_id = None, trip_id = None, service_date = None, vehicle_description = None,
                seated_capacity = None, standing_capacity = None, wheelchair_capacity = None, bike_capacity = None, field_dict=None,**kwargs):
    self._schedule = None
    self.boardTimeMin = None
    self.boardTimeMax = None

    if not field_dict:
      if agency_id:
        kwargs['agency_id'] = agency_id
      if trip_id:
        kwargs['trip_id'] = trip_id
      if service_date:
        kwargs['service_date'] = service_date
      if vehicle_description:
        kwargs['vehicle_description'] = vehicle_description
      if seated_capacity:
        kwargs['seated_capacity'] = seated_capacity
      if standing_capacity:
        kwargs['standing_capacity'] = standing_capacity
      if wheelchair_capacity:
        kwargs['wheelchair_capacity'] = wheelchair_capacity
      if bike_capacity:
        kwargs['bike_capacity'] = bike_capacity

      field_dict = kwargs
    self.__dict__.update(field_dict)
  
  def validateServiceDate(self,problems):
    valid_date = util.ValidateDate(self.service_date,
                                               'service_date', problems)
    if self._schedule.validRideDates == 0:
      return
    if valid_date:
      if self.service_date > self._schedule.ride_feed_date[1] or self.service_date < self._schedule.ride_feed_date[0]:
        problems.InvalidValue('service_date',self.service_date,'Service date does not fall in valid range')

  def validateTripID(self,problems):
    if util.IsEmpty(self.trip_id):
        return
    if self.trip_id not in self._schedule.trips.keys():
      problems.InvalidValue('trip_id',self.trip_id,'Did not find a matching trip_id in trips.txt')
    

  def validateVehicleDescription(self,problems):
    #a description can be very unique so any format is really appropriate
    if util.IsEmpty(self.vehicle_description):
        return

    

  def ValidateSeatedCapacity(self,problems):
    if util.IsEmpty(self.seated_capacity):
        self.seated_capacity = 0
        return
    try:
      self.seated_capacity = int(self.seated_capacity)
    except (ValueError, TypeError):
      problems.InvalidValue('seated_capacity', self.seated_capacity,
          'Value must be non negative integer')
      del self.seated_capacity
      return
    if self.seated_capacity < 0:
      problems.InvalidValue('seated_capacity', self.seated_capacity,
          'Value must be non negative integer')
    

  def ValidateStandingCapacity(self,problems):
    if util.IsEmpty(self.standing_capacity):
        self.standing_capacity = 0
        return
    try:
      self.standing_capacity = int(self.standing_capacity)
    except (ValueError, TypeError):
      problems.InvalidValue('standing_capacity', self.standing_capacity,
          'Value must be non negative integer')
      del self.standing_capacity
      return
    if self.standing_capacity < 0:
      problems.InvalidValue('standing_capacity', self.standing_capacity,
          'Value must be non negative integer')
    

  def ValidateWheelChairCapacity(self,problems):
    if util.IsEmpty(self.wheelchair_capacity):
        self.wheelchair_capacity = 0
        return
    try:
      self.wheelchair_capacity = int(self.wheelchair_capacity)
    except (ValueError, TypeError):
      problems.InvalidValue('wheelchair_capacity', self.wheelchair_capacity,
          'Value must be non negative integer')
      del self.wheelchair_capacity
      return
    if self.wheelchair_capacity < 0:
      problems.InvalidValue('wheelchair_capacity', self.wheelchair_capacity,
          'Value must be non negative integer')
    

  def ValidateBikeCapacity(self,problems):
    if util.IsEmpty(self.bike_capacity):
        self.bike_capacity = 0
        return
    try:
      self.bike_capacity = int(self.bike_capacity)
    except (ValueError, TypeError):
      problems.InvalidValue('bike_capacity', self.bike_capacity,
          'Value must be non negative integer')
      del self.bike_capacity
      return
    if self.bike_capacity < 0:
      problems.InvalidValue('bike_capacity', self.bike_capacity,
          'Value must be non negative integer')
    

  def validateagencieID(self,problems):
    if util.IsEmpty(self.agency_id):
        return
    if self.agency_id not in self._schedule._agencies.keys():
      problems.InvalidValue('agency_id',self.agency_id,'Did not find a matching agency_id in agencies.txt')

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    #found_problem = self.validateServiceDate(problems)
    found_problem = self.validateVehicleDescription(problems)
    found_problem = self.ValidateSeatedCapacity(problems)
    found_problem = self.ValidateStandingCapacity(problems)
    found_problem = self.ValidateWheelChairCapacity(problems)
    found_problem = self.ValidateBikeCapacity(problems)
    found_problem = self.validateagencieID(problems)
    found_problem = self.validateTripID(problems)
    found_problem = self.validateServiceDate(problems)

    

    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    self.Validate(problems)

  #def AddToSchedule(self, schedule, problems):
    #schedule.AddBoardAlightObject(self, problems)