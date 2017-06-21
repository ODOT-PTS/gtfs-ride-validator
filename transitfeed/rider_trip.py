from problems import default_problem_reporter
from gtfsobjectbase import GtfsObjectBase

class Rider_trip(GtfsObjectBase):
  """This class represents a rule that determines which itineraries a
  fare rule applies to."""
  _REQUIRED_FIELD_NAMES = ['rider_id','trip_id']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + [
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
    self.boardTimeMin = None
    self.boardTimeMax = None

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

  def validateBoardingTimeFormat(self,problems):
    if self.boarding_time is not None:
      accept = util.checkInProperTimeFormat(self.boarding_time)
      if accept == 0:
        problems.UnknownTimeFormat('boarding_time',self.boarding_time)

  def validateAlightingTimeFormat(self,problems):
    if self.alighting_time is not None:
      accept = util.checkInProperTimeFormat(self.alighting_time)
      if accept == 0:
        problems.UnknownTimeFormat('alighting_time',self.alighting_time)

  def validateRiderType(self,problems):
    if self.current_load is not None:
      if self.rider_type  < 0 or self.rider_type>11:
        problems.InvalidValue('rider_type', self.rider_type)

  def validateFarePaid(self,problems):
    if self.fare_paid is not None:
      if str(self.fare_paid).isDecimal() == False:
        problems.InvalidValue('fare_paid', self.fare_paid)

  def validateFareMethod(self,problems):
    if self.fare_method is not None:
      if isInstance(self.fare_method,int) == False or self.fare_method<0 or self.fare_method > 5:
        problems.InvalidValue('fare_method', self.fare_method)

  def validateAccompanyingDevice(self,problems):
    if self.accompanying_device is not None:
      if isInstance(self.accompanying_device,int) == False or self.accompanying_device<0 or self.accompanying_device > 4:
        problems.InvalidValue('accompanying_device', self.accompanying_device)

  def validateTransferStatus(self,problems):
    if self.transfer_status is not None:
      if isInstance(self.transfer_status,int) == False or self.transfer_status<0 or self.transfer_status > 1:
        problems.InvalidValue('accompanying_device', self.accompanying_device)

  def validateBoardingDate(self,problems):
    if self.boarding_date is not None:
      date = util.DateStringToDateObject(self.boarding_date)
      dateMin = util.DateStringToDateObject(self.boardTimeMin)
      dateMax = util.DateStringToDateObject(self.boardTimeMax)
      accept = util.CheckIfInBetweenDates(dateMin,dateMax,date)
      if accept == 0:
        problems.DateOutsideValidRangeGTFSRide('boarding_date', int(self.boarding_date),int(self.boardTimeMin),int(self.boardTimeMax))

  def validateAlightingDate(self,problems):
    if self.alighting_date is not None:
      date = util.DateStringToDateObject(self.alighting_date)
      dateMin = util.DateStringToDateObject(self.boardTimeMin)
      dateMax = util.DateStringToDateObject(self.boardTimeMax)
      accept = util.CheckIfInBetweenDates(dateMin,dateMax,date)
      if accept == 0:
        problems.DateOutsideValidRangeGTFSRide('alighting_date', int(self.alighting_date),int(self.boardTimeMin),int(self.boardTimeMax))

  def Validate(self, problems=default_problem_reporter):
    """Validate attribute values and this object's internal consistency.

    Returns:
      True iff all validation checks passed.
    """
    found_problem = False
    found_problem = ((not util.ValidateRequiredFieldsAreNotEmpty(
                          self, self._REQUIRED_FIELD_NAMES, problems))
                          or found_problem)
    found_problem = self.validateBoardingTimeFormat(problems)
    found_problem = self.validateAlightingTimeFormat(problems)
    found_problem = self.validateRiderType(problems)
    found_problem = self.validateFarePaid(problems)
    found_problem = self.validateFareMethod(problems)
    found_problem = self.validateAccompanyingDevice(problems)
    found_problem = self.validateTransferStatus(problems)
    found_problem = self.validateBoardingDate(problems)
    found_problem = self.validateAlightingDate(problems)

    return not found_problem

  def ValidateBeforeAdd(self, problems):
    return True

  def ValidateAfterAdd(self, problems):
    return